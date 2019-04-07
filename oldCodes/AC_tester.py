import os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(os.path.dirname(currentdir))
os.sys.path.insert(0,parentdir)

from kukaGrasp_pybullet.oldCodes.ActorCriticNetwork import ActorNetwork, CriticNetwork
from kukaGrasp_pybullet.environments.lance_kuka_diverse_env import LanceKukaDiverseObjectEnv
from keras import backend as K
import tensorflow as tf
import numpy as np
import atexit
import random

MODEL_PATH="20181202_ACN"
WIDTH,HEIGHT=512,512 #set resolution of camera
CHANNEL=1

def getActionCEM(critic,state,actionSpace):
	actions=[]
	bestAction=actionSpace.sample()
	for i in range(256):
		actions.append(actionSpace.sample())
	rewards=list(critic.model.predict([np.array([state for x in actions]),np.array(actions)]))
	actions=[x for _,x in sorted(zip(rewards,actions),key=lambda y:y[0])]
	actions=np.array(actions[-8:])
	mean=np.mean(actions,axis=0)
	covariance=np.cov(actions,rowvar=0)
	while np.linalg.norm(bestAction-mean)>0.05:
		actions=[]
		bestAction=mean
		while len(actions)<128:
			action=np.random.multivariate_normal(mean,covariance)
			if actionSpace.contains(action):
				actions.append(action)
		rewards=list(critic.model.predict([np.array([state for x in actions]),np.array(actions)]))
		actions=[x for _,x in sorted(zip(rewards,actions),key=lambda y:y[0])]
		actions=np.array(actions[-8:])
		mean=np.mean(actions,axis=0)
		covariance=np.cov(actions,rowvar=0)
	return bestAction

if __name__=="__main__":

	config = tf.ConfigProto()
	config.gpu_options.allow_growth = True
	sess = tf.Session(config=config)
	K.set_session(sess)

	actor=ActorNetwork(sess,(WIDTH,HEIGHT,CHANNEL),4,rewardStepLength=0.01,lr=0.001)
	critic=CriticNetwork(sess,(WIDTH,HEIGHT,CHANNEL),4,rewardStepLength=0.01,lr=0.0001)

	actorPath='../models/'+MODEL_PATH+'/actor.h5'
	criticPath='../models/'+MODEL_PATH+'/critic.h5'
	actor.load(actorPath)
	critic.load(criticPath)



	numObj=1
	environment = LanceKukaDiverseObjectEnv(renders=True, isDiscrete=False, \
		removeHeightHack=True,width=512,height=512,isTest=True,cameraRandom=1)
	#environment = LanceKukaDiverseObjectEnv(renders=True, isDiscrete=False, removeHeightHack=True, numObjects=numObj)
	success,total=0,0
	for i in range(500):
		done=False
		numObj=random.randint(1,1)
		environment._numObjects=numObj
		step=0
		state=environment.reset()
		initState=list(state)
		while not done and step<30:
			# predictAction=getActionCEM(critic,initState+list(state),environment.action_space)
			predictAction=actor.model.predict(np.array([list(initState)+list(state)]))[0]
			# predictAction=environment.action_space.sample()
			# if random.random()<0.6:
			# 	predictAction[2]=-0.7
			# print(predictAction)

			state,reward,done,info=environment.step(predictAction)
			# print("actualReward:",reward)
			step+=1
			# actor.displayImageFeatures(np.array([list(initState)+list(state)]))
		if reward>0:
			success+=1
		total+=1
		print("success rate:",success/total)