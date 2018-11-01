from matplotlib import pyplot
import pickle

LOGFILE="20181024_successRateHistory.pkl"

if __name__=="__main__":
	#load file
	rates=[]
	with open("../logs/"+LOGFILE,"rb") as f:
		rates=pickle.load(f)[0]

	x_axis=list(range(len(rates)))
	graph=pyplot.plot(x_axis,rates)

	
	pyplot.show(graph)