import os, inspect, pickle
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(os.path.dirname(currentdir))
os.sys.path.insert(0,parentdir)
from kukaGrasp_pybullet.networks.NeuralNetwork import GraspNetwork
import tensorflow as tf
from tensorflow.python.keras.models import Model
from tensorflow.python.keras import Input
from tensorflow.python.keras.layers import Dense,Conv2D,MaxPooling2D,RepeatVector,Reshape,Add,Flatten,Lambda
from operator import mul
from functools import reduce
import numpy as np

class GoogleCNN(GraspNetwork):
	def buildNetwork(self,imageDimension,actionDimension,outputDimension,rewardScale,optimizer,loss):
		mid,half=((rewardScale[0]+rewardScale[1])/2,(rewardScale[1]-rewardScale[0])/2)
		imageInput=Input(shape=imageDimension,name='ImageInput')
		hiddenLayer=Conv2D(64,(6,6),strides=2,activation='relu',padding='same')(imageInput)
		hiddenLayer=MaxPooling2D(pool_size=(3,3))(hiddenLayer)
		for convLayer in range(6):
			hiddenLayer=Conv2D(64,(5,5),activation='relu',padding='same')(hiddenLayer)
		imageFeatures=MaxPooling2D(pool_size=(3,3))(hiddenLayer)

		actionInput=Input(shape=actionDimension,name='ActionInput')
		hiddenLayer=Dense(64,activation='relu')(actionInput)
		hiddenLayer=RepeatVector(reduce(mul,imageFeatures.shape[1:-1]))(hiddenLayer)
		actionFeatures=Reshape(imageFeatures.shape[1:])(hiddenLayer)

		hiddenLayer=Add()([imageFeatures,actionFeatures])
		for convLayer in range(6):
			hiddenLayer=Conv2D(64,(3,3),activation='relu',padding='same')(hiddenLayer)
		hiddenLayer=MaxPooling2D(pool_size=(2,2))(hiddenLayer)
		for convLayer in range(3):
			hiddenLayer=Conv2D(64,(3,3),activation='relu',padding='same')(hiddenLayer)
		hiddenLayer=Flatten()(hiddenLayer)
		hiddenLayer=Dense(64,activation='relu')(hiddenLayer)
		hiddenLayer=Dense(64,activation='relu')(hiddenLayer)
		hiddenLayer=Dense(1,activation='tanh')(hiddenLayer)
		valueOutput=Lambda(lambda x: x*half+mid)(hiddenLayer)

		model=Model(inputs=[imageInput,actionInput],outputs=valueOutput)
		model.compile(loss=loss,optimizer=optimizer)
		self.model=model

	def getAction(self,X,actionSpace,threshold=0.8,method='CEM',steps=100):
		if hasattr(self,method):
			m=getattr(self,method)
		else:
			raise NameError("NO such method: "+method)
		result=[]
		for state in X:
			result.append(m(state,actionSpace,threshold,steps))
		return np.array(result)



	def CEM(self,state,actionSpace,threshold,steps=100):
		actions=[actionSpace.sample() for i in range(64)]
		best=0.0
		prob=self.predict([np.array([state for a in actions]),
											np.array(actions)])
		pairs=np.c_[prob,actions]
		pairs=pairs[pairs[:,0].argsort()]
		r,bestAction=pairs[-1][0],pairs[-1][1:]
		step=0
		while(r-best>0.001 and step<steps):
			actions=np.array(actions[-6:])
			mean=np.mean(actions,axis=0)
			covariance=np.cov(actions,rowvar=0)
			best=r
			actions=[]
			while len(actions)<64:
				action=np.random.multivariate_normal(mean,covariance)
				if actionSpace.contains(action): actions.append(action)
			prob=self.predict([np.array([state for a in actions]),
											np.array(actions)])
			pairs=np.c_[prob,actions]
			pairs=pairs[pairs[:,0].argsort()]
			r=pairs[-1][0]
			if r>best: bestAction=pairs[-1][1:]
			else:break
			step+=1
		return bestAction




if __name__=='__main__':
	print("testing the class GoogleCNN...")
	sess=tf.Session()
	imageDimension=(472,472,3)
	actionDimension=(4,)
	outputDimension=(1,)
	g=GoogleCNN(sess,imageDimension,actionDimension,outputDimension)
	print(g.model.summary())
	print("the model is good to use")
