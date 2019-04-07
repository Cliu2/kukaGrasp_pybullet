import os, inspect, pickle
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(os.path.dirname(currentdir))
os.sys.path.insert(0,parentdir)

from kukaGrasp_pybullet.networks.QLearnNetwork import possibilityNetwork
from tensorflow.python.keras.layers import Input, Conv2D, MaxPooling2D, Dropout, \
						Activation, Dense, concatenate, Flatten, RepeatVector, Reshape \
						,add
from tensorflow.python.keras.models import Model, load_model
from tensorflow.python.keras.optimizers import SGD, Adadelta
import numpy as np
from tensorflow.python.keras.callbacks import TensorBoard

def f(x):
	return 2*x+3


imageInput=Input(shape=(1,), name='imageInput')
middleLayer=Dense(64, activation='relu')(imageInput)
middleLayer=Dense(32, activation='relu')(middleLayer)
rewardOutput=Dense(1, activation='linear', name='rewardOutput')(middleLayer)
model=Model(inputs=[imageInput], outputs=[rewardOutput])
model.compile(loss='MSE', optimizer='Adadelta')

trainX=[]
trainY=[]
for i in range(50):
	x=np.random.random()*1000
	y=f(x)
	trainX.append(x)
	trainY.append(y)

	model.fit(np.array(trainX),np.array(trainY),verbose=1,epochs=10,callbacks=[TensorBoard(log_dir='../log')])

testData=[]
testY=[]
for i in range(1000):
	x=np.random.random()*1000
	y=f(x)
	p_y=model.predict(np.array([x]))[0]
	print(y," - ",p_y)
	testData.append(x)
	testY.append(y)

result=model.evaluate(testData,testY)
input()
print(result)
input()