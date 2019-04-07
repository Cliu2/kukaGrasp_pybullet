import os, inspect, pickle
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(os.path.dirname(currentdir))
workdir=os.path.dirname(currentdir)
os.sys.path.insert(0,parentdir)

from fyp.networks.CNN_for_sure import CNN_for_sure
import tensorflow as tf
import atexit
import numpy as np
from fyp.API.modules.gripper import *
from fyp.API.modules.rr_socket_interface import *
from fyp.API.modules.kinect_recorder import *
import cv2
import pdb

"""-----VARS-----"""
DATADIR='/home/ubuntu/Desktop/LanceFYP/fyp/data/20190404'
CONTINUE_GEN=True

"""--------------"""

gripper=Gripper()
gripper.speed = 100
arm=RR_interface(debug=False, speed=10, accel=20, zLimit=100)
totalRound=0

def onExit():
	goHome()
	gripper.status=False

atexit.register(onExit)

def generateData(rounds=100):
	global totalRound
	images,positions,targets,Yactions=loadData(CONTINUE_GEN)
	actions=[]
	

	# home_pos=[254.2, 1.54, 437.934, -25, 0, -180]
	initObject()	#attach an object, arm position at home

	for r in range(rounds):
		#1. put down the object randomly
		pos,_=arm.getCurPos()

		height_of_release = 130 # mm
		while(pos[2]>height_of_release):
			pos,_=arm.getCurPos()
			
			act=np.random.rand(3)*70-35
			act[0]=np.random.rand()*70-23
			act[2]=np.random.rand()*(-70)
			
			act = np.around(act, decimals=3)
			if pos[2]+act[2]>height_of_release:
				moveArm(act)					
			else:
				act[2]=height_of_release-pos[2]
				moveArm(act)
			# print("[Current position]: ", pos.tolist())
			# print("[Actions]: ", act)

		# targetPos,_=arm.getCurPos()

		gripper.status=False
		time.sleep(3) # gripper relase, object droped

		#1,5. move downward and update the targetPos and move back
		#moveArm(np.array([0,0,-40]))
		targetPos,_=arm.getCurPos()
		# print("[TargetPos]: ", targetPos)
		# targetPos[0]+=3
		targetPos[2]+=10
		#moveArm(np.array([0,0,40]))


		#2. move randomly and collect data
		totalStep=int(np.random.rand()*5+3)
		for step in range(totalStep):
			# strpos=' '.join([str(x) for x in pos[0:3]])
			# strtar=' '.join([str(x) for x in targetPos[0:3]])
			# filename="R{}S{} {} {}".format(r,step,strpos,strtar)
			act=np.random.rand(3)*30-15
			act[2]=np.random.rand()*(int(437/totalStep))
			while(not moveArm(act)):
				act=np.random.rand(3)*30-15
				act[2]=np.random.rand()*(int(437/totalStep))

			pos,_=arm.getCurPos()
			img=save_img(DATADIR,None)
			Yactions.append(targetPos-pos)
			images.append(img)
			positions.append(pos)
			targets.append(targetPos)
			actions.append(act)
			
			
		goHome()
		pos,_=arm.getCurPos()
		img=save_img(DATADIR,None)
		Yactions.append(targetPos-pos)
		images.append(img)
		positions.append(pos)
		targets.append(targetPos)



		#3. go back and grasp the object back to home point
		if not goTarget(targetPos,err=2):
			moveArm(np.array([30,30,-30]))
			#add some noise
			noise=np.random.rand(3)*2-1
			noise=np.append(noise,np.array([0,0,0]))
			while not goTarget(np.round(targetPos+noise,2),err=2):
				noise=np.random.rand(3)*2-1
				noise=np.append(noise,np.array([0,0,0]))

		# going downward, slow down the speed and acceleration first
		arm.setSpeed(1)
		arm.setAccel(3)
		while not moveArm(np.array([0,0,-40])):
			noise=np.random.rand(3)*2-1
			moveArm(noise)
		arm.setSpeed(10)
		arm.setAccel(20)


		gripper.status=True
		time.sleep(1)
		goHome()

	totalRound+=rounds
	# saveData(images,positions,targets,Yactions)

# exception safe handling if raising error 
def moveArm(act,error=1):
	displacement=np.append(act,np.array([0,0,0]))
	#displacement=[round(d,2) for d in displacement]
	try:
		arm.goDeltaPos(deltaPos=displacement.tolist(),error=error)
		# pdb.set_trace()
		# prevent it from sudden stop, add a delay for it
		time.sleep(0.05)
		return True
	except Exception as e:
		print("[ErrIK] Cannot move ",displacement, type(e), e)
		# input()
		time.sleep(0.1)
		# type(e) == UserWarning / ValueError
		# str(e) == ErrIK/reached height limit
		return False

def goHome():
	try:
		arm.goHome()
		return True
	except Exception as e:
		print(type(e), e)
		return False

def goTarget(target,err):
	try:
		arm.goPos(target.tolist(),error=err)
		return True
	except Exception as e:
		print(type(e),e)
		return False

def initObject():
	status=False
	goHome()
	gripper.status=True
	while(True):
		print('Attach an object to the Gripper, press <Enter> to toggle gripper.\nIf done, enter "s"')
		if ("s"==input()):
			gripper.status==True
			break
		gripper.toggle()

def saveData(images,positions,targets,Yactions):
	global totalRound
	np.save(DATADIR+"/img",np.array(images))
	np.save(DATADIR+"/pos",np.array(positions))
	np.save(DATADIR+"/tar",np.array(targets))
	np.save(DATADIR+"/Yactions",np.array(Yactions))
	np.save(DATADIR+"/totalRound",np.array([totalRound]))

def loadData(continue_generate_Data):
	global totalRound
	if continue_generate_Data:
		images=list(np.load(DATADIR+"/img.npy"))
		positions=list(np.load(DATADIR+"/pos.npy"))
		targets=list(np.load(DATADIR+"/tar.npy"))
		Yactions=list(np.load(DATADIR+"/Yactions.npy"))
		totalRound=list(np.load(DATADIR+'/totalRound.npy'))
		totalRound=totalRound[0]
	else:
		images=[]
		positions=[]
		targets=[]
		Yactions=[]
		totalRound=0
	return images,positions,targets,Yactions


if __name__=='__main__':
	generateData(15)