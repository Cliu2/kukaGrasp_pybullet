import os, inspect
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

MODEL_FILE_NAME="../models/20181020_no_action_penalty.h5"
MAXTRAIL=3000
DISCOUNTING_RATE=0.75
WIDTH,HEIGHT=512,512 #set resolution of camera
CHANNEL=3
SUCCESS_REWARD=100

def exit_handler():
	try:
		nw.saveModel(MODEL_FILE_NAME)
		print("model saved as '",MODEL_FILE_NAME,"', exiting...")
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
	return environment,nw

def naiveHuresticAction():
	dx, dy, dz, da = environment.action_space.sample()
	if np.random.random() < 0.5:
		dz = -1
	action = [dx, dy, dz, da]
	return action

if __name__=="__main__":
	environment,nw=initEnvironment()

	trail=0
	success=0
	nw.rewardStepLength=0.5
	statesForTrain,actions,rewards,nextStates=[],[],[],[]
	breakpoints=[]
	while trail<MAXTRAIL:
		environment._numObjects=random.randint(2,6)	#randomize number of obejcts
		initState=environment.reset()
		state=initState
		# statesForTrain,actions,rewards,nextStates=[],[],[],[]
		done,step=False,0		
		while not done and step<20:
			statesForTrain.append(np.array(list(initState)+list(state)))
			action=None
			if np.random.random()<0.8:#/(1+0.1*trail): # some naive hurestic
				action=naiveHuresticAction()
			else:
				action=nw.getBestAction(statesForTrain[-1],environment.action_space)
			action_env=list(action)+[0] #convert to the 5-d based action, the last always 0 for finger angle
			actions.append(action)
			state,reward,done,info=environment.step(action_env)
			nextStates.append(np.array(list(initState)+list(state)))
			rewards.append(reward)
			step+=1
		#train network using the data allocated in this trail
		""" only for train without next state
		for i in range(len(rewards)-2,-1,-1):
			rewards[i]=rewards[i+1]*DISCOUNTING_RATE+rewards[i]
		
		nw.train(statesForTrain,actions,rewards)
		"""

		trail+=1
		success+=1 if (rewards[-1]==SUCCESS_REWARD) else 0
		print("trail",trail, (rewards[-1]==SUCCESS_REWARD))
		# print("rewards",rewards)
		if trail%10==0:
			print("grasp success rate:",success/trail)

		#""" train network with information given on next state
		# graspSuccess= rewards[-1]==SUCCESS_REWARD
		# nw.epochs= max(int(300/(1+1/15*trail)),20) if graspSuccess else 5
		# nw.rewardStepLength=1 #max(0.01,nw.rewardStepLength*0.97)
		# rewards[-1]=max(0,rewards[-1])
		breakpoints.append(step)
		if trail%20==0:
			print(breakpoints)
			for i in range(1,len(breakpoints)):
				breakpoints[i]=breakpoints[i]+breakpoints[i-1]
			print(breakpoints)
			nw.epochs=max(int(50/(1+1/15*trail)),10)
			nw.trainWithNextState(statesForTrain,actions,rewards,nextStates,environment.action_space,breakpoints)
			statesForTrain,actions,rewards,nextStates=[],[],[],[]
		#"""

		
