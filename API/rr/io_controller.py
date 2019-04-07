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
import time
from toolbox import fileinterface
from common_controller import CommonController
from common_controller import MachineType
from common_controller import MachineError


__all__ = ['IOController']


class IOController(CommonController):
    def __init__(self, address, machineType):
        assert machineType in (MachineType.FOUR_AXIS_RR, MachineType.FOUR_AXIS_KEN,
                               MachineType.SIX_AXIS_RR, MachineType.SIX_AXIS_KEN)
        super(IOController, self).__init__(address, machineType)

    def connect(self):
        super(IOController, self).connect()

        try:
            self.getAllStatus()
        except MachineError:
            self._sendAndRecvData(self._machine_type)

    def getStatus(self, io, flag='input'):
        assert isinstance(io, int)
        assert 0 <= io <= 31
        assert flag in ('input', 'output')

        self._my_logger.info('getting io %s status...' % (io))
        if 'input' == flag:
            cmd_str = "getInput(%s)\n" % (io)
        else:
            cmd_str = "getOutput(%s)\n" % (io)
        io_is_off = self._sendAndRecvData(cmd_str, dataKey='ret')
        io_is_on = not io_is_off
        self._my_logger.info('io %s io_is_on: %s' % (io, io_is_on))
        return io_is_on

    def setStatus(self, io, flag):
        assert isinstance(io, int)
        assert 0 <= io <= 31
        assert flag in ('on', 'off', 'ON', 'OFF')

        flag = flag.lower()
        self._my_logger.info('setting io %s to %s status...' % (io, flag))

        cmd_str = "%s(%s)\n" % (flag, io)
        self._sendAndRecvData(cmd_str)
        self._my_logger.info('set io %s to %s status...' % (io, flag))

    def getAllStatus(self, flag='Input'):
        assert flag in ('Input', 'Output')
        cmd_str = "getInput(%s)\n" % (0)
        status = self._sendAndRecvData(cmd_str, dataKey=flag)
        inv_status = 2**64 - 1 - status
        bit_64_str = '{:0>64b}'.format(inv_status)
        resverse_str = bit_64_str[::-1]
        return [bool(int(i)) for i in resverse_str]


if __name__ == '__main__':
    os.chdir(_FILE_PATH)

    config_path = '../../data/input/logging_config.yaml'
    logging.config.dictConfig(fileinterface.loadYaml(config_path))

    address = ('127.0.0.1', 2005)
    io_controller = IOController(address, machineType=MachineType.FOUR_AXIS_KEN)
    io_controller.connect()
    # io_controller.setStatus(1, flag='ON')
    # time.sleep(1)
    # io_controller.setStatus(1, flag='OFF')
    print io_controller.getStatus(0)
    time.sleep(1)
    while True:
        time.sleep(0.5)
        print io_controller.getStatus(1)
