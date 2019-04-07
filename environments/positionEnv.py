import os, inspect, pickle
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(os.path.dirname(currentdir))
workdir=os.path.dirname(currentdir)
os.sys.path.insert(0,parentdir)

from kukaGrasp_pybullet.environments.lance_kuka_diverse_env import LanceKukaDiverseObjectEnv
import pybullet as p
import numpy as np

class positionEnv(LanceKukaDiverseObjectEnv):
	def _reward(self):
		# #override the reward method, adding reward for getting close to an object
		# reward = 0
		# # reward = -1 #give a cost for each step, hopefully will turn to short solution
		self._graspSuccess = 0
		armPos=np.array(self._kuka.getObservation()[0:3])
		# closest=9999
		for uid in self._objectUids:
			pos, _ = p.getBasePositionAndOrientation(uid)
			if pos[2] > 0.2:
				self._graspSuccess += 1
		# 		reward = 500
		# 		return reward
		# 	pos=np.array(pos)
		# 	distance=np.linalg.norm(armPos-pos)
		# 	closest=min(distance,closest)
		# # the reward can be gained from getting closer to an object, in range [0,10]
		# if self.lastClosestDistance!=None:
		# 	reward+=100*(self.lastClosestDistance-closest)
		# 	self.lastClosestDistance=closest
		# else:
		# 	self.lastClosestDistance=closest
		# return reward
		pos=np.array(pos)
		return np.concatenate((armPos,pos))