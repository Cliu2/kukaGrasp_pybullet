import os, inspect, pickle
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(os.path.dirname(currentdir))
workdir=os.path.dirname(currentdir)
os.sys.path.insert(0,parentdir)

from RewardLearner import RewardLearner
from kukaGrasp_pybullet.util import utils
import numpy as np
from matplotlib import pyplot as plt

class ReplayRewardLearner(RewardLearner):

	def calculateUtility(self,state,action,reward,nextState):
		return (reward+self.decay*self.network.getUtility(np.array([nextState]),self.environment.action_space)[0][0])

	def learn(self):
		explorePosibility=utils.DecayNumber(0.8,'linear',1/1000)
		lrController=utils.DecayNumber(0.5,'sigmoid',0.02,minV=0.01)
		replayBuffer=utils.ReplayBuffer(170,useNextState=True)		
		successRecorder=self.successRecorder
		succ=True
		states,actions,Y=[],[],[]
		self.environment.reset()
		for epi in range(1,self.episodes+1):
			initState=self.resetEnvironment(False,succ)
			initState=self.randomCutImages(initState,self.networkDimension)
			state=initState			
			done,step=False,0		
			states,actions,Y=[],[],[]	
			while not done and step<20:
				states.append(np.concatenate((initState,state),axis=1))
				action=self.network.getAction(np.array([states[-1]]),self.environment.action_space)[0]
				# print(action)
				# action=[x+np.random.random()*0.3-0.15 for x in action]
				# action=[min(1,x) for x in action]
				# action=[max(-1,x) for x in action]
				# print(action)
				actions.append(action)
				state,reward,done,info=self.environment.step(action)
				# print("reward:",reward)
				# plt.imshow(np.reshape(states[-1],(472,944)))
				# plt.show()
				# input()
				state=self.randomCutImages(state,self.networkDimension)
				self.recordTargets(reward,info,Y)
				step+=1
				
			replayBuffer.addRecords(states,actions,Y)
			replayBuffer.addRecord(None,None,None)
			# print(Y)
			# input()
			states,actions,Y=[],[],[]
			succ=info['grasp_success']
			isHighest=successRecorder.appendResult(succ==1)
			if epi%10==0: successRecorder.report()
			# print(Y)
			# self.network.displayImageFeatures(np.array([states[-1]]))
			print(epi,":",succ==True)
			if epi%self.epochsPerTraining==0:
				states,actions,Y,nextStates=replayBuffer.getRecord(70)				
				# self.trainModel(states,actions,targets,succ,epochs=self.epochs, verbose=self.verbose)
				for epochs in range(self.epochs):
					targets=self.getTrainTargets(states,actions,Y,nextStates,self.environment.action_space)
					trainActor=(epochs==(self.epochs-1))
					self.trainModel(states,actions,targets,succ,epochs=self.epochs*2, verbose=self.verbose,action=trainActor)
				print(targets)
				# input()
				replayBuffer.cleanBuffer()	
			if isHighest:
				self.saveTrainingResult()

	def getTrainTargets(self,states,actions,targets,nextStates,actionSpace):
		utilities=list(targets)
		for i in range(len(utilities)-1):
			currentState,nextState=states[i],nextStates[i]
			if nextState is None:
				continue
			# plt.imshow(np.reshape(currentState,(472,944)))
			# plt.show()
			# plt.imshow(np.reshape(nextState,(472,944)))
			# plt.show()
			utilities[i]=utilities[i]+self.decay*self.network.getUtility(np.array([nextState]),actionSpace)[0][0]
		return utilities

	def trainModel(self,states,actions,targets,success,epochs=20,verbose=0,action=False):		
		self.network.fitModel([np.array(states),np.array(actions)],np.array(targets),epochs=epochs,verbose=verbose,action=action)