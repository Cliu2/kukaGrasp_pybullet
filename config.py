#default parameters
RGB,DEPTH,SEGMENT=2,3,4

settings={
	'learner':'ReplayRewardLearner',
	'network':'ActorCriticDDPG',
	'modelFileNames':'Reward_DDPG_replayBuffer_actionScaled',
	'episodes':600,
	'lr':0.1,
	'decay':0.9,
	'imageDimension':(512,512),
	'display':True,
	'cameraType':SEGMENT,
	'cameraRandom':1,
	'objectRange':(1,2),
	'networkDimension':(472,472),
	'epochsPerTraining':2,
	'epochs':20,
	'verbose':1
}