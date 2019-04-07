# from matplotlib import pyplot
import pickle
import imp
import math,random

def dynamicallyImport(module,paths):
	#paths must be a list of string
	file,pathName,des=imp.find_module(module,paths)
	mod=imp.load_module(module,file,pathName,des)
	return mod

class SuccessHistoryCounter():
	"""
	A class to record success history of grasping
	"""
	def __init__(self,recordEvery=10,N=50):
		self.history=[]
		self.rate=[]
		self.N=N
		self.recordEvery=recordEvery
		self.maxR=0
		self.count=0
	
	def appendResult(self,res):
		self.history.append(res)
		if res: self.count+=1
		if len(self.history)%self.recordEvery==0:
			lastNRate=self.getLastNSuccessRate(self.N)
			self.rate.append(lastNRate)
			if self.maxR<lastNRate:
				self.maxR=lastNRate
				return True
		return False

	def getSuccessNumber(self):
		return self.count


	def getLastNSuccessRate(self,N):
		if len(self.history)<=N:
			return len([x for x in self.history if x==True])/len(self.history)
		else:
			temp=self.history[-N:]
			return len([x for x in temp if x==True])/len(temp)
		
	def saveRecord(self,fileName):
		with open(fileName,'wb') as f:
			pickle.dump([self.history,self.rate],f)

	def loadRecord(self,fileName):
		with open(fileName,'rb') as f:
			self.history=pickle.load(f)[0]
			self.rate=pickle.load(f)[1]
			self.maxR=max(self.rate)

	def showRateGraph(self):
		x_axis=[recordEvery*i for i in self.rate]
		graph=pyplot.plot(x_axis,self.rate)
		pyplot.show(graph)

	def report(self):
		print('successRate over last:',self.N,'rounds',self.rate[-1])
		print('total success:',self.count)

class DecayNumber():
	def __init__(self,start,decayMethod,decayRate,minV=0):
		"""
		Prams:
			decayRate: will be used differently in different methods.
			The larger decayRate, the fast return value decays

		exp:
			exponential decay: x <-- x*decayRate
		frac:
			fraction: value <-- start/(1+decayRate*value)
		sigmoid:
			2start/(1+e^(x*decayRate))
		linear:
			start(1-x*decayRate)
		"""
		self.value=None
		self.start=start
		self.min=minV
		self.decayRate=decayRate
		if hasattr(self,decayMethod):
			self.method=getattr(self,decayMethod)
		else:
			raise NameError("NO decay method named:"+decayMethod)

	def exp(self):
		if self.value==None: self.value=self.start
		self.value*=self.decayRate
		return self.value

	def frac(self):
		if self.value==None: self.value=-1
		self.value+=1
		return self.start/(1+self.decayRate*self.value)

	def sigmoid(self):
		if self.value==None: self.value=-1
		self.value+=1
		return self.start*2/(1+math.exp(self.value*self.decayRate))

	def getNumber(self):
		val=self.method()
		if self.min!=None:
			return max(self.min,val)
		else:
			return val

	def linear(self):
		if self.value==None: self.value=-1
		self.value+=1
		return self.start*(1-self.value*self.decayRate)

class ReplayBuffer():
	def __init__(self,bufferSize,useNextState=False):
		self.states=[]
		self.actions=[]
		self.Y=[]
		self.bufferSize=bufferSize
		self.useNextState=useNextState

	def addRecord(self,state,action,Y,random=True):
		self.states.append(state)
		self.actions.append(action)
		self.Y.append(Y)
		if len(self.actions)>self.bufferSize:
			self.fitRecordSize(random)

	def addRecords(self,states,actions,Y,random=True):
		self.states+=states
		self.actions+=actions
		self.Y+=Y
		if len(self.actions)>self.bufferSize:
			self.fitRecordSize(random)

	def fitRecordSize(self,useRandom):
		if (not self.useNextState) and useRandom:				
			indices=random.sample(range(len(self.actions)),self.bufferSize)
			self.states=[self.states[i] for i in indices]
			self.actions=[self.actions[i] for i in indices]
			self.Y=[self.Y[i] for i in indices]
		else:
			self.states=self.states[-self.bufferSize:]
			self.actions=self.actions[-self.bufferSize:]
			self.Y=self.Y[-self.bufferSize:]

	def getRecord(self,N):
		if self.useNextState:
			if (len(self.actions)>N):
				indices=random.sample(range(len(self.actions)-1),N)
				s=[self.states[i] for i in indices if self.actions[i]is not None]
				a=[self.actions[i] for i in indices if self.actions[i]is not None]
				y=[self.Y[i] for i in indices if self.actions[i]is not None]
				ns=[self.states[i+1] for i in indices if self.actions[i]is not None]
				return s,a,y,ns
			else:
				indices=[i for i in range(len(self.actions)-1) if (self.actions[i] is not None)]
				s=[self.states[i] for i in indices]
				a=[self.actions[i] for i in indices]
				y=[self.Y[i] for i in indices]
				ns=[self.states[i+1] for i in indices]
				return s,a,y,ns
		else:
			if len(self.actions)>N:
				indices=random.sample(range(len(self.actions)),N)
				s=[self.states[i] for i in indices]
				a=[self.actions[i] for i in indices]
				y=[self.Y[i] for i in indices]
				return s,a,y
			else:
				return self.states,self.actions,self.Y

	def cleanBuffer(self):
		self.states,self.actions,self.Y=[],[],[]

		

if __name__=="__main__":
	s=SuccessHistoryCounter()
	s.loadRecord("../logs/20190218_Reward_DDPG_replayBuffer_actionScaled.pkl")
	s.showRateGraph()