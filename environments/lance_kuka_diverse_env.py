from .kuka_diverse_object_gym_env import KukaDiverseObjectEnv
import random
import os
from gym import spaces
import time
import pybullet as p
from . import kuka
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
	def _reset(self):
		state=super()._reset()
		self.lastClosestDistance=None
		self._reward()
		return state

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

		# Choose the objects in the bin.
		if not hasattr(self, 'urdfList'): #this modification ensures the objects are placed samely if softReset
			self.urdfList = self._get_random_object(
			self._numObjects, self._isTest)
			self._objectUids = self._randomly_place_objects(self.urdfList)
		self._observation = self._get_observation()
		return np.array(self._observation)

	def _reward(self):
		#override the reward method, adding reward for getting close to an object
		reward = 0
		# reward = -0.3 #give a cost for each step, hopefully will turn to short solution
		self._graspSuccess = 0
		armPos=np.array(self._kuka.getObservation()[0:3])
		closest=9999
		for uid in self._objectUids:
			pos, _ = p.getBasePositionAndOrientation(uid)
			if pos[2] > 0.2:
				self._graspSuccess += 1
				reward = 100
				return reward
			pos=np.array(pos)
			distance=np.linalg.norm(armPos-pos)
			closest=min(distance,closest)
		# the reward can be gained from getting closer to an object, in range [0,10]
		# if self.lastClosestDistance!=None:
		# 	reward+=10*(self.lastClosestDistance-closest)
		# 	self.lastClosestDistance=closest
		# else:
		# 	self.lastClosestDistance=closest
		return reward

	if parse_version(gym.__version__)>=parse_version('0.9.6'):
	
		reset=_reset
		softReset=_soft_reset