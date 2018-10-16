import os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(os.path.dirname(currentdir))
os.sys.path.insert(0,parentdir)

from environments.kuka_diverse_object_gym_env import KukaDiverseObjectEnv
from environments.lance_kuka_diverse_env import LanceKukaDiverseObjectEnv
import time
import tensorflow as tf
from keras.layers import merge
from tensorflow import keras
import numpy as np
import networks.QLearnNetwork
import atexit
import os
import math

if __name__=="__main__":

	nw=network.possibilityNetwork(imageDimension=(512,512,3), \
		actionDimension=(4,), discounting=0.9)
	if os.path.isfile('../models/lancePossibilityModel_nextStateIncluded.h5'):
		nw.loadModel('../models/lancePossibilityModel_nextStateIncluded.h5')

	numObj=1
	environment = LanceKukaDiverseObjectEnv(renders=True, isDiscrete=False, \
		removeHeightHack=True,width=512,height=512)
	#environment = LanceKukaDiverseObjectEnv(renders=True, isDiscrete=False, removeHeightHack=True, numObjects=numObj)
	success,total=0,0
	while True:
		done=False
		numObj=(numObj+1)%5+1
		environment._numObjects=numObj
		step=0
		state=environment.reset()
		initState=list(state)
		while not done and step<30:
			predictAction=nw.getBestAction(initState+list(state),environment.action_space)
			state,reward,done,info=environment.step(predictAction)
			step+=1
		if reward>0:
			success+=1
		total+=1
		print("success rate:",success/total)