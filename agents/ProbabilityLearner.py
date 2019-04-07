import os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(os.path.dirname(currentdir))
os.sys.path.insert(0,parentdir)

from Learner import Learner
import numpy as np


class ProbabilityLearner(Learner):
	def recordTargets(self,reward,info,targets):
		targets.append(0)

	def getTrainTargets(self,states,actions,targets,succ,actionSpace):
		targets=[succ for x in targets]
		




if __name__=='__main__':
	print("testing the class ProbabilityLearner...")
	import tensorflow as tf
	sess=tf.Session()
	learner=ProbabilityLearner(sess,'GoogleCNN','probabiliy_pureCNN',episodes=50,display=False)
	learner.learn()
	print("the model is good to use")

