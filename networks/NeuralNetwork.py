import tensorflow as tf
from tensorflow.python.keras.models import Model, load_model
import numpy as np

class Network():
	def fitModel(self, X, Y, epochs=1, verbose=0):		
		self.model.fit(X,Y,epochs=epochs,verbose=verbose)
		# print(Y[-10:])
		# print(self.predict(X)[-10:])

	def predict(self, X):
		return self.model.predict(X)

	def getAction(self,X,actionSpace,threshold=0.8,method='CEM',steps=100):
		raise NotImplementedError("method not implemented")

	def saveModel(self,filePath):
		saver=tf.train.Saver()
		saver.save(self.sess,filePath)

	def loadModel(self,filePath):
		saver=tf.train.Saver()
		saver.restore(self.sess,filePath)

	def getUtility(self,X,actionSpace):
		action=self.getAction(X,actionSpace)
		return self.predict([X,action])

class GraspNetwork(Network):
	def __init__(self,sess,imageDimension,actionDimension,outputDimension,
						rewardScale=None,optimizer='Adadelta',loss='MSE',lr=0.001):
		self.sess=sess
		self.lr=lr
		self.buildNetwork(imageDimension,actionDimension,outputDimension,rewardScale,optimizer,loss)		

	def buildNetwork(self,imageDimension,actionDimension,outputDimension,rewardScale,optimizer,loss):
		raise NotImplementedError("method not implemented")