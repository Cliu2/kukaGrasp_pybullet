import os, inspect, pickle
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(os.path.dirname(currentdir))
os.sys.path.insert(0,parentdir)

from kukaGrasp_pybullet.util import utils
from kukaGrasp_pybullet import config
import argparse,atexit
import tensorflow as tf

class Train():
	def __init__(self,sess,parameters):
		self.sess=sess
		self.initAgent(parameters)

	def initAgent(self,parameters):
		trainerType=parameters['learner']
		agentModule=utils.dynamicallyImport(trainerType,['../agents'])
		agentClass=getattr(agentModule,trainerType)
		agent=agentClass(self.sess,parameters['network'],parameters['modelFileNames'],parameters['episodes'],parameters['lr'],
			parameters['decay'],parameters['imageDimension'],parameters['display'],parameters['cameraType'],parameters['cameraRandom'],
			parameters['objectRange'],parameters['networkDimension'],parameters['epochsPerTraining'],parameters['epochs'],parameters['verbose'])
		self.agent=agent
		
	def train(self):
		self.agent.learn()
		self.agent.saveTrainingResult()

def exit_handler():
	global train
	train.agent.saveTrainingResult()


if __name__=="__main__":
	con = tf.ConfigProto()
	con.gpu_options.allow_growth = True
	sess = tf.Session(config=con)

	global train
	train=Train(sess,config.settings)
	atexit.register(exit_handler)
	train.agent.loadModel("/root/project/pybullet3_lance/kukaGrasp_pybullet/models/20190220_Reward_DDPG_replayBuffer_actionScaled/model.ckpt")
	train.train()
