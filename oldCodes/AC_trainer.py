import os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(os.path.dirname(currentdir))
os.sys.path.insert(0,parentdir)

from kukaGrasp_pybullet.environments.lance_kuka_diverse_env import LanceKukaDiverseObjectEnv
from kukaGrasp_pybullet.networks.ActorCriticNetwork import ActorNetwork, CriticNetwork
import tensorflow as tf
from keras import backend as K
import random
import numpy as np
import atexit,pickle
from matplotlib import pyplot

MODEL_PATH="20181202_ACN"
MAXTRAIL=10000
DISCOUNTING_RATE=0.65
WIDTH,HEIGHT=512,512 #set resolution of camera
CHANNEL=1
SUCCESS_REWARD=500
MAX_DATA_SIZE=30
SUCCESS_RATE_HISTORY=[]
actor,critic=None,None

def exit_handler():
	global actor,critic
	actorPath='../models/'+MODEL_PATH+'/actor.h5'
	criticPath='../models/'+MODEL_PATH+'/critic.h5'
	if not os.path.exists('../models/'+MODEL_PATH): os.makedirs('../models/'+MODEL_PATH)
	actor.save(actorPath)
	critic.save(criticPath)
	print("models saved in the path: ../models/'",MODEL_PATH,"'/, exiting...")
	with open("../logs/"+MODEL_PATH[0:8]+'_successRateHistory.pkl', 'wb') as f:  # Python 3: open(..., 'wb')
			pickle.dump([SUCCESS_RATE_HISTORY],f)

def initEnvironment():
	global actor,critic
	#specify using GPU
	config = tf.ConfigProto()
	config.gpu_options.allow_growth = True
	sess = tf.Session(config=config)
	K.set_session(sess)

	#load saved model if exist

	actor=ActorNetwork(sess,(WIDTH,HEIGHT,CHANNEL),4,rewardStepLength=0.01,lr=0.1)
	critic=CriticNetwork(sess,(WIDTH,HEIGHT,CHANNEL),4,rewardStepLength=0.01,lr=0.1)

	actorPath='../models/'+MODEL_PATH+'/actor.h5'
	criticPath='../models/'+MODEL_PATH+'/critic.h5'
	if os.path.isfile(actorPath): actor.load(actorPath)
	if os.path.isfile(criticPath): critic.load(criticPath)

	#set exit handler to save model if unexpected termination
	atexit.register(exit_handler)

	#start environment
	environment = LanceKukaDiverseObjectEnv(renders=False, isDiscrete=False, \
		removeHeightHack=True,width=WIDTH,height=HEIGHT,cameraRandom=1)

	return environment,actor,critic

def train():
	#Tensorflow with GPU
	environment,actor,critic=initEnvironment()
	# initState=environment.reset()

	#train
	trail=0
	last100success=[]
	success=0
	successData,failData=None,None
	lastResultFlag=True
	failTimes=0
	while trail<MAXTRAIL:
		environment._numObjects=random.randint(1,5)
		if lastResultFlag or failTimes>=10:
			initState=environment.reset()
			failTimes=0
		else:
			failTimes+=1
			initState=environment.softReset()
		state=initState
		statesForTrain,actions,rewards,nextStates,dones=[],[],[],[],[]
		done,step=False,0
		loss=0
		while not done and step<20:
			currentState=list(initState)+list(state)
			statesForTrain.append(currentState)
			action=actor.model.predict(np.array([currentState]))
			# pyplot.imshow(np.array(currentState)[:,:,0])
			# pyplot.show()
			# input()
			
			if random.random()<0.3*(1-float(trail)/float(MAXTRAIL)):
				action[0]=environment.action_space.sample()
				if random.random()<0.8:
					action[0][2]=-0.8
				# print("random")
			else:
				print(action)
			real_action=list(action[0])+[0]
			# print(real_action)
			state,reward,done,info=environment.step(real_action)
			actions.append(action[0])
			rewards.append(reward)
			dones.append(done)
			nextStates.append(list(initState)+list(state))
			step+=1
		# if rewards[-1]!=SUCCESS_REWARD: rewards[-1]=0
		# print(rewards)
		# ---check the predict reward against actual reward---
		# utilities, Putilities=list(rewards),list(rewards)
		# for i in range(len(utilities)-2,-1,-1): 
		# 	utilities[i]=critic.model.predict([np.array([statesForTrain[i]]),np.array([actions[i]])])[0][0]
		# 	nextA=actor.model.predict(np.array([nextStates[i]]))
		# 	nextQ=critic.model.predict([np.array([nextStates[i]]),nextA])
		# 	Putilities[i]=nextQ[0][0]*DISCOUNTING_RATE+rewards[i]
		# print("critic error:",np.array([x-y for (x,y) in zip(utilities,Putilities)]))

		
		#get training data
		data=[statesForTrain,actions,rewards,nextStates,dones]
		if rewards[-1]==SUCCESS_REWARD:
		# if True:
			if successData!=None:
				for i in range(len(data)):
					successData[i]=list(successData[i])+list(data[i])
					if len(successData[i])>MAX_DATA_SIZE:
						successData[i]=successData[i][-MAX_DATA_SIZE:]
			else:
				successData=data
		else:
			if failData!=None:
				for i in range(len(data)):
					failData[i]=list(failData[i])+list(data[i])
					if len(failData[i])>MAX_DATA_SIZE:
						failData[i]=failData[i][-MAX_DATA_SIZE:]
			else:
				failData=data

		trail+=1
		success+=1 if (rewards[-1]==SUCCESS_REWARD) else 0
		lastResultFlag=(rewards[-1]==SUCCESS_REWARD)
		if trail>100:
			last100success.pop(0)
		if (rewards[-1]==SUCCESS_REWARD):
			last100success.append(1)
		else:
			last100success.append(0)
		print("trail",trail, (rewards[-1]==SUCCESS_REWARD))
		
		if trail%10==0:
				rate=len([x for x in last100success if x==1])/100 \
					if trail>100 else success/trail
				print("grasp success rate (last 100 tries):",rate)
				SUCCESS_RATE_HISTORY.append(rate)
				
		if trail%1==0:
			# data=list(successData) if successData!=None else list(failData)
			for fData in [True,False]:
				if fData:
					if failData==None: continue
					data=list(failData)
				else:
					if successData==None:continue
					data=list(successData)
			# for i in range(5):
				# data[i]=(list(random.sample(list(successData[i]),int(len(successData[i])*1.0))) if successData!=None else []) + \
				# 		(list(random.sample(list(failData[i]),int(len(failData[i])*0.5))) if failData!=None else [])
				# data[i]=(list(successData[i]) if successData!=None else [])+(list(failData[i]) if failData!=None else [])
			
			# nw.trainSuccessFail(data[0],data[1],data[2],data[3],data[4])
				Xstates=data[0]
				Xactions=data[1]
				Xrewards=data[2]
				XnextStates=data[3]
				Xdones=data[4]
				Xutilities=np.array(Xrewards).astype(float)
				for i in range(len(Xutilities)):
					nextS=XnextStates[i]
					nextA=actor.model.predict(np.array([nextS]))
					nextQ=critic.model.predict([np.array([nextS]),nextA])
					if Xdones[i]:
						Xutilities[i]=Xrewards[i]
					else:
						Xutilities[i]=nextQ[0][0]*DISCOUNTING_RATE+Xrewards[i]
				

				critic.model.fit([np.array(Xstates),np.array(Xactions)],np.array(Xutilities),epochs=int(50*(1.10-trail/MAXTRAIL)),verbose=0)
				Yactions,grads=None,None
				for i in range(int(5*(1.5-trail/MAXTRAIL))):
					if fData:
						# a_for_grad=actor.model.predict(np.array(Xstates))
						a_for_grad=np.array(Xactions)
						grads=critic.gradients(Xstates,a_for_grad)
						# grads=critic.gradients(Xstates,np.array(Xactions))
						# actor.train(np.array(Xstates),np.array(grads))
						Yactions=np.array(a_for_grad)+max(0.5*(1-trail/MAXTRAIL),0.01)*np.array(grads)
					else:
						Yactions=np.array(Xactions)
						# grads=critic.gradients(Xstates,np.array(Yactions))
					# print(grads[:,3])
					# print("Y",Yactions)
					# print("X",np.array(Xactions))
					# input()
					actor.model.fit(np.array(Xstates),np.array(Yactions),verbose=0,epochs=int(50*(1.10-trail/MAXTRAIL)))
				# print("grads:",grads[-10:])
				print("Yactions:",Yactions[-10:])
				# input()


if __name__=="__main__":
	train()