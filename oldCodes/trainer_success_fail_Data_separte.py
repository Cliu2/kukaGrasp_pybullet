import os, inspect, pickle
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(os.path.dirname(currentdir))
os.sys.path.insert(0,parentdir)

from kukaGrasp_pybullet.environments.kuka_diverse_object_gym_env import KukaDiverseObjectEnv
from kukaGrasp_pybullet.environments.lance_kuka_diverse_env import LanceKukaDiverseObjectEnv
import tensorflow as tf
<<<<<<< HEAD
=======
from keras.layers import merge
>>>>>>> 2e204aa97a1307b8ba9026a61746a0b8a27a5e2f
from tensorflow import keras
import numpy as np
from kukaGrasp_pybullet.networks.QLearnNetwork import possibilityNetwork
import atexit
import math,random

<<<<<<< HEAD
import cv2
import sys
from pylibfreenect2 import Freenect2, SyncMultiFrameListener
from pylibfreenect2 import FrameType, Registration, Frame
from pylibfreenect2 import createConsoleLogger, setGlobalLogger
from pylibfreenect2 import LoggerLevel

MODEL_FILE_NAME="20181112_180rounds.h5"
MAXTRAIL=180
=======
MODEL_FILE_NAME="20181029_successfail_trainer_dr0p9.h5"
MAXTRAIL=5000
>>>>>>> 2e204aa97a1307b8ba9026a61746a0b8a27a5e2f
DISCOUNTING_RATE=0.9
WIDTH,HEIGHT=512,512 #set resolution of camera
CHANNEL=3
SUCCESS_REWARD=500
MAX_DATA_SIZE=1000
SUCCESS_RATE_HISTORY=[]

<<<<<<< HEAD
listener = None
registration = None
frames = None
registered = Frame(512, 424, 4)
undistorted = Frame(512, 424, 4)
fn = Freenect2()

def open_kinect():
    try:
        from pylibfreenect2 import OpenGLPacketPipeline
        pipeline = OpenGLPacketPipeline()
    except:
        try:
            from pylibfreenect2 import OpenCLPacketPipeline
            pipeline = OpenCLPacketPipeline()
        except:
            from pylibfreenect2 import CpuPacketPipeline
            pipeline = CpuPacketPipeline()
    print("Packet pipeline:", type(pipeline).__name__)

    # Create and set logger
    logger = createConsoleLogger(LoggerLevel.Debug)
    setGlobalLogger(logger)

    global fn
    num_devices = fn.enumerateDevices()
    if num_devices == 0:
        print("No device connected!")
        sys.exit(1)

    serial = fn.getDeviceSerialNumber(0)
    device = fn.openDevice(serial, pipeline=pipeline)

    global listener
    listener = SyncMultiFrameListener(FrameType.Color | FrameType.Ir | FrameType.Depth)

    # Register listeners
    device.setColorFrameListener(listener)
    device.setIrAndDepthFrameListener(listener)

    device.start()

    # NOTE: must be called after device.start()
    global registration
    registration = Registration(device.getIrCameraParams(),
                                device.getColorCameraParams())


def get_frame():
    global listener
    global registration
    global frames
    global registered
    global undistorted

    frames = listener.waitForNewFrame()

    color = frames["color"]
    ir = frames["ir"]
    depth = frames["depth"]

    registration.apply(color, depth, undistorted, registered,
                       None,
                       None)

    color_arr = cv2.resize(color.asarray(), (int(1920 / 3), int(1080 / 3)))
    ir_arr = ir.asarray()
    depth_arr = depth.asarray()
    registered_arr = registered.asarray(np.uint8)

    return color_arr, ir_arr, depth_arr, registered_arr


=======
>>>>>>> 2e204aa97a1307b8ba9026a61746a0b8a27a5e2f
def exit_handler():
	try:
		nw.saveModel("../models/"+MODEL_FILE_NAME)
		print("model saved as '",MODEL_FILE_NAME,"', exiting...")
		with open("../logs/"+MODEL_FILE_NAME[0:8]+"_successRateHistory.pkl", "wb") as f:  # Python 3: open(..., 'wb')
				pickle.dump([SUCCESS_RATE_HISTORY],f)
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
<<<<<<< HEAD
		removeHeightHack=True,width=WIDTH,height=HEIGHT,cameraRandom=1)
=======
		removeHeightHack=True,width=WIDTH,height=HEIGHT)
>>>>>>> 2e204aa97a1307b8ba9026a61746a0b8a27a5e2f

	nw.action_space=environment.action_space
	return environment,nw

def naiveHuresticAction():
	dx, dy, dz, da = environment.action_space.sample()
	if np.random.random() < 0.6:
		dz = -1
	action = [dx, dy, dz, da]
	return action

if __name__=="__main__":
<<<<<<< HEAD

	environment,nw=initEnvironment()

	trail=0
	last100success=[]
=======
	environment,nw=initEnvironment()

	trail=0
>>>>>>> 2e204aa97a1307b8ba9026a61746a0b8a27a5e2f
	success=0
	nw.rewardStepLength=0.5
	successData,failData=None,None
	while trail<MAXTRAIL:
		environment._numObjects=random.randint(1,9)	#randomize number of obejcts
		initState=environment.reset()
		state=initState
		statesForTrain,actions,rewards,nextStates=[],[],[],[]
		done,step=False,0		
		while not done and step<20:
			statesForTrain.append(list(initState)+list(state))
			action=None
<<<<<<< HEAD
			if np.random.random()< max(0.2,0.8/(1+0.001*trail)): # some naive hurestic
=======
			if np.random.random()< max(0.3,0.8/(1+0.001*trail)): # some naive hurestic
>>>>>>> 2e204aa97a1307b8ba9026a61746a0b8a27a5e2f
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
<<<<<<< HEAD
		if trail>100:
			last100success.pop(0)
		if (rewards[-1]==SUCCESS_REWARD):
			last100success.append(1)
		else:
			last100success.append(0)
		print("trail",trail, (rewards[-1]==SUCCESS_REWARD))
		# print("rewards",rewards)
		# print(actions)
		if trail%10==0:
			rate=len([x for x in last100success if x==1])/100 \
				if trail>100 else success/trail
			print("grasp success rate (last 100 tries):",rate)
			SUCCESS_RATE_HISTORY.append(rate)
=======
		print("trail",trail, (rewards[-1]==SUCCESS_REWARD))
		# print("rewards",rewards)
		if trail%10==0:
			print("grasp success rate:",success/trail)
			SUCCESS_RATE_HISTORY.append(success/trail)
>>>>>>> 2e204aa97a1307b8ba9026a61746a0b8a27a5e2f
			
		if trail%10==0:
			data=list(successData) if successData!=None else list(failData)
			for i in range(5):
<<<<<<< HEAD
				data[i]=(list(random.sample(list(successData[i]),int(len(successData[i])*0.8))) if successData!=None else []) + \
						(list(random.sample(list(failData[i]),int(len(failData[i])*0.5))) if failData!=None else [])

			nw.epochs=max(int(50/(1+1/15*trail)),25)
=======
				data[i]=(list(successData[i]) if successData!=None else []) + \
						(list(failData[i]) if failData!=None else [])

			nw.epochs=max(int(50/(1+1/15*trail)),20)
>>>>>>> 2e204aa97a1307b8ba9026a61746a0b8a27a5e2f
			nw.trainSuccessFail(data[0],data[1],data[2],data[3],data[4])
		#"""

		
