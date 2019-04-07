#!/usr/bin/python2.7
# -*- coding:utf-8 -*-
__author__ = 'hkh'
__version__ = '1.0'
__date__ = '26/04/2017'
__all__ = [
    'RobotError',
    'RobotController',
]

import os
import sys
_FILE_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, '%s/../' % (_FILE_PATH))

import numpy as np
import time

from common_controller import CommonController
from common_controller import MachineType
from common_controller import MachineError


AXIS_ANGLE_RANGE_MAP = \
    {MachineType.FOUR_AXIS_RR: 720,
     MachineType.FOUR_AXIS_KEN: 720,
     MachineType.SIX_AXIS_RR: 360,
     MachineType.SIX_AXIS_KEN: 360}

HAND_MODE_FLAG_MAP = {'left': 'L', 'right': 'R', 'auto': ''}


class RobotError(MachineError):
    pass


class RobotController(CommonController):
    def __init__(self, address, machineType):
        assert machineType in (MachineType.FOUR_AXIS_RR, MachineType.FOUR_AXIS_KEN,
                               MachineType.SIX_AXIS_RR, MachineType.SIX_AXIS_KEN)
        super(RobotController, self).__init__(address, machineType)
        self._axis_angel_range = AXIS_ANGLE_RANGE_MAP[machineType]
        self._hand_mode = 'L'
        self._robot_stop_max_times = 5
        self._min_step = 0.0001

    def connectGUIconnecting(self):
        try:
            self._tcp.connect()
        except RobotError as e:
            raise MachineError(e)

    def connect(self):
        super(RobotController, self).connect()
        try:
            self.getCurPos()
        except MachineError:
            self._sendAndRecvData(self._machine_type)

    def getCurPos(self):
        # self._my_logger.info('getting cur pos')
        cmd_str = "getPos()"
        cur_pos_str_data = self._sendAndRecvData(cmd_str, dataKey='ret')
        cur_pos_6x1 = self._decode(cur_pos_str_data)
        # self._my_logger.info('get cur pos: %s', cur_pos_str_data)
        return cur_pos_6x1

    def getCurPosGUIconnecting(self):
        # self._my_logger.info('getting cur pos')
        cmd_str = "getRobotState()"
        cur_pos_str_data = self._sendAndRecvData(cmd_str, dataKey='Pos_mm')
        cur_pos_str = cur_pos_str_data[cur_pos_str_data.index('[')+1 : cur_pos_str_data.index(']')]
        cur_pos_6x1 = self._decode(cur_pos_str)
        # self._my_logger.info('get cur pos: %s', cur_pos_str_data)
        return cur_pos_6x1

    def goPos(self, pos, error=None, type="go", timeout=30, handModeFlag=None):
        assert isinstance(pos, (np.ndarray, list, tuple))
        assert 6 == len(pos)
        assert type in ("go", "move", "GO", "MOVE")
        assert handModeFlag in HAND_MODE_FLAG_MAP or handModeFlag is None

        if handModeFlag is None:
            hand_mode = self._hand_mode
        else:
            hand_mode = HAND_MODE_FLAG_MAP[handModeFlag]

        self._my_logger.info('go pos: %s', pos)
        type = type.lower()
        cur_hand_mode = self.getCurHandMode()
        if error is not None and cur_hand_mode == handModeFlag:
            cur_pos = self.getCurPos()
            if (abs(np.array(pos).reshape(-1) - cur_pos.reshape(-1)) < np.array(error).reshape(-1)).all():
                return True

        pos_str = self._encode(pos)
        if type == 'go':
            cmd_str = '%s(%s,"%sIT")\n' % (type, pos_str, hand_mode)
        else:
            cmd_str = '%s(%s,"%sI")\n' % (type, pos_str, hand_mode)

        self._sendAndRecvData(cmd_str)

        if error is None:
            return True

        robot_stop_times = 0
        pre_pos = None

        t = time.time()
        while True:
            if time.time() - t > timeout:
                raise RobotError('robot run timeout')

            cur_pos = self.getCurPos()

            if pre_pos is None:
                pre_pos = cur_pos

            abs_delta_pos = np.abs(pre_pos - cur_pos)
            # print abs_delta_pos
            if (abs_delta_pos < self._min_step).all():
                robot_stop_times += 1
                if robot_stop_times > self._robot_stop_max_times:
                    self._my_logger.warn('robot already stop')
                    raise RobotError('robot already stop')
            else:
                robot_stop_times = 0

            pre_pos = cur_pos

            delta_abs_pos = abs(np.array(pos).reshape(-1) - cur_pos.reshape(-1))
            delta_abs_pos[3:] %= self._axis_angel_range
            delta_abs_pos[3:][delta_abs_pos[3:] > self._axis_angel_range / 2] = \
                self._axis_angel_range - delta_abs_pos[3:][delta_abs_pos[3:] > self._axis_angel_range / 2]

            if type == 'go':
                if (delta_abs_pos < np.array(error).reshape(-1)).all():
                    return True
            else:
                if (delta_abs_pos[:3] < np.array(error).reshape(-1)).all():
                    return True
            time.sleep(0.01)

    def goDeltaPos(self, deltaPos, error=None, type="go", timeout=30):
        assert isinstance(deltaPos, (np.ndarray, list, tuple))
        assert 6 == len(deltaPos)
        assert type in ("go", "move", "GO", "MOVE")

        type = type.lower()

        self._my_logger.info("go delta pos: %s", (deltaPos))
        cur_pos = self.getCurPos()
        dst_pos = cur_pos + np.array(deltaPos).reshape(6, 1)
        cur_hand_mode = self.getCurHandMode()
        self.goPos(dst_pos, type=type, error=error, timeout=timeout, handModeFlag=cur_hand_mode)

    def getCurJointAngle(self):
        # self._my_logger.info('getting cur joint angle')
        cmd_str = "getJoints()"
        cur_joint_angle_str_data = self._sendAndRecvData(cmd_str, dataKey='ret')
        cur_joint_angle_6x1_deg = self._decode(cur_joint_angle_str_data)
        # self._my_logger.info('get cur joint angle: %s', cur_joint_angle_str_data)
        return cur_joint_angle_6x1_deg

    def getCurJointAngleGUIconnecting(self):
        # self._my_logger.info('getting cur joint angle')
        cmd_str = "getRobotState()"
        cur_joint_angle_str_data = self._sendAndRecvData(cmd_str, dataKey='Joint_deg')
        cur_pos_str = \
            cur_joint_angle_str_data[cur_joint_angle_str_data.index('[')+1 : cur_joint_angle_str_data.index(']')]
        cur_joint_angle_6x1_deg = self._decode(cur_pos_str)
        # self._my_logger.info('get cur joint angle: %s', cur_joint_angle_str_data)
        return cur_joint_angle_6x1_deg

    def goJointAngle(self, jointAngle_deg, error=None, timeout=30):
        assert isinstance(jointAngle_deg, (np.ndarray, list, tuple))
        assert 6 == len(jointAngle_deg)

        self._my_logger.info('go joint angle: %s', jointAngle_deg)

        if error is not None:
            cur_joint_angle_deg = self.getCurJointAngle()
            if (abs(np.array(jointAngle_deg).reshape(-1) - cur_joint_angle_deg.reshape(-1)) <
                    np.array(error).reshape(-1)).all():
                return True

        joint_angle_str = self._encode(jointAngle_deg)
        cmd_str = 'goja(%s,"I")\n' % (joint_angle_str, )
        self._sendAndRecvData(cmd_str)

        if error is None:
            return True

        robot_stop_times = 0
        pre_joint_angle = None

        t = time.time()
        while True:
            if time.time() - t > timeout:
                raise RobotError('robot run timeout')

            cur_joint_angle = self.getCurJointAngle()

            if pre_joint_angle is None:
                pre_joint_angle = cur_joint_angle

            abs_delta_joint_angle = np.abs(pre_joint_angle - cur_joint_angle)
            if (abs_delta_joint_angle < self._min_step).all():
                robot_stop_times += 1
                if robot_stop_times > self._robot_stop_max_times:
                    self._my_logger.warn('robot already stop')
                    raise RobotError('robot already stop')
            else:
                robot_stop_times = 0

            if (abs(cur_joint_angle.reshape(-1) - np.array(jointAngle_deg).reshape(-1)) <
                    np.array(error).reshape(-1)).all():
                return True
            time.sleep(0.01)

    def goDeltaJointAngle(self, deltaAngle_deg, error=None, timeout=30):
        assert isinstance(deltaAngle_deg, (np.ndarray, list, tuple))
        assert 6 == len(deltaAngle_deg)

        self._my_logger.info("go delta angle: %s", (deltaAngle_deg))
        cur_joint_angle_deg = self.getCurJointAngle()
        dst_joint_angle_deg = cur_joint_angle_deg + np.array(deltaAngle_deg).reshape(6, 1)
        self.goJointAngle(dst_joint_angle_deg, error=error, timeout=timeout)

    def setSpeed(self, speed):
        assert isinstance(speed, (int, float))
        assert 0 <= speed <= 100

        self._my_logger.info('set speed: %s' % (speed))
        cmd_str = "setSpeed(%s)\n" % (speed, )
        self._sendAndRecvData(cmd_str)
        cmd_str = "setMoveSpeed(%s)\n" % (speed, )
        self._sendAndRecvData(cmd_str)

    def setAccel(self, accel):
        assert isinstance(accel, (int, float))
        assert 0 <= accel <= 100

        self._my_logger.info('set accel: %s' % (accel))
        cmd_str = "setAccel(%s)\n" % (accel, )
        self._sendAndRecvData(cmd_str)
        cmd_str = "setMoveAccel(%s)\n" % (accel, )
        self._sendAndRecvData(cmd_str)

    def setHandMode(self, flag):
        assert flag in HAND_MODE_FLAG_MAP
        self._my_logger.info('set hand type: %s' % (HAND_MODE_FLAG_MAP[flag]))
        self._hand_mode = HAND_MODE_FLAG_MAP[flag]

    def waitMoveDone(self, timeout=30):
        self._my_logger.info('waiting move done')
        cmd_str = "targetOK()"
        target_ok = False
        robot_stop_times = 0
        pre_pos = None
        t = time.time()
        while not target_ok:
            if time.time() - t > timeout:
                raise RobotError('robot run timeout')

            cur_pos = self.getCurPos()
            if pre_pos is None:
                pre_pos = cur_pos

            abs_delta_pos = np.abs(pre_pos - cur_pos)
            if (abs_delta_pos < self._min_step).all():
                robot_stop_times += 1
                if robot_stop_times > self._robot_stop_max_times:
                    self._my_logger.warn('robot already stop')
                    raise RobotError('robot already stop')
            else:
                robot_stop_times = 0

            target_ok = self._sendAndRecvData(cmd_str, dataKey='ret')
            time.sleep(0.01)
        self._my_logger.info('move done!')

    def checkTargetOK(self, pos):
        assert isinstance(pos, (np.ndarray, list, tuple))
        assert 6 == len(pos)

        pos_str = self._encode(pos)
        cmd_str = 'checkGo(%s)\n' % (pos_str)
        data_str = self._sendAndRecvData(cmd_str, dataKey='ret')
        print (data_str)
        is_ok, use_time_ms = self._decode(data_str)
        if is_ok == 0:
            return True
        # elif is_ok == 1:
        #     return False
        else:
            return False
            # raise RobotError('is_ok: %s' % (is_ok))

    def solveIK(self, pos):
        assert isinstance(pos, (np.ndarray, list, tuple))
        assert 6 == len(pos)

        pos_str = self._encode(pos)
        cmd_str = 'coord2deg(%s)\n' % (pos_str)
        try:
            joints_str = self._sendAndRecvData(cmd_str, dataKey='ret')
        except MachineError as e:
            if 'Err_IK' in e.message:
                return RobotError('IK Error')
            else:
                raise e
        joints_6x1_deg = self._decode(joints_str)
        return joints_6x1_deg

    def solveFK(self, jointAngle_deg):
        assert isinstance(jointAngle_deg, (np.ndarray, list, tuple))
        assert 6 == len(jointAngle_deg)

        joint_angle_str = self._encode(jointAngle_deg)
        cmd_str = 'deg2coord(%s)\n' % (joint_angle_str)
        pos_str = self._sendAndRecvData(cmd_str, dataKey='ret')
        pos_6x1 = self._decode(pos_str)
        return pos_6x1

    def stop(self):
        self._my_logger.info('stop!')
        cmd_str = 'emgStop(1)'
        self._sendAndRecvData(cmd_str)
        cmd_str = 'emgStop(0)'
        self._sendAndRecvData(cmd_str)

    def moveToFarthest(self, axisId, dire):
        assert axisId in xrange(0, 6)
        assert dire in (-1, 1)
        cmd_str = 'moveToFarthest(%s, %s)' % (axisId, dire)
        self._sendAndRecvData(cmd_str)

    def getCurHandMode(self):
        hand_mode_decode = ('left', 'right')
        cmd_str = "getPos()"
        cur_hand_mode = self._sendAndRecvData(cmd_str, dataKey='HandMode')
        return hand_mode_decode[cur_hand_mode]


def main():
    import logging.config
    from toolbox import fileinterface
    # from toolbox import logging_config
    os.chdir('../')
    config_path = '../../data/input/config/logging.yml'
    # logging_config.config(config_path)
    # logging.config.dictConfig(fileinterface.loadYaml(config_path))

    address = ('127.0.0.1', 2005)

    my_robot = RobotController(address, machineType=MachineType.SIX_AXIS_KEN)
    my_robot.connect()
    my_robot.setSpeed(10)
    my_robot.setAccel(10)
    my_robot.setHandMode('left')
    print "check if target reachable"
    print my_robot.checkTargetOK(
        np.array([[ 575.386],
                  [-61.792],
                  [ 398.352  ],
                  [  25.4295 ],
                  [ -61.5302],
                  [  137.048]]))
    print "check if target reachable"     
    print my_robot.checkTargetOK(
        np.array([[ 252.47399902],
                 [ 400.73699951],
                 [ 594.39501953],
                 [ 139.72599792],
                 [  73.79350281],
                 [  81.60939789]]))
    cur_pos = my_robot.getCurPos()
    print 'cur_pos:\n', cur_pos
    print '---------------------------------------'
    
    # my_robot.goPos((400, 0, 100, 0, 0, 0), error=1)
    my_robot.solveIK([400, 0, 100, 0, 0, 0])
    # print my_robot.solveFK([0, 0, 0, 0, 0, 0])
    # my_robot.goDeltaPos((0, 0, -30, 0, 0, 0))
    time.sleep(0.5)
    my_robot.stop()
    # my_robot.goDeltaPos((10, 10, -10, 0, 0, 0), type='move', error=1)
    cur_joint_angle_deg = my_robot.getCurJointAngle()
    my_robot.goDeltaJointAngle((10, 0, 0, 10, 0, 0), error=1)
    my_robot.goJointAngle(cur_joint_angle_deg)
    my_robot.waitMoveDone()

def main_2():
    import logging.config
    from toolbox import fileinterface
    # from toolbox import logging_config
    os.chdir('../')
    config_path = '../../data/input/config/logging.yml'
    # logging_config.config(config_path)
    # logging.config.dictConfig(fileinterface.loadYaml(config_path))

    address = ('127.0.0.1', 2005)

    my_robot = RobotController(address, machineType=MachineType.SIX_AXIS_KEN)
    my_robot.connect()
    my_robot.setSpeed(10)
    my_robot.setAccel(10)
    my_robot.setHandMode('left')
    
    print '---------------------------------------'
    cur_pos = my_robot.getCurPos()
    print 'cur_pos:\n', cur_pos
    print '---------------------------------------'
    
    # my_robot.goPos((400, 0, 100, 0, 0, 0), error=1)
    my_robot.solveIK([400, 0, 100, 0, 0, 0])
    # print my_robot.solveFK([0, 0, 0, 0, 0, 0])
    # my_robot.goDeltaPos((0, 0, -30, 0, 0, 0))
    time.sleep(0.5)
    my_robot.stop()
    # my_robot.goDeltaPos((10, 10, -10, 0, 0, 0), type='move', error=1)
    cur_joint_angle_deg = my_robot.getCurJointAngle()
    my_robot.goDeltaJointAngle((10, 0, 0, 10, 0, 0), error=1)
    print '---------------------------------------'
    cur_pos = my_robot.getCurPos()
    print 'cur_pos:\n', cur_pos
    print '---------------------------------------'

    
    my_robot.goJointAngle(cur_joint_angle_deg)
    my_robot.waitMoveDone()
    
    print '---------------------------------------'
    cur_pos = my_robot.getCurPos()
    print 'cur_pos:\n', cur_pos
    print '---------------------------------------'

if __name__ == '__main__':
    os.chdir(_FILE_PATH)
    main_2()
    #address = ('127.0.0.1', 2005)
