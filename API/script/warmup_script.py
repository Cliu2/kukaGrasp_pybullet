import sys
import time
sys.path.append("../")

from rr.tcp_interface import *
from rr.robot_controller import *

from rr.common_controller import CommonController
from rr.common_controller import MachineType
from rr.common_controller import MachineError

import pdb

# initalial position [366.349, 4.69136, 420.248, 109.526, 5.56583 
#[476.09, -27.9355, 391.639, -44.6884, -21.559, -161.832]

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

    # connect to the robot
    address = ('127.0.0.1', 2005)
    my_robot = RobotController(address, machineType=MachineType.SIX_AXIS_KEN)
    my_robot.connect()
    my_robot.setSpeed(3)
    my_robot.setAccel(4)
    my_robot.setHandMode('left')
    print my_robot._sendAndRecvData("openFreqStatusPort(2005, 1000)", dataKey='ret', debug=True)
   
    prev = time.time()
    cur_pos = my_robot.getCurPos()
    print 'cur_pos:\n', cur_pos
    print 'time used: ', time.time() - prev
    # pdb.set_trace()
    
    # delay = {3:45, 4:40, 5:18}
    delay = {4:40, 5:18}
    
    for k in delay:
        pos_str = my_robot._sendAndRecvData('runLuaFile("/home/ubuntu/Desktop/rr_interface/script/lua_test_script/test%s.lua")' % (k), dataKey='ret')
        time.sleep(delay[k])
    # move_point_sequence([575.386, -61.792, 398.352, 25.4295, -61.5302, 137.048])
    #move_point_sequence([493.698, -298.9, 387.78, -47.2949, -53.5149, -166.395])
    #move_point_sequence([264.838, -333.156, 636.468, -121.978, -43.7164, -106.633])
    #move_point_sequence([421.519, -177.22, 561.523, 122.376, 4.61943, 88.9921])
    
    # move_point_sequence([205.947, -371.614, 141.72, -107.233, 7.14341, -170.074])
    # move_point_sequence([179.683, 438.159, 595.848, -139.384, -86.799, 26.8813])
    # move_point_sequence([118.468, 317.942, 783.522, -134.654, -60.4516, 23.6014])
    
    
