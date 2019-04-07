import os, inspect, pickle
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(os.path.dirname(currentdir))
workdir=os.path.dirname(currentdir)
os.sys.path.insert(0,parentdir)

from kukaGrasp_pybullet.environments.lance_kuka_diverse_env import LanceKukaDiverseObjectEnv
from kukaGrasp_pybullet.environments.positionEnv import positionEnv
from kukaGrasp_pybullet.util import utils
from kukaGrasp_pybullet.networks.CNN_for_sure import CNN_for_sure
import tensorflow as tf
import datetime,atexit
import numpy as np

FILENAME='/home/ubuntu/Desktop/LanceFYP/fyp/models/20190331_TunedCamera_512x512/model.ckpt'

environment = LanceKukaDiverseObjectEnv(renders=True, isDiscrete=False, \
		removeHeightHack=True,width=512,height=512,cameraType=2,cameraRandom=0)

con = tf.ConfigProto()
con.gpu_options.allow_growth = True
sess = tf.Session(config=con)

network=CNN_for_sure(sess,(512,512,3,),(4,))

def exit_handler():
	global network
	network.saveModel(FILENAME)

atexit.register(exit_handler)
# network.loadModel(FILENAME)

X,Y=[],[]
total=0
for episode in range(0):
	print(episode)
	state=environment.reset()
	target=environment.getTarget()
	# print("target:",target)
	position=environment.getPosition()
	
	for step in range(20):
		X.append(state)
		act=network.predict([state])[0]
		#Normalize
		# print("act:",act)
		act=[a/1000 for a in act]
		act[2]*=10
		act=[min(1,max(-1,a)) for a in act]
		position=environment.getPosition()
		# print("pos:", position)
		# print("image Feature:",network.printImageFeature(np.array([state])))
		t_act=target-position
		t_act[2]-=0.02*100
		t_act=np.append(t_act,90)
		state,reward,done,info=environment.step(act)
		# print("suggest_act",t_act)
		# input()
		Y.append(t_act)
		if done:
			break
	if info['grasp_success']:
		total+=1
		print("total success:",total)
		# print("final result:",info['grasp_success'])

	if episode%10==9:
		network.train(X,Y,epochs=100,verbose=2)
		X,Y=[],[]

network.saveModel(FILENAME)

print("===test===")
total=0
for episode in range(50):
	state=environment.reset()
	for step in range(22):
		X.append(state)
		act=network.predict([state])[0]
		#Normalize
		act=[a/1000 for a in act]
		act[2]*=10
		act=[min(1,max(-1,a)) for a in act]
		# print(act)
		state,reward,done,info=environment.step(act)
		if done:
			break
	pos=environment.getPosition()
	if pos[2]>0.1:
		act=[0,0,-pos[2]+0.02,0]
		state,reward,done,info=environment.step(act)
	if info['grasp_success']:
		total+=1
print(total)