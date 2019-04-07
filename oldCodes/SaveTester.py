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



sess=tf.Session()
with sess:
	i=Input((2,))
	h=Dense(64)(i)
	o=Dense(1)(h)
	model=Model(inputs=i,outputs=o)
	model.compile(optimizer='AdaDelta',loss='MSE')
	sess.run(tf.global_variables_initializer())
	for i in range(10):
		result=model.fit(np.array([[1,2]]),np.array([3]))
	tf.summary.merge_all()
	writer = tf.summary.FileWriter("logs/", sess.graph)
	saver=tf.train.Saver()
	saver.save(sess,'/root/project/pybullet3_lance/kukaGrasp_pybullet/models/20190122_model/model.ckpt')