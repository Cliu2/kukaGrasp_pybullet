from matplotlib import pyplot
import pickle

LOGFILE="20181029_successRateHistory.pkl"
PATH="/home/pi/Lance/kukaGrasp_pybullet"

if __name__=="__main__":
	#load file
	rates=[]
	with open(PATH+"/logs/"+LOGFILE,"rb") as f:
		rates=pickle.load(f)[0]

	x_axis=list(range(len(rates)))
	graph=pyplot.plot(x_axis,rates)

	
	pyplot.show(graph)