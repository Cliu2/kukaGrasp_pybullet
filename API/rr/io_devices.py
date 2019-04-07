#!/usr/bin/python2.7
# -*- coding:utf-8 -*-
__author__ = 'hyk'
__version__ = 1.0
__date__ = '16/01/2018'

import os
import sys
import time
import logging
import gettext

_ = gettext.gettext

_FILE_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append('%s/../../' % (_FILE_PATH))
from io_controller import IOController
from common_controller import MachineType


class IoDevicesError(Exception):
    pass


class IoDevicesBase(IOController):
    def __init__(self, address, config_dic, name, machineType):
        self._my_logger = logging.getLogger("IoDevices.%s" % (self.__class__.__name__))
        self._my_logger.info(_('init %s'), self.__class__.__name__)
        super(IOController, self).__init__(address, machineType)
        self.connect()
        self._config_dic = config_dic
        self._name = name

    def on(self):
        raise IoDevicesError(_('on() have not be implemented'))

    def off(self):
        raise IoDevicesError(_('off() have not be implemented'))

    def isOn(self):
        raise IoDevicesError(_('isOn() have not be implemented'))

    def isOff(self):
        raise IoDevicesError(_('isOff() have not be implemented'))

    def waitOnDone(self):
        raise IoDevicesError(_('waitOnDone() have not be implemented'))

    def waitOffDone(self):
        raise IoDevicesError(_('waitOffDone() have not be implemented'))


class GenerateIoDevices:
    def getIoDevices(self, address, config_dic, name, machineType):
        """

        Parameters
        ----------
        address
        such as ('127.0.0.1', 2005)

        config_dic
        the config_dic contain out_io,in_io,wait_io_on_time,wait_io_off_time,type

        name
        such as gripper

        Returns object
        -------

        """
        return eval("%s(address, config_dic, name, machineType)" % config_dic['type'])


class IoDevices2out2in(IoDevicesBase):
    def __init__(self, address, config_dic, name, machineType):
        """

        Parameters
        ----------
        address
        such as ('127.0.0.1', 2005)

        config_dic
        config_dic.keys():[out_on_io, out_off_io, in_on_io, in_off_io, wait_io_on_time_s, wait_io_off_time_s, type]

        name
        such as 'gripper'
        """

        super(IoDevices2out2in, self).__init__(address, config_dic, name, machineType)
        self._checkInputValue(address, config_dic, name, machineType)
        self._wait_io_on_time_s = self._config_dic['wait_io_on_time_s']
        self._wait_io_off_time_s = self._config_dic['wait_io_off_time_s']

    def _checkInputValue(self, address, config_dic, name, machineType):
        assert isinstance(config_dic, dict)
        assert isinstance(address, tuple)
        assert isinstance(name, str)
        config_dic_key_list = config_dic.keys()

        assert 'out_on_io' in config_dic_key_list, 'input dictionary has no key (out_on_io)'
        assert 'out_off_io' in config_dic_key_list, 'input dictionary has no key (out_off_io)'
        assert 'in_on_io' in config_dic_key_list, 'input dictionary has no key (in_on_io)'
        assert 'in_off_io' in config_dic_key_list, 'input dictionary has no key (in_off_io)'
        assert 'wait_io_on_time_s' in config_dic_key_list, 'input dictionary has no key (wait_io_on_time_s)'
        assert 'wait_io_off_time_s' in config_dic_key_list, 'input dictionary has no key (wait_io_off_time_s)'
        assert 'type' in config_dic_key_list, 'input dictionary has no key (type)'

    def on(self, wait=True):
        self._my_logger.info(_('on %s io'), self._name)
        self.setStatus(io=self._config_dic['out_off_io'], flag="OFF")
        self.setStatus(io=self._config_dic['out_on_io'], flag="ON")
        if wait:
            self.waitOnDone()

    def off(self, wait=True):
        self._my_logger.info(_('off %s io'), self._name)
        self.setStatus(io=self._config_dic['out_on_io'], flag="OFF")
        self.setStatus(io=self._config_dic['out_off_io'], flag="ON")
        if wait:
            self.waitOffDone()

    def isOn(self):
        return self.getStatus(io=self._config_dic['in_on_io'])

    def isOff(self):
        return self.getStatus(io=self._config_dic['in_off_io'])

    def waitOnDone(self):
        t = time.time()
        self._my_logger.info(_('wait %s io on done'), self._name)
        while not self.isOn():
            if time.time() - t > self._wait_io_on_time_s:
                raise IoDevicesError(_('wait %s io on done timeout' % self._name))
        self._my_logger.info(_('end of wait %s io on done' % self._name))

    def waitOffDone(self):
        t = time.time()
        self._my_logger.info(_('wait %s io off done' % self._name))
        while not self.isOff():
            if time.time() - t > self._wait_io_off_time_s:
                raise IoDevicesError(_('wait %s io off done timeout' % self._name))
        self._my_logger.info(_('end of wait %s io off done' % self._name))


class IoDevices1out2in(IoDevicesBase):
    def __init__(self, address, config_dic, name, machineType):
        """

        Parameters
        ----------
        address
        such as ('127.0.0.1', 2005)

        config_dic
        config_dic.keys():[out_io, in_on_io, in_off_io, wait_io_on_time_s, wait_io_off_time_s, type]

        name
        such as 'gripper'
        """
        super(IoDevices1out2in, self).__init__(address, config_dic, name, machineType)
        self._checkInputValue(address, config_dic, name, machineType)
        self._wait_io_on_time_s = self._config_dic['wait_io_on_time_s']
        self._wait_io_off_time_s = self._config_dic['wait_io_off_time_s']

    def _checkInputValue(self, address, config_dic, name, machineType):
        assert isinstance(config_dic, dict)
        assert isinstance(address, tuple)
        assert isinstance(name, str)
        config_dic_key_list = config_dic.keys()
        assert 'out_io' in config_dic_key_list, 'input dictionary has no key (out_io)'
        assert 'in_on_io' in config_dic_key_list, 'input dictionary has no key (in_on_io)'
        assert 'in_off_io' in config_dic_key_list, 'input dictionary has no key (in_off_io)'
        assert 'wait_io_on_time_s' in config_dic_key_list, 'input dictionary has no key (wait_io_on_time_s)'
        assert 'wait_io_off_time_s' in config_dic_key_list, 'input dictionary has no key (wait_io_off_time_s)'
        assert 'type' in config_dic_key_list, 'input dictionary has no key (type)'

    def on(self, wait=True):
        self._my_logger.info(_('on %s io' % self._name))
        self.setStatus(io=self._config_dic['out_io'], flag="ON")
        if wait:
            self.waitOnDone()

    def off(self, wait=True):
        self._my_logger.info(_('off %s io' % self._name))
        self.setStatus(io=self._config_dic['out_io'], flag="OFF")
        if wait:
            self.waitOffDone()

    def isOn(self):
        return self.getStatus(io=self._config_dic['in_on_io'])

    def isOff(self):
        return self.getStatus(io=self._config_dic['in_off_io'])

    def waitOnDone(self):
        t = time.time()
        self._my_logger.info(_('wait %s io on done' % self._name))
        while not self.isOn():
            if time.time() - t > self._wait_io_on_time_s:
                raise IoDevicesError(_('wait %s io on done timeout' % self._name))
        self._my_logger.info(_('end of wait %s io on done' % self._name))

    def waitOffDone(self):
        t = time.time()
        self._my_logger.info(_('wait %s io off done'), self._name)
        while not self.isOff():
            if time.time() - t > self._wait_io_off_time_s:
                raise IoDevicesError(_('wait %s io off done timeout'), self._name)
        self._my_logger.info(_('end of wait %s io off done'), self._name)


class IoDevices1out0in(IoDevicesBase):
    def __init__(self, address, config_dic, name, machineType):
        """

        Parameters
        ----------
        address
        such as ('127.0.0.1', 2005)

        config_dic
        config_dic.keys():[out_io, type]

        name
        such as 'gripper'
        """
        super(IoDevices1out0in, self).__init__(address, config_dic, name, machineType)
        self._checkInputValue(address, config_dic, name, machineType)

    def _checkInputValue(self, address, config_dic, name, machineType):
        assert isinstance(config_dic, dict)
        assert isinstance(address, tuple)
        assert isinstance(name, str)
        config_dic_key_list = config_dic.keys()
        assert 'out_io' in config_dic_key_list, 'input dictionary has no key (out_io)'
        assert 'type' in config_dic_key_list, 'input dictionary has no key (type)'

    def on(self):
        self._my_logger.info(_('on %s io'), self._name)
        self.setStatus(io=self._config_dic['out_io'], flag="ON")

    def off(self):
        self._my_logger.info(_('off %s io'), self._name)
        self.setStatus(io=self._config_dic['out_io'], flag="OFF")


class IoDevices0out1in(IoDevicesBase):
    def __init__(self, address, config_dic, name, machineType):
        """

        Parameters
        ----------
        address
        such as ('127.0.0.1', 2005)

        config_dic
        config_dic.keys():[in_on_io, type]

        name
        such as 'gripper'
        """
        super(IoDevices0out1in, self).__init__(address, config_dic, name, machineType)
        self._checkInputValue(address, config_dic, name, machineType)

    def _checkInputValue(self, address, config_dic, name, machineType):
        assert isinstance(config_dic, dict)
        assert isinstance(address, tuple)
        assert isinstance(name, str)
        config_dic_key_list = config_dic.keys()
        assert 'in_on_io' in config_dic_key_list, 'input dictionary has no key (in_on_io)'
        assert 'type' in config_dic_key_list, 'input dictionary has no key (type)'

    def isOn(self):
        return self.getStatus(io=self._config_dic['in_on_io'])


if __name__ == '__main__':
    from toolbox import fileinterface
    para_dic = {'address': ('127.0.0.1', 2005), 'block': {'out_io': 3, 'in_on_io': 7,
                                                          'in_off_io': 6, 'wait_io_on_time_s': 0.5,
                                                          'wait_io_off_time_s': 0.5, 'type': 'IoDevices1out2in'},
                'fixer': {'out_io': 6, 'type': 'IoDevices1out0in'},
                'sensor': {'in_on_io': 1, 'type': 'IoDevices0out1in'},
                'light':  {'out_io': 0, 'type': 'IoDevices1out0in'}}
    # print x
    io_devices_gennertor = GenerateIoDevices()
    print para_dic.keys()
    block = io_devices_gennertor.getIoDevices(para_dic['address'], para_dic['block'], 'block', MachineType.FOUR_AXIS_KEN)
    fixer = io_devices_gennertor.getIoDevices(para_dic['address'], para_dic['fixer'], 'fixer', MachineType.FOUR_AXIS_KEN)
    light = io_devices_gennertor.getIoDevices(para_dic['address'], para_dic['light'], 'light', MachineType.FOUR_AXIS_KEN)
    sensor = io_devices_gennertor.getIoDevices(para_dic['address'], para_dic['sensor'], 'sensor',
                                               MachineType.FOUR_AXIS_KEN)
    print type(block)
    # while True:
    #     print sensor.isOn()
    # block.on()
    # block.off()
    # fixer.on()
    # time.sleep(1)
    # fixer.off()
    light.on()
    print 'on'
    time.sleep(3)
    light.off()
