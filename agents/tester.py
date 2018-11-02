import os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(os.path.dirname(currentdir))
os.sys.path.insert(0,parentdir)

from kukaGrasp_pybullet.environments.lance_kuka_diverse_env import LanceKukaDiverseObjectEnv
import time
import tensorflow as tf
from keras.layers import merge
from tensorflow import keras
import numpy as np
from kukaGrasp_pybullet.networks.QLearnNetwork import possibilityNetwork
import atexit
import os
import math

MODEL_FILE_NAME='20181029_successfail_trainer_dr0p9.h5'
TEST_ROUNDS=500

if __name__=="__main__":

	nw=possibilityNetwork(imageDimension=(512,512,3), \
		actionDimension=(4,), discounting=0.9)
	nw.loadModel(parentdir+'/kukaGrasp_pybullet/models/'+MODEL_FILE_NAME)

	numObj=1
	environment = LanceKukaDiverseObjectEnv(renders=False, isDiscrete=False, \
		removeHeightHack=True,width=512,height=512,cameraRandom=1)
	#environment = LanceKukaDiverseObjectEnv(renders=True, isDiscrete=False, removeHeightHack=True, numObjects=numObj)
	success,total=0,0
	for i in range(TEST_ROUNDS):
		done=False
		numObj=(numObj+1)%5+1
		environment._numObjects=numObj
		step=0
		state=environment.reset()
		initState=list(state)
		while not done and step<30:
			predictAction=nw.getBestAction(initState+list(state),environment.action_space)
			print("predictReward:",nw.predictReward(initState+list(state),predictAction))
			state,reward,done,info=environment.step(predictAction)
			# print("actualReward:",reward)
			step+=1
		if reward>0:
			success+=1
		total+=1
		print("success rate:",success/total)
	with open(parentdir+"/kukaGrasp_pybullet/logs/"+MODEL_FILE_NAME+"_testResult.txt", "w") as f:  # Python 3: open(..., 'wb')
		f.write("over all success rate:" +str(success/total))