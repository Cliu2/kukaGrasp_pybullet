import tensorflow as tf
from tensorflow.python.keras.layers import Input, Conv2D, MaxPooling2D, Dropout, \
						Activation, Dense, concatenate, Flatten, RepeatVector, Reshape \
						,add
from tensorflow.python.keras.models import Model, load_model
from tensorflow.python.keras.optimizers import SGD, Adadelta
import numpy as np

class network():
	def __init__(self, lr=0.001, maxLearningEpochs=10000):
		self.lr=lr
		self.optimizer=Adadelta()
		self.buildLayers()
		self.epochs=maxLearningEpochs

	def buildLayers(self):
		imageInput=Input(shape=(48,48,3),name='imageInput')
		middleLayer=Conv2D(32, (3,3), activation='tanh')(imageInput)
		middleLayer=MaxPooling2D(pool_size=(4,4))(middleLayer)		
		middleLayer=Dropout(0.25)(middleLayer)
		middleLayer=Conv2D(16, (3,3), activation='tanh')(imageInput)
		middleLayer=MaxPooling2D(pool_size=(4,4))(middleLayer)
		middleLayer=Dropout(0.25)(middleLayer)		
		middleLayer=Flatten()(middleLayer)
		imageOutput=Dense(64,activation='tanh')(middleLayer)
		actionOutput=Dense(5,activation='sigmoid',name='actionOutput')(middleLayer)

		actionInput=Input(shape=(5,),name='actionInput')
		middleLayer=concatenate([imageOutput,actionInput], axis=1)
		middleLayer=Dense(64,activation='tanh')(middleLayer)
		middleLayer=Dense(32,activation='tanh')(middleLayer)
		rewardOutput=Dense(1,activation='sigmoid', name='rewardOutput')(middleLayer)
		model=Model(inputs=[imageInput,actionInput],outputs=[rewardOutput,actionOutput])
		model.compile(loss='binary_crossentropy', optimizer=self.optimizer)
		self.model=model

	def train(self,state,action,reward,idealAction):
		for i in range(len(action)):
			action[i]=[x/2+0.5 for x in action[i]]
			idealAction[i]=[x/2+0.5 for x in idealAction[i]]
		self.model.fit([state,action],[reward,idealAction],epochs=self.epochs,verbose=0)
		self.epochs=max(800,int(self.epochs*0.9))

	def getBestAction(self,state,actions=None):
		maxReward=None
		bestAction=None
		if actions!=None:
			for action in actions:
				reward,predictAction=self.model.predict([np.array([state]),np.array([action])])
				if maxReward==None or maxReward[0][0]<reward[0][0]:
					maxReward,bestAction=reward,[action]
		else:
			_,predictAction=self.model.predict([np.array([state]),np.array([[1,1,1,1,1]])])
			reward,_=self.model.predict([np.array([state]),np.array(predictAction)])
			bestAction=predictAction
			maxReward=reward
		bestAction[0]=[(x-0.5)*2 for x in bestAction[0]]
		#print(bestAction,maxReward)
		return bestAction,maxReward

	def saveModel(self,filepath,overwrite=True,include_optimizer=True):
		self.model.save(filepath,overwrite=overwrite,include_optimizer=include_optimizer)

	def loadModel(self,filepath):
		model=load_model(filepath)
		self.model=model

class possibilityNetwork():
	def __init__(self, imageDimension, actionDimension, rewardStepLength=0.5, discounting=0.9):
		self.imageDimension=imageDimension
		self.actionDimension=actionDimension
		self.buildModel()
		self.rewardStepLength=rewardStepLength
		self.discounting=discounting
		self.epochs=1
		self.action_space=None

	def buildModel(self):
		imageInput=Input(shape=(self.imageDimension[0]*2,self.imageDimension[1],self.imageDimension[2]), name='imageInput')
		middleLayer=Conv2D(64, (6,6), strides=2, activation='relu',padding='same')(imageInput)
		middleLayer=MaxPooling2D(pool_size=(3,3))(middleLayer)
		for convlayer in range(3):
			middleLayer=Conv2D(64, (5,5) ,activation='relu',padding='same')(middleLayer)
		imageFeatures=MaxPooling2D(pool_size=(3,3))(middleLayer)
		imageFeatureShape=imageFeatures.shape

		actionInput=Input(shape=self.actionDimension)
		middleLayer=Dense(64, activation='relu')(actionInput)
		middleLayer=RepeatVector(imageFeatureShape[1]*imageFeatureShape[2])(middleLayer)
		middleLayer=Reshape((imageFeatureShape[1],imageFeatureShape[2],64))(middleLayer)

		middleLayer=concatenate([imageFeatures,middleLayer],axis=1)
		# for convlayer in range(7):
		# 	middleLayer=Conv2D(64, (3,3), activation='relu',padding='same')(middleLayer)
		# middleLayer=MaxPooling2D(pool_size=(2,2))(middleLayer)
		for convlayer in range(2):
			middleLayer=Conv2D(16, (3,3), strides=3, activation='relu',padding='same')(middleLayer)
		middleLayer=Flatten()(middleLayer)
		middleLayer=Dense(64, activation='relu')(middleLayer)
		middleLayer=Dense(64, activation='relu')(middleLayer)
		middleLayer=Dense(32, activation='relu')(middleLayer)
		rewardOutput=Dense(1, activation='linear', name='rewardOutput')(middleLayer)
		model=Model(inputs=[imageInput,actionInput], outputs=[rewardOutput])
		model.compile(loss='MSE', optimizer='Adadelta')
		self.model=model

	def train(self, state, action, reward):
		state,action,reward=np.array(state),np.array(action),np.array(reward)
		for i in range(len(reward)):
			reward[i]=(1-self.rewardStepLength)*self.predictReward(state[i],action[i]) \
						+ self.rewardStepLength*reward[i]
		"can be improved, add prediction on next state"
		self.model.train_on_batch([state,action],reward)

	def trainWithNextState(self,state,action,reward,nextState,actionSpace,breakpoints=None):
		state,action,reward,nextState=np.array(state),np.array(action),np.array(reward),np.array(nextState)
		target=[]
		# for i in range(len(reward)):
		# 	t=0
		# 	if breakpoints==None or (i+1) not in breakpoints:
		# 		t=(1-self.rewardStepLength)*self.predictReward(state[i],action[i]) \
		# 			+self.rewardStepLength*(reward[i]+self.predictReward(nextState[i],action[i+1]) \
		# 				* self.discounting)
		# 	else:
		# 		nextAction=self.getBestAction(nextState[i],actionSpace)
		# 		t=(1-self.rewardStepLength)*self.predictReward(state[i],action[i]) \
		# 			+ self.rewardStepLength*(reward[i])
		# 	target.append(t)
		# self.model.train_on_batch([state,action],target)
		"""a new method here-20181023"""
		target=list(reward)
		for i in range(len(reward)-1,-1,-1):
			if breakpoints==None or (i+1) not in breakpoints:
				target[i]=self.discounting*target[i+1]+target[i]
		self.model.fit([state,action],target,verbose=1,epochs=self.epochs)

	def trainSuccessFail(self,state,action,reward,utility,nextState):
		state,action,reward=np.array(state),np.array(action),np.array(reward)
		target=np.array(utility)
		# target=[]
		for i in range(len(reward)):
			# target.append(max(utility[i], \
			# 		(reward[i]+self.getUtility(nextState[i]))))
			target[i]=max(utility[i],self.predictReward(state[i],action[i]))
		target=np.array(target)
		self.model.fit([state,action],target,verbose=1,epochs=self.epochs)

	def getUtility(self,state):
		action=self.getBestAction(state,self.action_space)
		return self.predictReward(state,action)

	def predictReward(self, state, action):
		state,action=np.array(state),np.array(action)
		if len(state.shape)==3:
			state=np.array([state])
		if len(action.shape)==1:
			action=np.array([action])
		reward=self.model.predict([state,action])
		return reward[0][0]

	def predictRewardOnBatch(self,states,actions):
		states,actions=np.array(states),np.array(actions)
		reward=self.model.predict([states,actions])
		return reward[:,0]

	def getBestAction(self, state, actionSpace):
		#use CEM to get a best action based on the probability of success
		rank=lambda x:self.predictReward(state,x)
		actions=[]
		bestAction=actionSpace.sample()
		for i in range(64):
			actions.append(actionSpace.sample())
		rewards=list(self.predictRewardOnBatch([state for x in actions],actions))
		actions=[x for _,x in sorted(zip(rewards,actions),key=lambda x:x[0])]
		actions=np.array(actions[-6:])
		mean=np.mean(actions,axis=0)
		covariance=np.cov(actions,rowvar=0)
		while np.linalg.norm(bestAction-mean)>0.1:
			actions=[]
			bestAction=mean
			while len(actions)<64:
				action=np.random.multivariate_normal(mean,covariance)
				if actionSpace.contains(action):
					actions.append(action)
			rewards=list(self.predictRewardOnBatch([state for x in actions],actions))
			actions=[x for _,x in sorted(zip(rewards,actions),key=lambda x:x[0])]
			actions=np.array(actions[-6:])
			mean=np.mean(actions,axis=0)
			covariance=np.cov(actions,rowvar=0)
		return bestAction

	def saveModel(self,filepath,overwrite=True,include_optimizer=True):
		self.model.save(filepath,overwrite=overwrite,include_optimizer=include_optimizer)
	
	def loadModel(self,filepath):
		model=load_model(filepath)
		self.model=model	
				
