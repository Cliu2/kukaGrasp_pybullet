import tensorflow as tf
from tensorflow.python.keras.models import Model
from tensorflow.python.keras import Input
from tensorflow.python.keras.layers import Dense,Conv2D,MaxPooling2D,Add,Flatten,Lambda,Concatenate
from tensorflow.python.keras.optimizers import Adam
# from matplotlib import pyplot as plt
import numpy as np

class CNN_for_sure():
	def __init__(self,sess,imageDimension,actionDimension):
		self.sess=sess
		self.network=self.buildNetwork(imageDimension,actionDimension)

	def buildNetwork(self,imageDimension,actionDimension):
		tf.keras.backend.set_session(self.sess)
		imageInput=Input(shape=imageDimension,name='ImageInput')
		self.imageInput=imageInput
		hiddenLayer=Conv2D(64,(6,6),strides=2,activation='relu',padding='same')(imageInput)
		hiddenLayer=MaxPooling2D(pool_size=(3,3))(hiddenLayer)
		for convLayer in range(6):
			hiddenLayer=Conv2D(64,(5,5),activation='relu',padding='same')(hiddenLayer)
		imageFeatures=MaxPooling2D(pool_size=(3,3))(hiddenLayer)

		for convLayer in range(6):
			hiddenLayer=Conv2D(64,(3,3),activation='relu',padding='same')(hiddenLayer)
		hiddenLayer=MaxPooling2D(pool_size=(2,2))(hiddenLayer)
		for convLayer in range(3):
			hiddenLayer=Conv2D(64,(3,3),activation='relu',padding='same')(hiddenLayer)
		hiddenLayer=Flatten()(hiddenLayer)
		hiddenLayer=Dense(64,activation='relu')(hiddenLayer)
		self.imageFeatureLayer=hiddenLayer
		hiddenLayer=Dense(64,activation='relu')(hiddenLayer)
		hiddenLayer=Dense(64,activation='relu')(hiddenLayer)
		hiddenLayer=Dense(64,activation='relu')(hiddenLayer)
		hiddenLayer=Dense(64,activation='relu')(hiddenLayer)
		output=Dense(actionDimension[0],activation='linear')(hiddenLayer)

		model=Model(inputs=imageInput,outputs=output)
		opti=Adam(lr=0.0001)
		model.compile(loss='MSE',optimizer=opti)
		self.model=model

	def train(self,images,actions,epochs=100,verbose=0):
		if type(actions)!=np.ndarray:
			actions=np.array(actions)
		if type(images)!=np.ndarray:
			images=np.array(images)
		self.model.fit(images,actions,epochs=epochs,verbose=verbose)

	def predict(self,images):
		if type(images)!=np.ndarray:
			images=np.array(images)
		p=self.model.predict(images)
		return p

	def printImageFeature(self,X):
		i=self.sess.run(self.imageFeatureLayer,feed_dict={
			self.imageInput:X
		})
		print(i)

	def saveModel(self,filePath):
		saver=tf.train.Saver()
		saver.save(self.sess,filePath)

	def loadModel(self,filePath):
		saver=tf.train.Saver()
		saver.restore(self.sess,filePath)

