import os, inspect, pickle
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(os.path.dirname(currentdir))
workdir=os.path.dirname(currentdir)
os.sys.path.insert(0,parentdir)

# from kukaGrasp_pybullet.API.modules.gripper import *
# import time

# gripper = Gripper()
# while(True):
# 	gripper.speed = 100 # setting and serial write the speed to the suction motor, range from 0 - 255
# 	gripper.status = True # enabling or disabling(release) the suction gripper
# 	gripper.toggle() # toggle the gripper
# 	time.sleep(1000)
# 	gripper.status=False
# 	gripper.toggle()


# from kukaGrasp_pybullet.API.modules.rr_socket_interface import *
# rr = RR_interface(debug=False, speed=10, accel=20, zLimit=110)
# rr.goHome() # reset the robot and go to home position
# ret, used_time = rr.getCurPos() # this will return the an array of end-effector position
# # rr.goDeltaPos([dx,dy,dz,du,dv,dw]) # this will move the arm to delta [x,y,z,u,v,w]
# # rr.goPos([x,y,z,u,v,w]) 
# for i in range(10):
# 	# input()
# 	print(ret,used_time)
# 	rr.goDeltaPos([15,15,-5,0,0,0])

from kukaGrasp_pybullet.API.modules.kinect_recorder import *
# kinect = Kinect()
a=save_img('./pic','test') # this will save an image as jpg with a path "dir_name/filename.jpg"
print(a.shape)