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
import yaml
import numpy as np
from tcp_interface import TcpInterface
from tcp_interface import ConnectError

__all__ = ['MachineError', 'MachineType', 'DecodeError', 'InvalidData', 'CommonController']

"""
* @brief enum ErrorCode define the error type and number.
* -# Err_RegexPattern   -21: the Regex Pattern is wrong.
* -# Err_YamlParser     -18: Failed to parser the yaml file, or the yaml file not exist.
* -# Err_RouteShm       -17: Failed to read/write the Route Shared Memory.
* -# Err_Power          -16: The power flag of robot is not desirable.
* -# Err_RobotInit      -15: The LogicRobot object is not initialized.
* -# Err_IONum          -14: The number of IO is invalid.
* -# Err_InputArgs      -13: The input function parameters is invalid.
* -# Err_ParamNotInit   -12: Parameter not be initialized.
* -# Err_FoundFile      -11: Failed to find the file
* -# Err_UnequalZero    -10: the value != 0. But the value expects 0.
* -# Err_EqualZero      -9 : the value == 0. But the value does not expect 0.
* -# Err_CureSteps      -8 : The calculated cure-steps less than 4.
* -# Err_MemMalloc      -7 : Failed to call the malloc() function.
* -# Err_Ik             -6 : Failed to solve the ik.
* -# Err_OutCoordRange  -5 : The calculated coordinate (mm) value is out of the valid range.
* -# Err_OutJointsRange -4 : The calculated robot joint angle is out of the valid range.
* -# Err_Trajectory     -3 : Failed to calculate the robot trajectory.
* -# Err_RWShm          -2 : Failed to Read/Write Shared Memory.
* -# Err_Error          -1 : Generic Error.
* -# Err_OK              0 : OK.
"""
ERROR_TYPE = {
    '-25': 'Err_CoordOutRange',
    '-24': 'Err_JaOutRange',
    '-23': 'Err_AccessSemFlag',
    '-22': 'Err_OverRouteShm',
    '-21': 'Err_RegexPattern',
    '-20': 'Err_LuaCall',
    '-19': 'Err_TcpConnection',
    '-18': 'Err_YamlParser',
    '-17': 'Err_RouteShm',
    '-16': 'Err_Power',
    '-15': 'Err_RobotInit',
    '-14': 'Err_IONum',
    '-13': 'Err_InputArgs',
    '-12': 'Err_ParamNotInit',
    '-11': 'Err_FileExistance',
    '-10': 'Err_UnequalZero',
    '-9': 'Err_EqualZero',
    '-8': 'Err_CurveSteps',
    '-7': 'Err_MemMalloc',
    '-6': 'Err_IK',
    '-5': 'Err_OutCoordRange',
    '-4': 'Err_OutJointsRange',
    '-3': 'Err_Trajectory',
    '-2': 'Err_RWShm',
    '-1': 'Err_Error',
    '0': 'Err_OK'
}


class MachineError(Exception):
    pass


class DecodeError(MachineError):
    pass


class InvalidData(MachineError):
    pass


class MachineType(object):
    FOUR_AXIS_RR = 'robot(4,"RR")\n'
    SIX_AXIS_RR = 'robot(6,"RR")\n'
    FOUR_AXIS_KEN = 'robot(4,"KENT")\n'
    SIX_AXIS_KEN = 'robot(6,"KENT")\n'


class CommonController(object):
    def __init__(self, address, machineType):
        self._my_logger = logging.getLogger("CommonController.%s" % (self.__class__.__name__))
        self._tcp = TcpInterface(address=address)
        self._machine_type = machineType

    def connect(self):
        try:
            self._tcp.connect()
            self._sendAndRecvData('motor(1)')
        except ConnectError as e:
            raise MachineError(e)

    def close(self):
        self._tcp.close()

    def isConnected(self):
        return self._tcp.isConnected()

    def _sendAndRecvData(self, msg, dataKey=None, bufferLength=1024, debug=False):
        try:
            receive_str = self._tcp.sendAndRecv(msg, bufferLength)
            if debug:
                print receive_str
        except ConnectError as e:
            raise MachineError(e)
        receive_data = self.__decodeSrcStr(receive_str)

        err = receive_data['err']
        if err < 0:
            self._my_logger.warn("robot return err: %s" % (ERROR_TYPE[str(err)], ))
            if 'ErrMsg' in receive_data:
                self._my_logger.warn('ErrMsg: %s' % (receive_data['ErrMsg']))
            raise MachineError("robot return err: %s" % (ERROR_TYPE[str(err)]), )
        if dataKey is None:
            return receive_data
        elif dataKey in receive_data:
            # self._my_logger.info('receive data: %s', receive_data[dataKey])
            return receive_data[dataKey]
        else:
            self._my_logger.warn('key %s not in receive data', dataKey)
            raise InvalidData('key %s not in receive data' % (dataKey, ))

    def _encode(self, pos):
        assert isinstance(pos, (np.ndarray, list, tuple))
        assert len(pos) > 0

        ravel_str = str(np.array(pos).reshape(-1).tolist())[1:-1]
        return ravel_str

    def _decode(self, str):
        # self._my_logger.info('decode data')
        try:
            pos_list = str.split(',')
            pos_nx1 = np.array(pos_list, dtype=np.float32).reshape(-1, 1)
        except Exception as e:
            self._my_logger.error('decode error: %s' % (e.message))
            raise DecodeError(e.message)
        # self._my_logger.info('end decode data')
        return pos_nx1

    def __decodeSrcStr(self, str):
        data_dict = {}
        for split_str in str.split('\n'):
            if len(split_str) > 3:
                split_idx = split_str.find(':')
                key = split_str[:split_idx]
                value = split_str[split_idx + 1:]
                # key, value = split_str.split(':')
                try:
                    data_dict[key] = int(value)
                except ValueError:
                    data_dict[key] = value
        return data_dict
