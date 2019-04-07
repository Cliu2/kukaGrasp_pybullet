#!/usr/bin/python2.7
# -*- coding:utf-8 -*-
__author__ = 'hkh'
__version__ = '1.0'
__date__ = '26/04/2017'

import os
import sys
_FILE_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, '%s/../../' % (_FILE_PATH))

import numpy as np
import time
import logging
import logging.config
from toolbox import fileinterface
from common_controller import CommonController
from common_controller import MachineType
from common_controller import MachineError


__all__ = ['XYPlatformController']


class XYPlatformController(CommonController):
    def __init__(self, address, machineType):
        super(XYPlatformController, self).__init__(address, machineType)

    def connect(self):
        super(XYPlatformController, self).connect()
        try:
            self.getCurPos()
        except MachineError:
            self._sendAndRecvData(self._machine_type)

    def getCurPos(self):
        self._my_logger.info('getting cur pos')
        cmd_str = "xy()\n"
        cur_pos_str_data = self._sendAndRecvData(cmd_str, dataKey='ret')
        cur_pos_2x1 = self._decode(cur_pos_str_data)
        self._my_logger.info('get cur pos: %s', cur_pos_2x1)
        return cur_pos_2x1

    def goPos(self, pos, error=None, timeout=60):
        assert isinstance(pos, (np.ndarray, list, tuple))
        assert 2 == len(pos)

        self._my_logger.info('go pos: %s', pos)

        pos_str = self._encode(pos)
        cmd_str = "xy(%s)\n" % (pos_str, )
        self._sendAndRecvData(cmd_str)

        if error is None:
            return True

        t = time.time()
        while True:
            if time.time() - t > timeout:
                raise MachineError('xy run timeout')

            cur_pos = self.getCurPos()
            if (abs((cur_pos).reshape(-1) - np.array(pos).reshape(-1)) <
                    np.array(error).reshape(-1)).all():
                return True
            time.sleep(0.02)

    def goDeltaPos(self, deltaPos, error=None, timeout=60):
        assert isinstance(deltaPos, (np.ndarray, list, tuple))
        assert 2 == len(deltaPos)

        self._my_logger.info("go delta pos: %s", (deltaPos))
        cur_pos = self.getCurPos()
        dst_pos = cur_pos + np.array(deltaPos).reshape(2, 1)
        self.goPos(dst_pos, error=error, timeout=timeout)

    def getCurJointAngle(self):
        self._my_logger.info('getting cur joint angle')
        cmd_str = "jaxy()\n"
        cur_joint_angle_str_data = self._sendAndRecvData(cmd_str, dataKey='ret')
        cur_joint_angle_2x1_deg = self._decode(cur_joint_angle_str_data)
        self._my_logger.info('get cur joint angle: %s', cur_joint_angle_2x1_deg)
        return cur_joint_angle_2x1_deg

    def goJointAngle(self, jointAngle_deg, error=None, timeout=60):
        assert isinstance(jointAngle_deg, (np.ndarray, list, tuple))
        assert 2 == len(jointAngle_deg)

        self._my_logger.info('go joint angle: %s', jointAngle_deg)

        angle_str = self._encode(jointAngle_deg)
        cmd_str = "jaxy(%s)\n" % (angle_str, )
        self._sendAndRecvData(cmd_str)

        if error is None:
            return True

        t = time.time()
        while True:
            if time.time() - t > timeout:
                raise MachineError('xy run timeout')

            cur_joint_angle = self.getCurJointAngle()
            if (abs((cur_joint_angle).reshape(-1) - np.array(jointAngle_deg).reshape(-1)) <
                    np.array(error).reshape(-1)).all():
                return True
            time.sleep(0.01)

    def goDeltaJointAngle(self, deltaAngle_deg, error=None, timeout=60):
        assert isinstance(deltaAngle_deg, (np.ndarray, list, tuple))
        assert 2 == len(deltaAngle_deg)

        self._my_logger.info("go delta angle: %s", (deltaAngle_deg))
        cur_joint_angle_deg = self.getCurJointAngle()
        dst_joint_angle_deg = cur_joint_angle_deg + np.array(deltaAngle_deg).reshape(2, 1)
        self.goJointAngle(dst_joint_angle_deg, error=error, timeout=timeout)

    def setSpeed(self, speed):
        assert isinstance(speed, (int, float))
        assert 0 <= speed <= 100

        self._my_logger.info('set speed')
        cmd_str = "xySpeed(%s)\n" % (speed, )
        self._sendAndRecvData(cmd_str)

    def setAccel(self, accel):
        assert isinstance(accel, (int, float))
        assert 0 <= accel <= 100

        self._my_logger.info('set accel')
        cmd_str = "xyAccel(%s)\n" % (accel, )
        self._sendAndRecvData(cmd_str)

    def waitMoveDone(self):
        self._my_logger.info('waiting move done')
        cmd_str = "xyTargetOK()"
        target_ok = False
        while not target_ok:
            target_ok = self._sendAndRecvData(cmd_str, dataKey='ret')
            time.sleep(0.01)
        self._my_logger.info('move done!')

    def checkTargetOK(self):
        raise MachineError('this func have not been implemented')

    def stop(self):
        self._my_logger.info('stop!')
        cmd_str = 'emgStop(1)'
        self._sendAndRecvData(cmd_str)
        cmd_str = 'emgStop(0)'
        self._sendAndRecvData(cmd_str)


if __name__ == '__main__':
    os.chdir(_FILE_PATH)

    config_path = '../../res/input/logging_config.yaml'
    logging.config.dictConfig(fileinterface.loadYaml(config_path))

    address = ('127.0.0.1', 2005)
    xy_controller = XYPlatformController(address, machineType=MachineType.FOUR_AXIS_RR)
    xy_controller.connect()
    xy_controller.setSpeed(10)
    xy_controller.setAccel(10)
    print xy_controller.getCurPos()
    xy_controller.goDeltaPos((50, 50), error=1)
    xy_controller.goDeltaPos((-50, -50), error=1)
