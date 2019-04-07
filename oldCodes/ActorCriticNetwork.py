#import libraries here
import numpy as np
import math
from keras.initializers import normal, identity
from keras.models import model_from_json, load_model
from keras.layers import Add,MaxPooling2D,Conv2D,Dense, Flatten, Input, merge, Lambda, Activation
from keras.models import Sequential, Model, load_model
from keras.optimizers import Adam,Adadelta
import keras.backend as K
import tensorflow as tf
from matplotlib import pyplot as plt
# from tensorflow.python.keras.layers import Input, Conv2D, MaxPooling2D, Dropout, \
# 						Activation, Dense, concatenate, Flatten, RepeatVector, Reshape \
# 						,add
# from tensorflow.python.keras.models import Model, load_model


class ActorNetwork():
	def __init__(self, sess, imageDimension, actionDimension, lr=0.1,rewardStepLength=0.01,critic=None):
		self.sess=sess
		self.imageDimension=imageDimension
		self.actionDimension=actionDimension
		self.rewardStepLength=rewardStepLength
		self.epochs=1
		self.action_space=None
		self.critic=critic
		self.lr=lr

		K.set_session(sess)

		self.model,self.weights,self.state,self.xyza=self.buildModel(imageDimension,actionDimension)
		# self.target_model,self.target_weights,self.target_state=self.buildModel(imageDimension,actionDimension)
		self.action_gradient=tf.placeholder(tf.float32,[None,actionDimension])
		# self.reward=tf.placeholder(tf.float32,[None,1])
		# origin code: self.params_grad=tf.gradients(self.model.output,self.weights,-self.action_gradient)
		self.params_grad=tf.gradients(tf.add(self.model.output,self.action_gradient),self.weights)
		# self.loss=tf.subtract(tf.constant(5000.0),self.reward)
		grads=zip(self.params_grad,self.weights)
		# self.optimize=tf.train.AdadeltaOptimizer(100).apply_gradients(grads)
		# self.optimize=tf.train.AdadeltaOptimizer().minimize(self.loss,var_list=[self.weights])
		self.sess.run(tf.initialize_all_variables())

	def buildModel(self, imageDimension, actionDimension):
		imageInput=Input(shape=(self.imageDimension[0]*2,self.imageDimension[1],self.imageDimension[2]), name='imageInput')
		self.imageInput=imageInput
		middleLayer=Conv2D(16, (16,16), strides=8, activation='relu',padding='same')(imageInput)
		self.displayLayer=middleLayer
		middleLayer=MaxPooling2D(pool_size=(16,16))(middleLayer)
		for convlayer in range(3):
			middleLayer=Conv2D(8, (8,8) ,activation='relu',padding='same')(middleLayer)
		middleLayer=MaxPooling2D(pool_size=(4,4))(middleLayer)
		middleLayer=Flatten()(middleLayer)
		middleLayer=Dense(64,activation='relu')(middleLayer)
		middleLayer=Dense(32,activation='relu')(middleLayer)
		middleLayer=Dense(32,activation='relu')(middleLayer)
		xyza=Dense(actionDimension,activation='tanh')(middleLayer)
		model=Model(input=imageInput,output=xyza)
		adam=Adadelta(self.lr)
		model.compile(loss='MSE',optimizer=adam)
		return model,model.trainable_weights, imageInput,xyza

	def displayImageFeatures(self,X,layer=None):
		if layer==None:layer=self.displayLayer
		val=self.sess.run(layer,feed_dict={
			self.imageInput:X
			})[0]
		for i in range(16):
			graph=val[:,:,i]
			plt.imshow(graph)
			plt.show()

	def train(self,states,action_grads):
		print("action_grads",action_grads)
		self.lastWeights=np.array(self.sess.run(self.weights))
		# print("lastWeights",self.lastWeights)
		temp=self.sess.run(self.optimize,feed_dict={
			self.state:states,
			self.action_gradient:action_grads
		})
		# print("modelOutput",self.model.output)
		# print("optimize",temp)
		# p_grad=np.array(self.sess.run(self.params_grad,feed_dict={self.action_gradient:action_grads,self.state:states}))
		# print("params_grad",p_grad)

		self.currentWeights=np.array(self.sess.run(self.weights))
		# print("weights",self.currentWeights.shape)
		diff=self.lastWeights-self.currentWeights
		# print("diff",diff[0][0][0])

		
		# input()

	def target_train(self):
		actor_weights=self.model.get_weights()
		actor_target_weights=self.target_model.get_weights()
		for i in range(len(actor_weights)):
			actor_target_weights[i]=self.rewardStepLength*actor_weights[i]+(1-self.rewardStepLength)*actor_target_weights[i]
		self.target_model.set_weights(actor_target_weights)

	def save(self,fileName):
		self.model.save(fileName)

	def load(self,fileName):
		self.model=load_model(fileName)

class CriticNetwork():
	def __init__(self,sess,imageDimension,actionDimension,rewardStepLength=0.01,lr=0.001):
		self.sess=sess
		self.rewardStepLength=rewardStepLength
		self.lr=lr
		self.actionDimension=actionDimension

		K.set_session(sess)

		self.model,self.action,self.state,self.ValueOutput=self.buildNetwork(imageDimension,actionDimension)
		# self.target_model,self.target_action,self.target_state=self.buildNetwork(imageDimension,actionDimension)
		self.action_grads=tf.gradients(self.model.output,self.action)
		self.sess.run(tf.initialize_all_variables())

	def gradients(self,states,actions):
		temp= self.sess.run(self.action_grads,feed_dict={
			self.state:states,
			self.action:actions
		})[0]
		# print(temp)
		return temp

	def target_train(self):
		critic_weights=self.model.get_weights()
		critic_target_weights=self.target_model.get_weights()
		for i in range(len(critic_weights)):
			critic_target_weights[i]=self.rewardStepLength*critic_weights[i]+(1-self.rewardStepLength)*critic_target_weights[i]
		self.target_model.set_weights(critic_target_weights)

	def buildNetwork(self,imageDimension,actionDimension):
		imageInput=Input(shape=(imageDimension[0]*2,imageDimension[1],imageDimension[2]), name='imageInput')
		actionInput=Input(shape=(actionDimension,),name='action_critic')
		middleLayer=Conv2D(16, (16,16), strides=8, activation='relu',padding='same')(imageInput)
		middleLayer=MaxPooling2D(pool_size=(16,16))(middleLayer)
		for convlayer in range(3):
			middleLayer=Conv2D(8, (8,8) ,activation='relu',padding='same')(middleLayer)
		middleLayer=MaxPooling2D(pool_size=(4,4))(middleLayer)
		middleLayer=Flatten()(middleLayer)
		middleLayer=Dense(64,activation='relu')(middleLayer)
		middleLayer=Dense(64,activation='tanh')(middleLayer)
		actionMiddleLayer=Dense(64,activation='linear')(actionInput)
		middleLayer=Add()([middleLayer,actionMiddleLayer])
		middleLayer=Dense(64,activation='relu')(middleLayer)
		middleLayer=Dense(32,activation='relu')(middleLayer)
		ValueOutput=Dense(1,activation='linear',name='value_output')(middleLayer)

		model=Model(input=[imageInput,actionInput],output=[ValueOutput])
		# adam=Adam(lr=self.lr)
		adam=Adadelta()
		model.compile(loss='MSE',optimizer=adam)
		return model,actionInput,imageInput,ValueOutput

	def save(self,fileName):
		self.model.save(fileName)

	def load(self,fileName):
		self.model=load_model(fileName)