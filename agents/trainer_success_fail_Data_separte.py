import os, inspect, pickle
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(os.path.dirname(currentdir))
os.sys.path.insert(0,parentdir)

from kukaGrasp_pybullet.environments.kuka_diverse_object_gym_env import KukaDiverseObjectEnv
from kukaGrasp_pybullet.environments.lance_kuka_diverse_env import LanceKukaDiverseObjectEnv
import tensorflow as tf
from keras.layers import merge
from tensorflow import keras
import numpy as np
from kukaGrasp_pybullet.networks.QLearnNetwork import possibilityNetwork
import atexit
import math,random

MODEL_FILE_NAME="../models/20181024_successfail_trainer.h5"
MAXTRAIL=5000
DISCOUNTING_RATE=0.7
WIDTH,HEIGHT=512,512 #set resolution of camera
CHANNEL=3
SUCCESS_REWARD=500
MAX_DATA_SIZE=500

def exit_handler():
	try:
		nw.saveModel(MODEL_FILE_NAME)
		print("model saved as '",MODEL_FILE_NAME,"', exiting...")
		with open(MODEL_FILE_NAME[0:8]+'_successRateHistory.pkl', 'wb') as f:  # Python 3: open(..., 'wb')
				pickle.dump([successRateHistory],f)
	except NameError:
		pass

def initEnvironment():
	#specify using GPU
	gpu_options=tf.GPUOptions(allow_growth=True)
	session = tf.InteractiveSession(config=tf.ConfigProto(gpu_options=gpu_options))

	#load saved model if exist
	nw=possibilityNetwork(imageDimension=(WIDTH,HEIGHT,CHANNEL), \
		actionDimension=(4,), discounting=DISCOUNTING_RATE)
	if os.path.isfile(MODEL_FILE_NAME):
		nw.loadModel(MODEL_FILE_NAME)

	#set exit handler to save model if unexpected termination
	atexit.register(exit_handler)

	#start environment
	environment = LanceKukaDiverseObjectEnv(renders=False, isDiscrete=False, \
		removeHeightHack=True,width=WIDTH,height=HEIGHT)

	nw.action_space=environment.action_space
	return environment,nw

def naiveHuresticAction():
	dx, dy, dz, da = environment.action_space.sample()
	if np.random.random() < 0.6:
		dz = -1
	action = [dx, dy, dz, da]
	return action

if __name__=="__main__":
	environment,nw=initEnvironment()

	trail=0
	success=0
	nw.rewardStepLength=0.5
	successData,failData=None,None
	successRateHistory=[]
	while trail<MAXTRAIL:
		environment._numObjects=random.randint(1,9)	#randomize number of obejcts
		initState=environment.reset()
		state=initState
		statesForTrain,actions,rewards,nextStates=[],[],[],[]
		done,step=False,0		
		while not done and step<20:
			statesForTrain.append(list(initState)+list(state))
			action=None
			if np.random.random()< max(0.3,0.8/(1+0.001*trail)): # some naive hurestic
				action=naiveHuresticAction()
			else:
				action=nw.getBestAction(statesForTrain[-1],environment.action_space)
			action_env=list(action)+[0] #convert to the 5-d based action, the last always 0 for finger angle
			actions.append(action)
			state,reward,done,info=environment.step(action_env)
			rewards.append(reward)
			nextStates.append(list(initState)+list(state))
			step+=1
		# calculate utilities
		utilities=np.array(rewards)
		for i in range(len(utilities)-2,-1,-1):
			utilities[i]=utilities[i+1]*DISCOUNTING_RATE+utilities[i]
		
		#get training data
		data=[statesForTrain,actions,rewards,utilities,nextStates]
		if utilities[-1]==SUCCESS_REWARD:
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
		print("trail",trail, (rewards[-1]==SUCCESS_REWARD))
		# print("rewards",rewards)
		if trail%10==0:
			print("grasp success rate:",success/trail)
			successRateHistory.append(success/trail)
			
		if trail%3==0:
			data=successData if successData!=None else failData
			for i in range(5):
				data[i]=list(successData[i]) if successData!=None else [] + \
						list(failData[i]) if failData!=None else []
			nw.epochs=max(int(50/(1+1/15*trail)),20)
			nw.trainSuccessFail(data[0],data[1],data[2],data[3],data[4])
		#"""

		