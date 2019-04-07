import os, inspect, pickle
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(os.path.dirname(currentdir))
os.sys.path.insert(0,parentdir)
from kukaGrasp_pybullet.networks.NeuralNetwork import Network,GraspNetwork
import tensorflow as tf
from tensorflow.python.keras.models import Model
from tensorflow.python.keras import Input
from tensorflow.python.keras.layers import Dense,Conv2D,MaxPooling2D,Add,Flatten,Lambda
from matplotlib import pyplot as plt
import numpy as np

class Actor(Network):
	def __init__(self,sess,imageInput,imageFeatureLayer,outputDimension,optimizer='AdadeltaOptimizer',loss='MSE',lr=0.01):
		self.sess=sess
		self.imageInput=imageInput
		self.lr=lr
		self.buildNetwork(imageFeatureLayer,outputDimension,optimizer,loss)

	def buildNetwork(self,imageFeatureLayer,outputDimension,optimizer,loss):
		with tf.variable_scope("actor"):
			hiddenLayer=Dense(64,activation='relu')(imageFeatureLayer)
			hiddenLayer=Dense(64,activation='relu')(hiddenLayer)
			hiddenLayer=Dense(32,activation='relu')(hiddenLayer)
			actionOutput=Dense(outputDimension[0],activation='tanh',name='action_output')(hiddenLayer)
		self.output=actionOutput

		self.actionGrad=tf.placeholder(tf.float32,[None,outputDimension[0]])
		network_params=tf.trainable_variables('actor')
		parameters_gradients=tf.gradients(actionOutput,network_params,-self.actionGrad)
		opti=getattr(tf.train,optimizer)(self.lr)
		self.optimizer=opti.apply_gradients(zip(parameters_gradients,network_params))
		
	def getAction(self,X):
		# X should be a np-array of state information, other parameters are not used in this network
		return self.sess.run(self.output,feed_dict={
			self.imageInput:X
		})

	def fitModelByGrad(self,state,actionGrad):
		# print(actionGrad[0])
		# input()
		self.sess.run(self.optimizer,feed_dict={
			self.imageInput:state,
			self.actionGrad:actionGrad
		})


class Critic(Network):
	def __init__(self,sess,imageInput,imageFeatureLayer,actionDimension,outputDimension,outputScale,lr=0.001,optimizer='Adadelta',loss='MSE'):
		self.sess=sess
		self.imageInput=imageInput
		self.scale=outputScale
		self.lr=lr
		self.buildNetwork(imageFeatureLayer,actionDimension,outputDimension,optimizer,loss)

	def buildNetwork(self,imageFeatureLayer,actionDimension,outputDimension,optimizer,loss):
		tf.keras.backend.set_session(self.sess)
		mid,half=((self.scale[0]+self.scale[1])/2,(self.scale[1]-self.scale[0])/2)
		with tf.variable_scope("critic"):
			actionInput=Input(shape=actionDimension,name='actionInput')
			hiddenLayer=Lambda(lambda x: x*256)(actionInput)
			hiddenLayer=Dense(64,activation='relu')(hiddenLayer)
			hiddenLayer=Dense(64,activation='relu')(hiddenLayer)
			hiddenLayer=Add()([hiddenLayer,imageFeatureLayer])
			hiddenLayer=Dense(64,activation='relu')(hiddenLayer)
			hiddenLayer=Dense(64,activation='relu')(hiddenLayer)
			hiddenLayer=Dense(32,activation='relu')(hiddenLayer)
			# hiddenLayer=Dense(outputDimension[0],activation='tanh',name='value_output')(hiddenLayer)
			# valueOutput=Lambda(lambda x: x*half+mid)(hiddenLayer)
			valueOutput=Dense(outputDimension[0],activation='linear',name='value_output')(hiddenLayer)
		self.output=valueOutput
		self.actionInput=actionInput

		self.actionGrad=tf.gradients(valueOutput,self.actionInput)
		model=Model(inputs=[self.imageInput,actionInput],outputs=valueOutput)
		opti=getattr(tf.keras.optimizers,optimizer)(lr=0.0000000001)
		self.optimizer=opti
		model.compile(loss=loss,optimizer=opti)
		self.model=model

	def getActionGrad(self,state,action):
		return self.sess.run(self.actionGrad,feed_dict={
				self.imageInput:state,
				self.actionInput:action
		})

class ActorCriticDDPG(GraspNetwork):
	def buildNetwork(self,imageDimension,actionDimension,outputDimension,rewardScale,optimizer,loss):
		with tf.variable_scope("imageProcess"):
			imageInput=Input(shape=imageDimension,name='imageInput')
			hiddenLayer=Conv2D(64,(6,6),strides=2,activation='relu',padding='same')(imageInput)
			hiddenLayer=MaxPooling2D(pool_size=(3,3))(hiddenLayer)
			for convLayer in range(6):
				hiddenLayer=Conv2D(64,(5,5),activation='relu')(hiddenLayer)
			hiddenLayer=MaxPooling2D(pool_size=(3,3))(hiddenLayer)
			for convLayer in range(6):
				hiddenLayer=Conv2D(64,(3,3),activation='relu',padding='same')(hiddenLayer)
			hiddenLayer=MaxPooling2D(pool_size=(2,2))(hiddenLayer)
			for convLayer in range(3):
				hiddenLayer=Conv2D(64,(3,3),activation='relu',padding='same')(hiddenLayer)
			self.displayLayer=hiddenLayer
			hiddenLayer=Flatten()(hiddenLayer)
			imageFeatureLayer=Dense(64,activation='relu')(hiddenLayer)
		self.imageFeatureLayer=imageFeatureLayer
		self.imageInput=imageInput

		actor=Actor(self.sess,imageInput,imageFeatureLayer,actionDimension,optimizer+'Optimizer',loss,self.lr)
		critic=Critic(self.sess,imageInput,imageFeatureLayer,actionDimension,outputDimension,rewardScale,self.lr,optimizer,loss)
		self.actor=actor
		self.critic=critic
		self.sess.run(tf.global_variables_initializer())

	def getAction(self,X,actionSpace):
		return self.actor.getAction(X)

	def fitModel(self,X,Y,epochs=1,verbose=0,action=False):
		# print("Y:",Y)
		states,actions=X[0],X[1]
		# self.critic.fitModel(X,Y,epochs,verbose)
		self.critic.fitModel(X,Y,1,verbose)
		
		if action:
			acts=self.actor.getAction(states)
			totalR=sum(self.predict([states,acts]))/len(acts)
			print("before train actor")
			print(totalR)
			
			for epoch in range(epochs):		
				acts=self.actor.getAction(states)	
				actionGrads=self.critic.getActionGrad(states,acts)[0]
				self.actor.fitModelByGrad(states,actionGrads)

			print('after train actor')
			acts=self.actor.getAction(states)
			totalR=sum(self.predict([states,acts]))/len(acts)
			print(totalR)
			# input()

	def predict(self,X):
		return self.critic.predict(X)

	def displayImageFeatures(self,X,layer=None):
		if layer==None:layer=self.displayLayer
		val=self.sess.run(layer,feed_dict={
			self.imageInput:X
			})[0]
		for i in range(64):
			graph=val[:,:,i]
			plt.imshow(graph)
			plt.show()

	def loadModel(self,filePath):
		saver=tf.train.Saver()
		saver.restore(self.sess,filePath)
		# self.critic.optimizer=getattr(tf.keras.optimizers,'Adadelta')(lr=1.0)
		# self.critic.model.compile(loss='MSE',optimizer=self.critic.optimizer)
		# self.sess.run(tf.variables_initializer(self.critic.optimizer.variables()))


if __name__=='__main__':
	sess=tf.Session()
	ddpg=ActorCriticDDPG(sess,(472,472,3),(4,),(1,))
	print("success")