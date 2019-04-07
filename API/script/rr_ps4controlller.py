#!/usr/bin/env python3

# using PS4 controller to control the rr6 robotic arm for generating human demonstration results
import sys
sys.path.append("../")

from modules.rr_socket_interface import *
from modules.ps4controller import *
from modules.gripper import *
import socket
import pickle
import pdb
import os
import time
import pygame
from pprint import pprint
from enum import Enum
import serial

import threading
stop_ps4_update = False
ps4 = None
Home_pos = [254.2, 1.54, 437.934, -25, 0, -180]

raising_edge_flags = {
    'X': False,
    'O': False,
    'Square': False,
    'Triangle': False
}

def update_ps4_status():
    global raising_edge_flags
    while not stop_ps4_update:
        ps4.get_event()
        time.sleep(0.005)

        if ps4.raising_edge(ps4.button.X) and not raising_edge_flags['X']:
            raising_edge_flags['X'] = True

        if ps4.raising_edge(ps4.button.O) and not raising_edge_flags['O']:
            raising_edge_flags['O'] = True
            
        if ps4.raising_edge(ps4.button.Square) and not raising_edge_flags['Square']:
            raising_edge_flags['Square'] = True
            
        if ps4.raising_edge(ps4.button.Triangle) and not raising_edge_flags['Triangle']:
            raising_edge_flags['Triangle'] = True

if __name__ == "__main__":
    ps4 = PS4Controller(deadzone=0.1)
    rr = RR_interface(debug=False, speed=10, accel=20)
    gripper = Gripper()

    pprint(rr.getCurPos())
    
    cooldown = 0
    hat_coeff = [20,20,20]
    since_last_move = time.time()
    moving = True

    # move to init position
    try:
        rr.goPos(Home_pos, error=1)
    except Exception as e:
        print(type(e), e)
    pprint(rr.getCurPos())

    t = threading.Thread(target=update_ps4_status)
    t.start()

    while True:
        try:

            if ps4.button_data[ps4.button.PS]:
                print("Exit the program")
                stop_ps4_update = True
                # rr.stop()
                t.join()
                break
            
            if raising_edge_flags['O']:
                print("back to home position")
                rr.stop()
                rr.goPos(Home_pos, error=1)
                raising_edge_flags['O'] = False # clear the flag

            if raising_edge_flags['X']:
                print("toggle the gripper")
                gripper.toggle()
                raising_edge_flags['X'] = False # clear the flag
            
            if raising_edge_flags['Triangle']:
                raising_edge_flags['Triangle'] = False # clear the flag

            if raising_edge_flags['Square']:
                raising_edge_flags['Square'] = False # clear the flag
            
            if ps4.Lx != 0 or ps4.Ly != 0 or ps4.Ry != 0:
                moving = True
                # moving the robot, only one movement within cd time
                l = [abs(ps4.Lx), abs(ps4.Ly), abs(ps4.Ry)]
                max_ele_index = l.index(max(l))

                if time.time() - since_last_move > cooldown:
                    since_last_move = time.time()

                    start = time.time()
                    ret, used_time = rr.goDeltaPos([ps4.Ly*hat_coeff[0], ps4.Lx*hat_coeff[1], ps4.Ry*hat_coeff[2], 0, 0, 0])
                    print([ps4.Ly*hat_coeff[0], ps4.Lx*hat_coeff[1], ps4.Ry*hat_coeff[2], 0, 0, 0], used_time, time.time()-start)
                
                    # prevent it from suddent stop, add a delay for it
                    time.sleep(0.05)
                # else:
                #     print("cooling down", time.time() - since_last_move)
            elif ps4.Lx == 0 and ps4.Ly == 0 and ps4.Ry == 0 and moving:
                moving = False
                rr.stop()
                print("========== Stopped the robot! ==========")
                print(rr.getCurPos())
                print("========== Current position ^ ==========")

        except Exception as e:
            print(type(e), e)