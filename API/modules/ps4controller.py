#!/usr/bin/env python3

# using PS4 controller to control the rr6 robotic arm for generating human demonstration results

import socket
import pickle
import pdb
import os
import time
import pygame
from pprint import pprint
from enum import Enum


class PS4Controller(object):
    class Button(Enum):
        X = 0
        O = 1
        Triangle = 2
        Square = 3
        L1 = 4
        R1 = 5
        L2 = 6
        R2 = 7
        Share = 8
        Options = 9
        PS = 10
        L3 = 11
        R3 = 12
        T_pad = 13

    controller = None
    axis_data = None
    button_data = None
    hat_data = None

    button_data_old = None
    hat_data_old = None

    button = Button

    def __init__(self, deadzone=0.015):
        pygame.init()
        pygame.joystick.init()
        self.controller = pygame.joystick.Joystick(0)
        self.controller.init()

        self.deadzone = deadzone

        # init the ps4 data
        self.axis_data = {0: 0.0, 1: 0.0, 2: -1.0, 3: 0.0, 4: 0.0, 5: -1.0}
        self.button_data = {}
        for i in range(self.controller.get_numbuttons()):
            self.button_data[self.Button(i)] = False
        self.hat_data = {}
        for i in range(self.controller.get_numhats()):
            self.hat_data[i] = (0, 0)
        self.save_old_data()  # init ps4 old data
        self.wrap_axis_data()  # wraping the axis data to specific axis name

    def deadzone_filter(self):
        for k in self.axis_data:
            if abs(self.axis_data[k]) < self.deadzone:
                self.axis_data[k] = 0.0

    def get_event(self):
        # constantly call this function
        self.save_old_data()

        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                self.axis_data[event.axis] = round(event.value, 2)
            elif event.type == pygame.JOYBUTTONDOWN:
                self.button_data[self.button(event.button)] = True
            elif event.type == pygame.JOYBUTTONUP:
                self.button_data[self.button(event.button)] = False
            elif event.type == pygame.JOYHATMOTION:
                self.hat_data[event.hat] = event.value

            self.deadzone_filter()
            self.wrap_axis_data()

            return True  # updated

        return False

    def print(self):
        pprint(self.button_data)
        pprint(self.axis_data)
        pprint([self.Lx, self.Ly, self.Rx, self.Ry, self.L2, self.R2])
        pprint(self.hat_data)

    def wrap_axis_data(self):
        self.Lx = self.axis_data[0]
        self.Ly = -1*self.axis_data[1]
        self.Rx = self.axis_data[3]
        self.Ry = -1*self.axis_data[4]
        self.L2 = (self.axis_data[2]+1)/2.0
        self.R2 = (self.axis_data[5]+1)/2.0

    def save_old_data(self):
        self.button_data_old = self.button_data.copy()
        self.hat_data_old = self.hat_data.copy()

    def raising_edge(self, b):
        return (not self.button_data_old[b]) and self.button_data[b]

    def falling_edge(self, b):
        return self.button_data_old[b] and (not self.button_data[b])


if __name__ == "__main__":
    ps4 = PS4Controller(deadzone=0.2)

    while True:
        if ps4.get_event():
            #pass
            os.system('clear')
            ps4.print()
        time.sleep(0.01)