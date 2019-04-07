import os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(os.path.dirname(currentdir))
os.sys.path.insert(0,parentdir)

from Learner import Learner
import numpy as np

class RewardLearner(Learner):
	def recordTargets(self,reward,info,targets):
		targets.append(reward)

	def getTrainTargets(self,states,actions,targets,succ,actionSpace):
		for i in range(len(targets)-1):
			currentState,nextState=states[i],states[i+1]
			targets[i]=targets[i]+self.decay*self.network.getUtility(np.array([nextState]),actionSpace)[0][0]


if __name__=='__main__':
	print("testing the class ProbabilityLearner...")
	import tensorflow as tf
	sess=tf.Session()
	learner=RewardLearner(sess,'ActorCriticDDPG','reward_DDPG',episodes=50,display=False)
	learner.loadModel("/root/project/pybullet3_lance/kukaGrasp_pybullet/models/20190122_reward_DDPG/model.ckpt")
	learner.learn()
	print("the model is good to use")
