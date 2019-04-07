import os, inspect, pickle
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(os.path.dirname(currentdir))
os.sys.path.insert(0,parentdir)

from kukaGrasp_pybullet.environments.kuka_diverse_object_gym_env import KukaDiverseObjectEnv
import random
import os
from gym import spaces
import time
import pybullet as p
import kuka
import numpy as np
import pybullet_data
import pdb
import distutils.dir_util
import glob
from pkg_resources import parse_version
import gym
import math

class LanceKukaDiverseObjectEnv(KukaDiverseObjectEnv):
	"""
	Inherit from KukaDiverseObjectEnv, add softReset method:
	only reset position, object types not changed
	"""
	def __init__(self,
				 urdfRoot=pybullet_data.getDataPath(),
				 actionRepeat=80,
				 isEnableSelfCollision=True,
				 renders=False,
				 isDiscrete=False,
				 maxSteps=1000,
				 dv=0.06,
				 removeHeightHack=False,
				 blockRandom=0.3,
				 cameraRandom=0,
				 width=48,
				 height=48,
				 numObjects=1,
				 isTest=False,
				 cameraType=4):
		"""Initializes the KukaDiverseObjectEnv. 

		Args:
			urdfRoot: The diretory from which to load environment URDF's.
			actionRepeat: The number of simulation steps to apply for each action.
			isEnableSelfCollision: If true, enable self-collision.
			renders: If true, render the bullet GUI.
			isDiscrete: If true, the action space is discrete. If False, the
			action space is continuous.
			maxSteps: The maximum number of actions per episode.
			dv: The velocity along each dimension for each action.
			removeHeightHack: If false, there is a "height hack" where the gripper
			automatically moves down for each action. If true, the environment is
			harder and the policy chooses the height displacement.
			blockRandom: A float between 0 and 1 indicated block randomness. 0 is
			deterministic.
			cameraRandom: A float between 0 and 1 indicating camera placement
			randomness. 0 is deterministic.
			width: The image width.
			height: The observation image height.
			numObjects: The number of objects in the bin.
			isTest: If true, use the test set of objects. If false, use the train
			set of objects.
		"""

		self._isDiscrete = isDiscrete
		self._timeStep = 1./240.
		self._urdfRoot = urdfRoot
		self._actionRepeat = actionRepeat
		self._isEnableSelfCollision = isEnableSelfCollision
		self._observation = []
		self._envStepCounter = 0
		self._renders = renders
		self._maxSteps = maxSteps
		self.terminated = 0
		self._cam_dist = 1.3
		self._cam_yaw = 180 
		self._cam_pitch = -40
		self._dv = dv
		self._p = p
		self._removeHeightHack = removeHeightHack
		self._blockRandom = blockRandom
		self._cameraRandom = cameraRandom
		self._width = width
		self._height = height
		self._numObjects = numObjects
		self._isTest = isTest
		self._cameraType = cameraType

		if self._renders:
			self.cid = p.connect(p.SHARED_MEMORY)
			if (self.cid<0):
				self.cid = p.connect(p.GUI)
			p.resetDebugVisualizerCamera(1.3,180,-41,[0.52,-0.2,-0.33])
		else:
			self.cid = p.connect(p.DIRECT)
		self._seed()

		if (self._isDiscrete):
			if self._removeHeightHack:
				self.action_space = spaces.Discrete(9)
			else:
				self.action_space = spaces.Discrete(7)
		else:
			self.action_space = spaces.Box(low=-1, high=1, shape=(3,))	# dx, dy, da
			if self._removeHeightHack:
				self.action_space = spaces.Box(low=-1,
											 high=1,
											 shape=(4,))	# dx, dy, dz, da
		self.viewer = None

	def _reset(self):
		"""Environment reset called at the beginning of an episode.
		"""
		# Set the camera settings.
		# look = [0.23, 0.2, 0.54]
		look=[0.5,0.1,0.0]
		distance = 2.4
		# pitch = -56 + self._cameraRandom*np.random.uniform(-3, 3)
		# yaw = 245 + self._cameraRandom*np.random.uniform(-3, 3)
		pitch=-34
		yaw=90
		roll = 0
		self._view_matrix = p.computeViewMatrixFromYawPitchRoll(
			look, distance, yaw, pitch, roll, 2)
		fov = 20. + self._cameraRandom*np.random.uniform(-2, 2)
		aspect = self._width / self._height
		near = 0.01
		far = 10
		self._proj_matrix = p.computeProjectionMatrixFOV(
			fov, aspect, near, far)

		self._attempted_grasp = False
		self._env_step = 0
		self.terminated = 0

		p.resetSimulation()
		p.setPhysicsEngineParameter(numSolverIterations=150)
		p.setTimeStep(self._timeStep)
		p.loadURDF(os.path.join(self._urdfRoot,"plane.urdf"),[0,0,-1])

		p.loadURDF(os.path.join(self._urdfRoot,"table/table.urdf"), 0.5000000,0.00000,-.820000,0.000000,0.000000,0.0,1.0)
				
		p.setGravity(0,0,-10)
		self._kuka = kuka.Kuka(urdfRootPath=self._urdfRoot, timeStep=self._timeStep)
		self._envStepCounter = 0
		p.stepSimulation()

		# reset closest distance
		self.lastClosestDistance=None

		# Choose the objects in the bin.
		self.urdfList = self._get_random_object(
			self._numObjects, self._isTest)
		self._objectUids = self.record_and_place_objects(self.urdfList)
		self._observation = self._get_observation()		
		self.lastClosestDistance=None
		self._reward()
		return np.array(self._observation)

	def _soft_reset(self):
		"""
		Environment reset called at the beginning of an episode.
		"""
		# Set the camera settings.
		look = [0.23, 0.2, 0.54]
		distance = 1.
		pitch = -56 + self._cameraRandom*np.random.uniform(-3, 3)
		yaw = 245 + self._cameraRandom*np.random.uniform(-3, 3)
		roll = 0
		self._view_matrix = p.computeViewMatrixFromYawPitchRoll(
			look, distance, yaw, pitch, roll, 2)
		fov = 20. + self._cameraRandom*np.random.uniform(-2, 2)
		aspect = self._width / self._height
		near = 0.01
		far = 10
		self._proj_matrix = p.computeProjectionMatrixFOV(
			fov, aspect, near, far)
		
		self._attempted_grasp = False
		self._env_step = 0
		self.terminated = 0

		p.resetSimulation()
		p.setPhysicsEngineParameter(numSolverIterations=150)
		p.setTimeStep(self._timeStep)
		p.loadURDF(os.path.join(self._urdfRoot,"plane.urdf"),[0,0,-1])
		
		p.loadURDF(os.path.join(self._urdfRoot,"table/table.urdf"), 0.5000000,0.00000,-.820000,0.000000,0.000000,0.0,1.0)
				
		p.setGravity(0,0,-10)
		self._kuka = kuka.Kuka(urdfRootPath=self._urdfRoot, timeStep=self._timeStep)
		self._envStepCounter = 0
		p.stepSimulation()

		# reset closest distance
		self.lastClosestDistance=None

		# Choose the objects in the bin.
		self._objectUids = self.place_objects(self.urdfList)
		self._observation = self._get_observation()
		self._reward()
		return np.array(self._observation)

	def _get_observation(self):
		"""Return the observation as an image.
		"""
		img_arr = p.getCameraImage(width=self._width,
											height=self._height,
											viewMatrix=self._view_matrix,
											projectionMatrix=self._proj_matrix)
		rgb = img_arr[self._cameraType]	#3 for depth camera, 4 for segment camera
		# np_img_arr = np.reshape(rgb, (self._height, self._width, 4))
		channel=4 if self._cameraType==2 else 1
		np_img_arr = np.reshape(rgb, (self._height, self._width,channel))
		# return np_img_arr[:, :, :3]
		return np_img_arr if self._cameraType!=2 else np_img_arr[:,:,:3]

	def record_and_place_objects(self,urdfList):
		self.objConfig=[]
		objectUids = []
		for urdf_name in urdfList:
			xpos = 0.4 +self._blockRandom*random.random()
			ypos = self._blockRandom*(random.random()-.5)
			angle = np.pi/2 + self._blockRandom * np.pi * random.random()
			orn = p.getQuaternionFromEuler([0, 0, angle])
			urdf_path = os.path.join(self._urdfRoot, urdf_name)
			uid = p.loadURDF(urdf_path, [xpos, ypos, .15],
			[orn[0], orn[1], orn[2], orn[3]])
			self.objConfig.append([urdf_path,[xpos, ypos, .15],[orn[0], orn[1], orn[2], orn[3]]])
			objectUids.append(uid)
			# Let each object fall to the tray individual, to prevent object
			# intersection.
			for _ in range(500):
				p.stepSimulation()
		return objectUids

	def place_objects(self,urdfList):
		objectUids = []
		for a in self.objConfig:
			uid = p.loadURDF(a[0], a[1],a[2])
			objectUids.append(uid)
			for _ in range(500):
				p.stepSimulation()
		return objectUids

	def _reward(self):
		#override the reward method, adding reward for getting close to an object
		reward = 0
		# reward = -1 #give a cost for each step, hopefully will turn to short solution
		self._graspSuccess = 0
		armPos=np.array(self._kuka.getObservation()[0:3])
		for uid in self._objectUids:
			pos, _ = p.getBasePositionAndOrientation(uid)
			if pos[2] > 0.2:
				self._graspSuccess += 1
				reward = 100
				return reward
			pos=np.array(pos)
			distance=np.linalg.norm(armPos-pos)
			# print(distance)
		# the reward can be gained from getting closer to an object, in range [0,10]
		# if self.lastClosestDistance!=None:
		# 	reward+=100*(self.lastClosestDistance-closest)
		# 	self.lastClosestDistance=closest
		# else:
		# 	self.lastClosestDistance=closest
		# print("displacement:",[x-y for (x,y) in zip(armPos,pos)])
		# print("armPos",armPos)
		reward+=-(np.dot(np.array([30,30,30]),np.absolute(armPos-pos)))
		# reward+= (-10*distance)
		# print("reward",reward)
		# input()
		return reward

	def getPosition(self):
		pos=np.array(self._kuka.getObservation()[0:3])*1000
		pos[2]/=10
		return pos

	def getTarget(self):
		uid=self._objectUids[0]
		pos,ori=p.getBasePositionAndOrientation(uid)
		pos=np.array(pos)*1000
		pos[2]/=10
		return pos

	if parse_version(gym.__version__)>=parse_version('0.9.6'):
	
		reset=_reset
		softReset=_soft_reset

if __name__=='__main__':
	env=LanceKukaDiverseObjectEnv(renders=True)
	print(env.reset())
	input()