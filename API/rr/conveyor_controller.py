#!/usr/bin/python2.7
# -*- coding:utf-8 -*-
__author__ = 'hkh'
__version__ = '1.0'
__date__ = '26/04/2017'

import os
import sys
_FILE_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, '%s/../../' % (_FILE_PATH))

import time
import logging
import logging.config
from toolbox import fileinterface
from common_controller import CommonController
from common_controller import MachineType
from common_controller import MachineError


__all__  = ['ConveyorController']


class ConveyorController(CommonController):
    def __init__(self, address, dirIO, machineType):
        assert machineType in (MachineType.FOUR_AXIS_RR, MachineType.FOUR_AXIS_KEN,
                               MachineType.SIX_AXIS_RR, MachineType.SIX_AXIS_KEN)
        super(ConveyorController, self).__init__(address, machineType)
        self._dir_io = dirIO

    def connect(self):
        super(ConveyorController, self).connect()
        try:
            self.getDis_mm()
        except MachineError:
            self._sendAndRecvData(self._machine_type)

    def getDis_mm(self):
        self._my_logger.info('getting conveyor dis...')
        cmd_str = "conv_getPos()"
        conveyor_dis_mm = self._sendAndRecvData(cmd_str, dataKey='ret')
        self._my_logger.info('get Conveyor Dis(mm): %s' % (conveyor_dis_mm))
        return conveyor_dis_mm

    def waitStop(self):
        self._my_logger.info('waiting conveyor stop...')
        pre_dis_mm = self.getDis_mm()
        while True:
            time.sleep(0.1)
            new_dis_mm = self.getDis_mm()
            self._my_logger.info('new_dis_mm: %s' % (new_dis_mm))
            if pre_dis_mm == new_dis_mm:
                break
            else:
                pre_dis_mm = new_dis_mm
        self._my_logger.info('end of wait conveyor stop')

    def run(self, dis_mm=None):
        self._my_logger.info('run conveyor')
        cmd_str = "conv_run()"
        self._sendAndRecvData(cmd_str)

        if dis_mm is not None:
            origin_dis_mm = self.getDis_mm()
            while True:
                time.sleep(0.1)
                now_dis = self.getDis_mm()
                if now_dis - origin_dis_mm > dis_mm:
                    self.stop()
                    break

    def stop(self):
        self._my_logger.info('stopping conveyor')
        cmd_str = "conv_stop()"
        self._sendAndRecvData(cmd_str)
        self._my_logger.info('stopped conveyor')

    def setSpeed(self, speed):
        assert 0 <= speed <= 28
        assert isinstance(speed, int)
        self._my_logger.info('setting Conveyor Speed: %s', speed)
        cmd_str = "conv_setSpeed(%s)\n" % (speed)
        self._sendAndRecvData(cmd_str)
        self._my_logger.info('set Conveyor Speed!')

    def reset(self):
        self._my_logger.info('resetting...')
        cmd_str = "conv_reset()"
        self._sendAndRecvData(cmd_str)
        self._my_logger.info('reset!')

    def setDirection(self, flag):
        assert flag in ('positive', 'negative')

        self._my_logger.info('setting dir as %s', flag)
        if 'positive' == flag:
            cmd_str = "off(%s)\n" % (self._dir_io, )
        else:
            cmd_str = "on(%s)\n" % (self._dir_io, )
        self._sendAndRecvData(cmd_str)
        self._my_logger.info('set dir!')


if __name__ == '__main__':
    os.chdir(_FILE_PATH)

    config_path = '../../res/input/logging_config.yaml'
    logging.config.dictConfig(fileinterface.loadYaml(config_path))

    address = ('127.0.0.1', 2005)

    conveyor = ConveyorController(address, dirIO=10, machineType=MachineType.FOUR_AXIS_RR)
    conveyor.connect()
    conveyor.reset()
    print conveyor.getDis_mm()
    conveyor.setSpeed(1)
    conveyor.run()
    time.sleep(1)
    conveyor.setSpeed(28)
    time.sleep(1)
    conveyor.stop()
    conveyor.waitStop()
    conveyor.run(100)
