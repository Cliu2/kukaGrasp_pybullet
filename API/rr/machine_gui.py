#!/usr/bin/python2.7
# -*- coding:utf-8 -*-
__author__ = 'hkh'
__version__ = '1.0'
__date__ = '26/04/2017'

import os
import sys
_FILE_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, '%s/../../' % (_FILE_PATH))

import logging
import logging.config
from toolbox import fileinterface
import wx
import numpy as np
import copy
import functools
from base_frame import BaseFrame
from common_controller import MachineType
from common_controller import MachineError
from robot_controller import RobotController
from xy_platform_controller import XYPlatformController
from io_controller import IOController
from tcp_interface import ConnectError


def tryException(exception, errorMessage=None):
    def decorated(func):
        def wrapper(*args, **kwargs):
            try:
                res = func(*args, **kwargs)
                return res
            except exception as e:
                if errorMessage is None:
                    wx.MessageBox(e.message)
                else:
                    wx.MessageBox(errorMessage)

        return functools.wraps(func)(wrapper)
    return decorated


class MachineGui(BaseFrame):
    def __init__(self, parent, address):
        super(MachineGui, self).__init__(parent)
        # robot #
        # self._my_robot = RobotController(address=address, machineType=MachineType.FOUR_AXIS_RR)
        self._robot_run_pos = None
        self._robot_hand_mode = None
        self._robot_speed_level = None
        self._robot_speed = {
            'low': 1,
            'high': 100}
        self._robot_run_type = None
        self._robot_continue_movement = None
        self._robot_run_step = None

        # xy #
        # self._my_xy = XYPlatformController(address=address, machineType=MachineType.FOUR_AXIS_RR)
        self._xy_run_pos = None
        self._xy_speed_level = None
        self._xy_continue_movement = None
        self._xy_run_step = None
        self._xy_speed = {
            'low': 1,
            'high': 100}
        self._xy_limite = {
            'min_x': -0.0,
            'max_x': 170.0,
            'min_y': -170.0,
            'max_y': 0.0}
        # io #
        # self._my_io = IOController(address=address, machineType=MachineType.FOUR_AXIS_RR)
        self._input_io_num = 32
        self._io_input_check = [
            self.m_io_input_check_0, self.m_io_input_check_1, self.m_io_input_check_2, self.m_io_input_check_3,
            self.m_io_input_check_4, self.m_io_input_check_5, self.m_io_input_check_6, self.m_io_input_check_7,
            self.m_io_input_check_8, self.m_io_input_check_9, self.m_io_input_check_10, self.m_io_input_check_11,
            self.m_io_input_check_12, self.m_io_input_check_13, self.m_io_input_check_14, self.m_io_input_check_15,
            self.m_io_input_check_16, self.m_io_input_check_17, self.m_io_input_check_18, self.m_io_input_check_19,
            self.m_io_input_check_20, self.m_io_input_check_21, self.m_io_input_check_22, self.m_io_input_check_23,
            self.m_io_input_check_24, self.m_io_input_check_25, self.m_io_input_check_26, self.m_io_input_check_27,
            self.m_io_input_check_28, self.m_io_input_check_29, self.m_io_input_check_30, self.m_io_input_check_31,
        ]
        # self._io_input_status = self._getInputIOStatusFromMachine()
        # self._updateGuiInputIOStatus()

        self._output_io_num = 32
        self._io_output_check = [
            self.m_io_output_check_0, self.m_io_output_check_1, self.m_io_output_check_2, self.m_io_output_check_3,
            self.m_io_output_check_4, self.m_io_output_check_5, self.m_io_output_check_6, self.m_io_output_check_7,
            self.m_io_output_check_8, self.m_io_output_check_9, self.m_io_output_check_10, self.m_io_output_check_11,
            self.m_io_output_check_12, self.m_io_output_check_13, self.m_io_output_check_14, self.m_io_output_check_15,
            self.m_io_output_check_16, self.m_io_output_check_17, self.m_io_output_check_18, self.m_io_output_check_19,
            self.m_io_output_check_20, self.m_io_output_check_21, self.m_io_output_check_22, self.m_io_output_check_23,
            self.m_io_output_check_24, self.m_io_output_check_25, self.m_io_output_check_26, self.m_io_output_check_27,
            self.m_io_output_check_28, self.m_io_output_check_29, self.m_io_output_check_30, self.m_io_output_check_31,
        ]
        # self._io_output_status = self._getOutputIOStatusFromMachine()
        # self._updateGuiOutputIOStatus()
        self.m_text_ctrl_ip.SetValue(address[0])
        self.m_text_ctrl_port.SetValue(str(address[1]))

    @tryException(ValueError)
    def _onConnect(self, event):
        try:
            address = self._getServerAddress()
            machine_type = self._getRobotType()
            if not hasattr(self, '_my_robot'):
                self._my_robot = RobotController(address=address, machineType=machine_type)
            if not hasattr(self, '_my_xy'):
                self._my_xy = XYPlatformController(address=address, machineType=machine_type)
            if not hasattr(self, '_my_io'):
                self._my_io = IOController(address=address, machineType=machine_type)

            if not self._my_robot.isConnected():
                self._my_robot.connect()
                self._my_io.connect()
                self._my_xy.connect()
                self._io_input_status = self._getInputIOStatusFromMachine()
                self._updateGuiInputIOStatus()
                self._io_output_status = self._getOutputIOStatusFromMachine()
                self._updateGuiOutputIOStatus()
                wx.MessageBox('连接成功')
                self.m_button_connect.SetLabel('disconnect')
            else:
                self._my_robot.close()
                self._my_io.close()
                self._my_xy.close()
                self.m_button_connect.SetLabel('connect')
                if hasattr(self, '_my_robot'):
                    del self._my_robot
                if hasattr(self, '_my_io'):
                    del self._my_io
                if hasattr(self, '_my_xy'):
                    del self._my_xy
                wx.MessageBox('断开成功')
        except MachineError:
            if hasattr(self, '_my_robot'):
                del self._my_robot
            if hasattr(self, '_my_io'):
                del self._my_io
            if hasattr(self, '_my_xy'):
                del self._my_xy
            wx.MessageBox('连接失败')

    @tryException(MachineError)
    def onRobotRun(self, event):
        event.Skip()
        self._updateRobotRunPos()
        self._my_robot.goPos(self._robot_run_pos, type=self._robot_run_type)

    @tryException(MachineError)
    def onRobotStop(self, event):
        event.Skip()
        self._my_robot.stop()

    @tryException(MachineError)
    def onRobotAddX(self, event):
        event.Skip()
        if self._robot_continue_movement:
            self._my_robot.moveToFarthest(0, 1)
        else:
            self._updateRobotRunStep()
            self._my_robot.goDeltaPos(deltaPos=(self._robot_run_step, 0, 0, 0, 0, 0), type='move')

    @tryException(MachineError)
    def onRobotAddY(self, event):
        event.Skip()
        if self._robot_continue_movement:
            self._my_robot.moveToFarthest(1, 1)
        else:
            self._updateRobotRunStep()
            self._my_robot.goDeltaPos(deltaPos=(0, self._robot_run_step, 0, 0, 0, 0), type='move')

    @tryException(MachineError)
    def onRobotAddZ(self, event):
        event.Skip()
        if self._robot_continue_movement:
            self._my_robot.moveToFarthest(2, 1)
        else:
            self._updateRobotRunStep()
            self._my_robot.goDeltaPos(deltaPos=(0, 0, self._robot_run_step, 0, 0, 0), type='move')

    @tryException(MachineError)
    def onRobotAddU(self, event):
        event.Skip()
        if self._robot_continue_movement:
            self._my_robot.moveToFarthest(3, 1)
        else:
            self._updateRobotRunStep()
            self._my_robot.goDeltaPos(deltaPos=(0, 0, 0, self._robot_run_step, 0, 0), type='go')

    @tryException(MachineError)
    def onRobotAddV(self, event):
        event.Skip()
        if self._robot_continue_movement:
            self._my_robot.moveToFarthest(4, 1)
        else:
            self._updateRobotRunStep()
            self._my_robot.goDeltaPos(deltaPos=(0, 0, 0, 0, self._robot_run_step, 0), type='go')

    @tryException(MachineError)
    def onRobotAddW(self, event):
        event.Skip()
        if self._robot_continue_movement:
            self._my_robot.moveToFarthest(5, 1)
        else:
            self._updateRobotRunStep()
            self._my_robot.goDeltaPos(deltaPos=(0, 0, 0, 0, 0, self._robot_run_step), type='go')

    @tryException(MachineError)
    def onRobotSubX(self, event):
        event.Skip()
        if self._robot_continue_movement:
            self._my_robot.moveToFarthest(0, -1)
        else:
            self._updateRobotRunStep()
            self._my_robot.goDeltaPos(deltaPos=(-self._robot_run_step, 0, 0, 0, 0, 0), type='move')

    @tryException(MachineError)
    def onRobotSubY(self, event):
        event.Skip()
        if self._robot_continue_movement:
            self._my_robot.moveToFarthest(1, -1)
        else:
            self._updateRobotRunStep()
            self._my_robot.goDeltaPos(deltaPos=(0, -self._robot_run_step, 0, 0, 0, 0), type='move')

    @tryException(MachineError)
    def onRobotSubZ(self, event):
        event.Skip()
        if self._robot_continue_movement:
            self._my_robot.moveToFarthest(2, -1)
        else:
            self._updateRobotRunStep()
            self._my_robot.goDeltaPos(deltaPos=(0, 0, -self._robot_run_step, 0, 0, 0), type='move')

    @tryException(MachineError)
    def onRobotSubU(self, event):
        event.Skip()
        if self._robot_continue_movement:
            self._my_robot.moveToFarthest(3, -1)
        else:
            self._updateRobotRunStep()
            self._my_robot.goDeltaPos(deltaPos=(0, 0, 0, -self._robot_run_step, 0, 0), type='go')

    @tryException(MachineError)
    def onRobotSubV(self, event):
        event.Skip()
        if self._robot_continue_movement:
            self._my_robot.moveToFarthest(4, -1)
        else:
            self._updateRobotRunStep()
            self._my_robot.goDeltaPos(deltaPos=(0, 0, 0, 0, -self._robot_run_step, 0), type='go')

    @tryException(MachineError)
    def onRobotSubW(self, event):
        event.Skip()
        if self._robot_continue_movement:
            self._my_robot.moveToFarthest(5, -1)
        else:
            self._updateRobotRunStep()
            self._my_robot.goDeltaPos(deltaPos=(0, 0, 0, 0, 0, -self._robot_run_step), type='go')

    def onRobotButtonUp(self, event):
        event.Skip()
        if self._robot_continue_movement:
            self.onRobotStop(event)

    def _updateRobotRunPos(self):
        x = float(self.m_robot_x_text.GetValue())
        y = float(self.m_robot_y_text.GetValue())
        z = float(self.m_robot_z_text.GetValue())
        u = float(self.m_robot_u_text.GetValue())
        v = float(self.m_robot_v_text.GetValue())
        w = float(self.m_robot_w_text.GetValue())
        self._robot_run_pos = (x, y, z, u, v, w)

    def _updateRobotHandMode(self):
        self._robot_hand_mode = self.m_robot_hand_mode_choice.GetStringSelection()

    def _updateRobotSpeedLevel(self):
        self._robot_speed_level = self.m_robot_speed_choice.GetStringSelection()

    def _updateRobotRunType(self):
        self._robot_run_type = self.m_robot_run_type_choice.GetStringSelection()

    def _updateRobotContinueMovementFlag(self):
        self._robot_continue_movement = self.m_robot_continue_movement_check.GetValue()

    def _updateRobotRunStep(self):
        self._robot_run_step = float(self.m_robot_step_text.GetValue())

    def _updateGuiRobotCurPos(self):
        cur_robot_pos = self._my_robot.getCurPos()
        self.m_robot_cur_x.SetValue(str(cur_robot_pos[0][0]))
        self.m_robot_cur_y.SetValue(str(cur_robot_pos[1][0]))
        self.m_robot_cur_z.SetValue(str(cur_robot_pos[2][0]))
        self.m_robot_cur_u.SetValue(str(cur_robot_pos[3][0]))
        self.m_robot_cur_v.SetValue(str(cur_robot_pos[4][0]))
        self.m_robot_cur_w.SetValue(str(cur_robot_pos[5][0]))

    @tryException(MachineError)
    def onXYRun(self, event):
        event.Skip()
        self._updateXYRunPos()
        self._my_xy.setSpeed(self._xy_speed[self._xy_speed_level])
        self._my_xy.goPos(self._xy_run_pos)

    @tryException(MachineError)
    def onXYStop(self, event):
        event.Skip()
        self._my_xy.stop()

    @tryException(MachineError)
    def onXYSubX(self, event):
        event.Skip()
        if self._xy_continue_movement:
            cur_pos = self._my_xy.getCurPos()
            dst_pos = cur_pos.copy()
            dst_pos[0] = self._xy_limite['min_x']
            self._my_xy.goPos(dst_pos)
        else:
            self._updateXYRunStep()
            self._my_xy.goDeltaPos(deltaPos=(-self._xy_run_step, 0))

    @tryException(MachineError)
    def onXYAddX(self, event):
        event.Skip()
        if self._xy_continue_movement:
            cur_pos = self._my_xy.getCurPos()
            dst_pos = cur_pos.copy()
            dst_pos[0] = self._xy_limite['max_x']
            self._my_xy.goPos(dst_pos)
        else:
            self._updateXYRunStep()
            self._my_xy.goDeltaPos(deltaPos=(self._xy_run_step, 0))

    @tryException(MachineError)
    def onXYSubY(self, event):
        if self._xy_continue_movement:
            cur_pos = self._my_xy.getCurPos()
            dst_pos = cur_pos.copy()
            dst_pos[1] = self._xy_limite['min_y']
            self._my_xy.goPos(dst_pos)
        else:
            self._updateXYRunStep()
            self._my_xy.goDeltaPos(deltaPos=(0, -self._xy_run_step))

    @tryException(MachineError)
    def onXYAddY(self, event):
        if self._xy_continue_movement:
            cur_pos = self._my_xy.getCurPos()
            dst_pos = cur_pos.copy()
            dst_pos[1] = self._xy_limite['max_y']
            self._my_xy.goPos(dst_pos)
        else:
            self._updateXYRunStep()
            self._my_xy.goDeltaPos(deltaPos=(0, self._xy_run_step))

    @tryException(MachineError)
    def onXYButtonUp(self, event):
        event.Skip()
        if self._xy_continue_movement:
            self.onXYStop(event)

    def _updateXYRunPos(self):
        x = float(self.m_xy_x_text.GetValue())
        y = float(self.m_xy_y_text.GetValue())
        self._xy_run_pos = (x, y)

    def _updateXYRunStep(self):
        self._xy_run_step = float(self.m_xy_step_text.GetValue())

    def _updateXYSpeedLevel(self):
        self._xy_speed_level = self.m_xy_speed_choice.GetStringSelection()

    def _updateXYContinueMovementFlag(self):
        self._xy_continue_movement = self.m_xy_continue_movement_check.GetValue()

    def _updateGuiXYCurPos(self):
        cur_xy_pos = self._my_xy.getCurPos()
        self.m_xy_cur_x.SetValue(str(cur_xy_pos[0][0]))
        self.m_xy_cur_y.SetValue(str(cur_xy_pos[1][0]))

    def onSetOutputIO(self, event):
        event.Skip()
        machine_io_output_status = np.array(self._io_output_status).ravel()
        gui_io_output_status = np.array([i.GetValue() for i in self._io_output_check]).ravel()
        io_not_equal = np.not_equal(machine_io_output_status, gui_io_output_status)
        for i in xrange(len(io_not_equal)):
            if io_not_equal[i]:
                flag = 'on' if gui_io_output_status[i] else 'off'
                self._my_io.setStatus(i, flag)
        self._io_output_status = copy.deepcopy(gui_io_output_status)

    def _getInputIOStatusFromMachine(self):
        return self._my_io.getAllStatus('Input')

    def _getOutputIOStatusFromMachine(self):
        return self._my_io.getAllStatus('Output')

    def _updateGuiInputIOStatus(self):
        for i in xrange(self._input_io_num):
            status = self._io_input_status[i]
            self._io_input_check[i].SetValue(status)

    def _updateGuiOutputIOStatus(self):
        for i in xrange(self._output_io_num):
            status = self._io_output_status[i]
            self._io_output_check[i].SetValue(status)

    def _getServerAddress(self):
        ip = self.m_text_ctrl_ip.GetAddress()
        port = int(self.m_text_ctrl_port.GetValue())
        return (ip, port)

    def _getRobotType(self):
        map_dict = {u'4轴-RR': MachineType.FOUR_AXIS_RR,
                    u'6轴-RR': MachineType.SIX_AXIS_RR,
                    u'4轴-KEN': MachineType.FOUR_AXIS_KEN,
                    u'6轴-KEN': MachineType.SIX_AXIS_KEN}
        return map_dict[self.m_choice_robot_type.GetStringSelection()]

    def onUpdate(self, event):
        event.Skip()
        if hasattr(self, '_my_robot') and self._my_robot.isConnected():
            self._updateRobotContinueMovementFlag()
            self._updateRobotSpeedLevel()
            self._updateRobotHandMode()
            self._updateRobotRunType()
            self._my_robot.setSpeed(self._robot_speed[self._robot_speed_level])
            self._my_robot.setAccel(self._robot_speed[self._robot_speed_level])
            self._my_robot.setHandMode(self._robot_hand_mode)
            self._updateGuiRobotCurPos()
        if hasattr(self, '_my_xy') and self._my_xy.isConnected():
            self._updateXYContinueMovementFlag()
            self._updateXYSpeedLevel()
            self._my_xy.setSpeed(self._xy_speed[self._xy_speed_level])
            self._my_xy.setAccel(self._xy_speed[self._xy_speed_level])
            self._updateGuiXYCurPos()
        if hasattr(self, '_my_io') and self._my_io.isConnected():
            self._io_input_status = self._getInputIOStatusFromMachine()
            self._updateGuiInputIOStatus()

    def onExit(self, event):
        self.Destroy()


if __name__ == '__main__':
    os.chdir(_FILE_PATH)

    # config_path = '../../res/input/logging_config.yaml'
    # logging.config.dictConfig(fileinterface.loadYaml(config_path))

    address = ('127.0.0.1', 2005)

    app = wx.App()
    frame = MachineGui(None, address=address)
    frame.Show()
    app.MainLoop()
