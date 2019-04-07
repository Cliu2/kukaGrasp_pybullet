import tensorflow as tf
from tensorflow.python.keras.models import Model
from tensorflow.python.keras import Input
from tensorflow.python.keras.layers import Dense,Conv2D,MaxPooling2D,Add,Flatten,Lambda,Concatenate
# from matplotlib import pyplot as plt
import numpy as np
def plotDot(m_origin,pos,value):
	m=np.copy(m_origin)
	pos1=(np.floor(pos[0]),np.floor(pos[1]))
	pos2=(np.ceil(pos[0]),np.floor(pos[1]))
	pos3=(np.floor(pos[0]),np.ceil(pos[1]))
	pos4=(np.ceil(pos[0]),np.ceil(pos[1]))
	if pos[0]==int(pos[0]) and pos[1]==int(pos[1]):
		m[(int(pos[0]),int(pos[1]))]+=np.array(value)
	elif pos[0]==int(pos[0]):
		pos1=(int(pos1[0]),int(pos1[1]))
		pos3=(int(pos3[0]),int(pos3[1]))
		m[pos1]+=(value*abs(pos3[1]-pos[1]))
		m[pos3]+=(value*abs(pos1[1]-pos[1]))
	elif pos[1]==int(pos[1]):
		pos1=(int(pos1[0]),int(pos1[1]))
		pos2=(int(pos2[0]),int(pos2[1]))
		m[pos1]+=(value*abs(pos2[0]-pos[0]))
		m[pos2]+=(value*abs(pos1[0]-pos[0]))
	else:
		pos1=(int(pos1[0]),int(pos1[1]))
		pos2=(int(pos2[0]),int(pos2[1]))
		pos3=(int(pos3[0]),int(pos3[1]))
		pos4=(int(pos4[0]),int(pos4[1]))
		m[pos1]+=(value*abs(pos4[0]-pos[0])*abs(pos4[1]-pos[1]))
		m[pos2]+=(value*abs(pos3[0]-pos[0])*abs(pos3[1]-pos[1]))
		m[pos3]+=(value*abs(pos2[0]-pos[0])*abs(pos2[1]-pos[1]))
		m[pos4]+=(value*abs(pos1[0]-pos[0])*abs(pos1[1]-pos[1]))

	return m

def genMap(pos,target):
	m=np.zeros((300,300,3))
	m=plotDot(m,pos,np.array([0.0,0.0,1.0]))
	m=plotDot(m,target,np.array([1.0,0.0,0.0]))
	return m

# imageFeatureLayer=Input(shape=(2,2,),name='image_Feature')
imageFeatureLayer=Input(shape=(300,300,3,),name='image_Feature')
for layer in range(10):
	i=Conv2D(16,(10,10),strides=5,activation='relu')(imageFeatureLayer)
	i=MaxPooling2D(pool_size=(10,10))(i)
i=Conv2D(8,(3,3),strides=3,activation='relu')(imageFeatureLayer)
i=MaxPooling2D(pool_size=(2,2))(i)
i=Flatten()(imageFeatureLayer)
i=Dense(64,activation='relu')(i)

h=Dense(32,activation='relu',name='critic_h1')(i)
c_a=Input(shape=(2,),name='critic_action_input')
ah=Dense(32,activation='relu',name='critic_a1')(c_a)
h=Add(name='critic_merge')([ah,h])
h=Dense(32,activation='relu',name='critic_h2')(h)
reward=Dense(1,activation='linear',name='critic_output')(h)
r_grad=tf.gradients(reward,c_a,name='reward_grad')
y_input=tf.placeholder(tf.float32,[None,1],name='critic_reward_input')
cost = tf.reduce_mean(tf.square(y_input - reward),name='critic_loss')
c_optimizer = tf.train.AdamOptimizer(0.001).minimize(cost)

with tf.variable_scope('actor'):
	h1=Dense(32,activation='relu',name="actor_h1")(i)
	h1=Dense(32,activation='relu',name="actor_h2")(h1)
	h1=Dense(32,activation='relu',name="actor_h3")(h1)
	action=Dense(2,activation='linear',name="actor_output")(h1)
net=tf.trainable_variables('actor')
in_grad=tf.placeholder(tf.float32,[None,2],name="actor_inputGrad")
a_grad=tf.gradients(action,net,-in_grad,name='actor_actionGrad')
a_optimizer = tf.train.AdamOptimizer(0.001).apply_gradients(zip(a_grad,net))
a_input=tf.placeholder(tf.float32,[None,2],name='actor_action_input')
cost_a=tf.reduce_mean(tf.square(a_input-action))
a_optimizer2 = tf.train.AdamOptimizer(0.0001).minimize(cost_a)


sess=tf.Session()
sess.run(tf.global_variables_initializer())

saver=tf.train.Saver()
# saver.restore(sess,'/root/project/pybullet3_lance/kukaGrasp_pybullet/models/20190328_test_300.ckpt')

def calUtility(tars,poss,maps,acts,rews,nposs,done):
	util=list(rews)
	if done:
		loop=len(rews)-2
		util[-1]=np.array([util[-1]])
	else:
		loop=len(rews)-1

	for i in range(loop,-1,-1):
		m=genMap(tars[i],nposs[i])
		bestAct=sess.run(action,feed_dict={
			imageFeatureLayer:np.array([m])
			})
		u=util[i]+0.99*sess.run(reward,feed_dict={
			imageFeatureLayer:np.array([m]),
			c_a:bestAct
			})[0][0]
		util[i]=np.array([u])

	return util


def run(max_step=15,showRes=False,randAct=False):
	tars,poss,maps,acts,rews,nposs=[],[],[],[],[],[]
	tar=(np.random.rand(1,2)*299)[0]
	pos=(np.random.rand(1,2)*299)[0]
	done=False
	success=False
	step=0
	while not done and step<max_step:
		step+=1
		m=genMap(pos,tar)
		if randAct:
			act=(np.random.rand(1,2)*2-1)
			temp=pos+act[0]
			while temp[0]<0 or temp[0]>=299 or temp[1]<0 or temp[1]>=299:
				act=(np.random.rand(1,2)*2-1)
				temp=pos+act[0]
		else:
			act=sess.run(action,feed_dict={
				imageFeatureLayer:np.array([m]),
			})
		if showRes:
			"==="
			print(tar,pos)
			print(tar-pos)
			print(act)
		tars.append(tar)
		poss.append(pos)
		maps.append(m)
		pos=pos+act[0]
		acts.append(act[0])
		nposs.append(pos)
		if pos[0]<0 or pos[0]>=299 or pos[1]<0 or pos[1]>=299:
			done=True
			rew=-1.0
		elif -np.sum(abs(tar-pos))>-10:
			print("in!")
			success=True
			done=True
			rew=10.0
		else:
			rew=0.0
		rews.append(rew)

	util=calUtility(tars,poss,maps,acts,rews,nposs,done)

	return tars,poss,maps,acts,util,nposs,success

def HER(tars,poss,maps,acts,rews,nposs):
	HERtars,HERposs,HERmaps,HERacts,HERrews,HERnposs=[],[],[],[],[],[]
	tar=nposs[-1]
	
	for i in range(len(poss)):
		pos=poss[i]
		if pos[0]<0 or pos[0]>=9 or pos[1]<0 or pos[1]>=9:
			continue
		npos=nposs[i]
		if npos[0]<0 or npos[0]>=9 or npos[1]<0 or npos[1]>=9:
			npos=(np.random.rand(1,2)*9)[0]
		m=genMap(pos,npos)
		act=npos-pos
		rew=10.0
		HERtars.append(npos)
		HERposs.append(pos)
		HERacts.append(act)
		HERnposs.append(npos)
		HERrews.append(rew)
	# 	print(pos,npos)
	# 	print(act)
	# input()

	HERutil=[np.array([u]) for u in HERrews]

	return HERtars,HERposs,HERmaps,HERacts,HERutil,HERnposs

ran=True
for episode in range(1000):
	print(episode)
	tars,poss,maps,acts,util,nposs,success=run(showRes=True,randAct=ran)
	# HERtars,HERposs,HERmaps,HERacts,HERutil,HERnposs=HER(tars,poss,maps,acts,util,nposs)
	print(sum(util)/len(util))
	# print(HERutil)
	# input()
	
	#train critic
	# for i in range(80):
	# 	sess.run(c_optimizer,feed_dict={
	# 		imageFeatureLayer:np.array(maps),
	# 		c_a:np.array(acts),
	# 		y_input:np.array(util)
	# 	})

	# 	if i==79:
	# 		print("loss===",sess.run(cost,feed_dict={
	# 			imageFeatureLayer:np.array(maps),
	# 			c_a:np.array(acts),
	# 			y_input:np.array(util)
	# 		}))

	# 	if len(HERmaps)>0:
	# 		sess.run(c_optimizer,feed_dict={
	# 			imageFeatureLayer:np.array(HERmaps),
	# 			c_a:np.array(HERacts),
	# 			y_input:np.array(HERutil)
	# 		})

	if episode<0:
		continue
	else:
		ran=False

	#train actor
	targetActions=np.array(tars)-np.array(poss)
	targetActions=[30*t/sum(abs(t)) for t in targetActions]
	# print(targetActions)
	for i in range(50):
		
		sess.run(a_optimizer2,feed_dict={
			imageFeatureLayer:np.array(maps),
			a_input:targetActions
		})

		if i%10==0:			
			print(sess.run(cost_a,feed_dict={
			imageFeatureLayer:np.array(maps),
			a_input:targetActions
			}))
		

		# if len(HERmaps)>0:
		# 	t_act=sess.run(action,feed_dict={
		# 		imageFeatureLayer:np.array(HERmaps)
		# 	})
		# 	t_grad=sess.run(r_grad,feed_dict={
		# 		imageFeatureLayer:np.array(HERmaps),
		# 		c_a:t_act
		# 	})[0]
		# 	sess.run(a_optimizer,feed_dict={
		# 		imageFeatureLayer:np.array(HERmaps),
		# 		in_grad:t_grad
		# 	})

saver=tf.train.Saver()
# saver.save(sess,'/root/project/pybullet3_lance/kukaGrasp_pybullet/models/20190328_test_300.ckpt')

print("=====Test=====")
input()
total=0
for test in range(100):
	tars,poss,maps,acts,util,nposs,success=run(showRes=False)
	if success:
		total+=1

print(total)

