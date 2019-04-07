import sys
import time
sys.path.append("../")

from rr.tcp_interface import *
from rr.robot_controller import *

from rr.common_controller import CommonController
from rr.common_controller import MachineType
from rr.common_controller import MachineError

import pdb
import numpy as np

def move_point_sequence(pos):
    # moving to one point and print out the final locaiton
    try:
        my_robot.goPos(pos, error=5.0, type="move")
        my_robot.waitMoveDone()
    except Exception as e:
        print(type(e), e)
    time.sleep(0.5)
    print '---------------------------------------'
    cur_pos = my_robot.getCurPos()
    print 'cur_pos:\n', cur_pos
    print '---------------------------------------'

if __name__ == "__main__":
    print('--------------------------------------')
    # connect to the robot
    address = ('127.0.0.1', 2005)
    my_robot = RobotController(address, machineType=MachineType.SIX_AXIS_KEN)
    my_robot.connect()
    my_robot.setSpeed(3)
    my_robot.setAccel(4)
    my_robot.setHandMode('left')
    
    prev = time.time()
    cur_pos = my_robot.getCurPos()
    print 'cur_pos:\n', cur_pos
    print 'time used', time.time() - prev
    print('--------------------------------------')
    
    print("moving to current pos with goPos")
    prev = time.time()
    my_robot.goPos(cur_pos.reshape(-1), error=1, type="move")
    cur_pos = my_robot.getCurPos()
    print 'cur_pos:\n', cur_pos
    print 'time used', time.time() - prev
    print('--------------------------------------')
    
    print("moving to new pos with goPos")
    prev = time.time()
    my_robot.goPos(cur_pos.reshape(-1) + np.array([0,0,10,0,0,0]), error=1, type="move")
    cur_pos = my_robot.getCurPos()
    print 'cur_pos:\n', cur_pos
    print 'time used', time.time() - prev
    print('--------------------------------------')
    
    print("moving to new pos with goDeltaPos")
    prev = time.time()
    my_robot.goDeltaPos(np.array([0,0,-10,0,0,0]), error=1, type="move")
    cur_pos = my_robot.getCurPos()
    print 'cur_pos:\n', cur_pos
    print 'time used', time.time() - prev
    print('--------------------------------------')
    
    #pos_str = my_robot._sendAndRecvData('runLuaFile("/home/ubuntu/Desktop/rr_interface/script/lua_test_script/test4.lua")', dataKey='ret')
    #time.sleep(30)
    
    #my_robot.stop()
    #my_robot.close()
    
