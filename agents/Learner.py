import os, inspect, pickle
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(os.path.dirname(currentdir))
workdir=os.path.dirname(currentdir)
os.sys.path.insert(0,parentdir)

from kukaGrasp_pybullet.environments.lance_kuka_diverse_env import LanceKukaDiverseObjectEnv
from kukaGrasp_pybullet.environments.positionEnv import positionEnv
from kukaGrasp_pybullet.util import utils
import tensorflow as tf
import datetime
import numpy as np

class Learner():
	def __init__(self,sess,network,modelFileName,episodes,lr=0.1,decay=0.9, \
		imageDimension=(512,512),display=False,cameraType=3,cameraRandom=1, \
		objectRange=(2,6),networkDimension=(472,472),epochsPerTraining=10,epochs=50,verbose=0):
		"""
		Args: 
			network: the network class to be used
			modelFileName: the file names for models to be saved as
			episode: the numerb of episodes the agent will learn
			decay: reward decay rate
			imageDimension: the resolution of iamge input (HEIGHT,WIDTH)
			display: Bool, whether render will be used
			cameraType: the camera to be used, 2 for RGB, 3 for depth camera, 4 for segment camera
			cameraRandom: whether randomize the location of camera, 1 for random, 0 for fixed
			objectRange: the lower limit and upper limit of number of objects
		"""
		self.sess=sess
		self.date=datetime.datetime.now().strftime("%Y%m%d")
		self.episodes=episodes
		self.decay=decay
		self.lr=lr
		self.modelPath="{pdir}/models/{date}_{name}/model.ckpt".format(pdir=workdir,date=self.date,name=modelFileName)
		self.logFileName="{pdir}/logs/{date}_{name}.pkl".format(pdir=workdir,date=self.date,name=modelFileName)
		modelDir="{pdir}/models/{date}_{name}/".format(pdir=workdir,date=self.date,name=modelFileName)
		if not os.path.exists(modelDir):
			os.makedirs(modelDir)
		self.epochsPerTraining=epochsPerTraining
		if cameraType==3 or cameraType==4:
			imageDimension+=(1,)
			networkDimension+=(1,)
		elif cameraType==2:
			imageDimension+=(3,)
			networkDimension+=(3,)
		self.imageDimension=imageDimension
		self.networkDimension=networkDimension
		networkDimension=(self.networkDimension[0],self.networkDimension[1]*2,self.networkDimension[2])
		self.environment=self.initEnvironment(imageDimension,display,cameraType,cameraRandom)
		self.network=self.initNetwork(network,modelFileName,episodes,decay,networkDimension)
		self.resetCount=0
		self.successRecorder=utils.SuccessHistoryCounter()
		self.epochs=epochs
		self.verbose=verbose
		self.objectRange=objectRange
		

	def initEnvironment(self,imageDimension,display,cameraType,cameraRandom):
		#imageDimension: (WIDTH,HEIGHT,CHANNEL)
		environment = LanceKukaDiverseObjectEnv(renders=display, isDiscrete=False, \
		removeHeightHack=True,width=imageDimension[1],height=imageDimension[0],cameraType=cameraType,cameraRandom=1)
		# environment = positionEnv(renders=display, isDiscrete=False, \
		# removeHeightHack=True,width=imageDimension[1],height=imageDimension[0],cameraType=cameraType,cameraRandom=1)
		environment._numObjects=1
		return environment

	def goDownHuresticAction(self,prob=0.5,down=-0.7):
		dx,dy,dz,da=self.environment.action_space.sample()
		if np.random.random()<prob:
			dz=down
		return np.array([dx,dy,dz,da])

	def recordTargets(self,reward,info,targets):
		raise NotImplementedError("method not implemented")

	def getTrainTargets(self,states,actions,targets,succ,actionSpace):
		raise NotImplementedError("method not implemented")

	def trainModel(self,states,actions,targets,success,epochs=20,verbose=0):		
		self.network.fitModel([np.array(states),np.array(actions)],np.array(targets),epochs=epochs,verbose=verbose)

	def learn(self):
		explorePosibility=utils.DecayNumber(0.8,'linear',1/1000)
		lrController=utils.DecayNumber(0.5,'sigmoid',0.02,minV=0.01)
		successRecorder=self.successRecorder
		succ=True
		states,actions,Y=[],[],[]
		for epi in range(1,self.episodes+1):
			initState=self.resetEnvironment(False,succ)
			initState=self.randomCutImages(initState,self.networkDimension)
			state=initState			
			done,step=False,0			
			while not done and step<20:
				states.append(np.concatenate((initState,state),axis=1))
				if np.random.random()<explorePosibility.getNumber():
					action=self.goDownHuresticAction(prob=0.7)
				else:
					action=self.network.getAction(np.array([states[-1]]),self.environment.action_space)[0]
					print(action)
				actions.append(action)
				state,reward,done,info=self.environment.step(action)
				state=self.randomCutImages(state,self.networkDimension)
				self.recordTargets(reward,info,Y)
				step+=1
			Y[-1]=max(0,Y[-1])
			succ=info['grasp_success']
			isHighest=successRecorder.appendResult(succ==1)
			if epi%10==0: successRecorder.report()
			self.getTrainTargets(states,actions,Y,succ,self.environment.action_space)
			# print(Y)
			# self.network.displayImageFeatures(np.array([states[-1]]))
			print(epi,":",succ==True)
			if epi%self.epochsPerTraining==0:
				self.trainModel(states,actions,Y,succ,epochs=self.epochs, verbose=self.verbose)
				states,actions,Y=[],[],[]			
			if isHighest:
				self.saveTrainingResult()
		
	def resetEnvironment(self,useSoftReset,lastResult=True,resetLimit=15):
		numObj=np.random.randint(self.objectRange[0],self.objectRange[1])
		if useSoftReset:
			if lastResult or self.resetCount>resetLimit: 
				self.resetCount=0
				self.environment._numObjects=numObj
				return self.environment.reset()
			else:
				return self.environment.softReset()
		else:
			self.environment._numObjects=numObj
			return self.environment.reset()

	def initNetwork(self,network,modelFileName,episodes,decay,imageDimension):
		#decay is not used for this agent
		networkModule=utils.dynamicallyImport(network,['../networks'])
		networkClass=getattr(networkModule,network)
		network=networkClass(self.sess,imageDimension,(4,),(1,),(-1,1),lr=self.lr)
		return network

	def randomCutImages(self,state,cutShape):
		horizon=np.random.randint(0,state.shape[0]-cutShape[0])
		veritical=np.random.randint(0,state.shape[1]-cutShape[1])
		cut=state[horizon:horizon+cutShape[0],veritical:veritical+cutShape[1]]
		return cut

	def saveTrainingResult(self):
		print("model saved as:"+self.modelPath)
		self.network.saveModel(self.modelPath)
		print("log saved as:"+self.logFileName)
		self.successRecorder.saveRecord(self.logFileName)

	def loadModel(self,modelFileName):
		print("loading model:"+modelFileName)
		self.network.loadModel(modelFileName)
