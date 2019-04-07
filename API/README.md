# rr_interface

This repository is for bridging the ROS command to the TCP interface for the ethernet over USB communication used in Robotics Robotics 6 DOF robot arm.

The TCP client node sent a LUA script commmand though USB to the robot arm controller.

# How to use

## On the Jetson Tk1 side
Open a terminal, run
```
sudo killall RBTServer_main
~/Desktop/FastBoot.sh
```
After the RR GUI is opened, open another terminal and run
```
python ~/Desktop/rr_interface_v2/script/socket_server.py
```

## Modules
The modules folder contains the interface api for different hardware, namely kinect, suction gripper, 6DOF robot arm and ps4. Here shows differ

### Kinect_recorder.py
```
from modules.kinect_recorder import *
kinect = Kinect()
kinect.save_img(dir_name, filename) # this will save an image as jpg with a path "dir_name/filename.jpg"
```

### gripper.py
The udev rule under the config folder will create a softlink that contains the id of the Arduino. Therefore it will always open the port "/dev/arduino-75734323939351C011C0" in this application.
```
from modules.gripper import *
gripper = Gripper()
gripper.speed = 100 # setting and serial write the speed to the suction motor, range from 0 - 255
gripper.status = True # enabling or disabling(release) the suction gripper
gripper.toggle() # toggle the gripper
```

### ps4controller.py
```
from modules.ps4controller import *
ps4 = PS4Controller(deadzone=0.1)
ps4.get_event() # handle the ps4 event wrapping the data
ps4.raising_edge(ps4.button.X) # check of the button "X" is just pressed by the user
```

### rr_socket_interface.py
For every function, two things will be returned, one is the response of the function and the other on is the time used for the server to execute the command.

```
from modules.rr_socket_interface import *
rr = RR_interface(debug=False, speed=10, accel=20, zLimit=110)
rr.goHome() # reset the robot and go to home position
ret, used_time = rr.getCurPos() # this will return the an array of end-effector position
rr.goDeltaPos([dx,dy,dz,du,dv,dw]) # this will move the arm to delta [x,y,z,u,v,w]
rr.goPos([x,y,z,u,v,w]) 
```

### Example of recording the position and image
```
# At the begining of the program, make a directory for storing image and position data
program_start_time = str(int(datetime.datetime.now().timestamp()*1000))
dir_name = "./demo_{}".format(program_start_time)
if not os.path.exists(dir_name):
    os.makedirs(dir_name)
pos_log_file = open(dir_name+"/position.txt", "a")

# each record do action
rr.stop()
cur_time = int(time.time()*1000)
pos_log_file.write(str(cur_time)+' '+str(list(rr.cur_pos.reshape(-1)))+'\r\n')
kinect.save_img(dir_name, str(cur_time))
```