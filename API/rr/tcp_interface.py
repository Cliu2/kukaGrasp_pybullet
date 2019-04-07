#!/usr/bin/python2.7
# -*- coding:utf-8 -*-
__author__ = 'hkh'
__version__ = '1.0'
__date__ = '26/04/2017'

import os
import sys
_FILE_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, '%s/../../' % (_FILE_PATH))

import socket
import threading
import logging
import logging.config
from toolbox import fileinterface

import time

__all__ = ['ConnectError', 'TcpInterface']


class ConnectError(Exception):
    pass


class TcpInterface(object):
    _linked_address = {}

    def __init__(self, address):
        self._my_logger = logging.getLogger(self.__class__.__name__)
        self._timeout_time_s = 1
        self._lock = None
        self._sock = None
        self._address = address

    def __del__(self):
        self.close()

    def _register(self):
        if not self._isAddressRegistered():
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            lock = threading.Lock()
            self.__class__._linked_address[self._address] = {}
            self.__class__._linked_address[self._address]['sock'] = sock
            self.__class__._linked_address[self._address]['lock'] = lock
            self.__class__._linked_address[self._address]['connect_num'] = 1
        else:
            self._my_logger.info('the address have already connected')
            sock = self.__class__._linked_address[self._address]['sock']
            lock = self.__class__._linked_address[self._address]['lock']
            self.__class__._linked_address[self._address]['connect_num'] += 1
        return sock, lock

    def _unRegister(self):
        if self._address in self.__class__._linked_address:
            self.__class__._linked_address[self._address]['connect_num'] -= 1
            if 0 == self.__class__._linked_address[self._address]['connect_num']:
                self._sock.close()
                self.__class__._linked_address.pop(self._address)
        self._sock = None
        self._lock = None

    def connect(self):
        if self.isConnected():
            self._my_logger.info('have already connected')
        else:
            self._sock, self._lock = self._register()
            try:
                try:
                    self._sock.getpeername()
                except socket.error:
                    self._sock.connect(self._address)
                    self._sock.settimeout(self._timeout_time_s)
            except socket.error as e:
                self._unRegister()
                raise ConnectError(e)

    def close(self):
        if self.isConnected():
            self._unRegister()

    def isConnected(self):
        if self._sock is not None:
            return True
        else:
            return False

    def _isAddressRegistered(self):
        return self._address in self.__class__._linked_address

    def sendAndRecv(self, msg, bufferLength=1024):
        if not self.isConnected():
            raise ConnectError('have not connect server')
        self._lock.acquire()
        try:
            if not self.isConnected():
                raise ConnectError('have not connect to server')
            self._my_logger.info('sending str: %s ...', msg)
            self._sock.sendall(msg)
            self._my_logger.info('sent str')
            self._my_logger.info('receiving str...')
            receive_str = self._sock.recv(bufferLength)
            self._my_logger.info('received str!')
            if receive_str:
                return receive_str
            else:
                raise ConnectError('receive data is Null')
        except socket.timeout:
            raise ConnectError('socket timeout')
        except socket.error:
            raise ConnectError('socket error')
        finally:
            self._lock.release()


if __name__ == '__main__':
	#os.chdir(_FILE_PATH)

    #config_path = '../../res/input/logging_config.yaml'
    #logging.config.dictConfig(fileinterface.loadYaml(config_path))
	address = ('127.0.0.1', 2005)

	a = TcpInterface(address)
	a.connect()
	print(a.sendAndRecv("motor(1)"))
	time.sleep(1)    
	print(a.sendAndRecv("robot(6,'KENT')\n"))
	time.sleep(1)
	print(a.sendAndRecv('setSpeed(5)\n'))
	time.sleep(1)    
	print(a.sendAndRecv('setAccel(10)\n'))
	time.sleep(1)
	print(a.sendAndRecv('setMoveSpeed(5)\n'))
	time.sleep(1)    
	print(a.sendAndRecv('setMoveAccel(10)\n'))
	time.sleep(1) 
	print(a.sendAndRecv('getJoints()\n'))
	time.sleep(1)
	
	print(a.sendAndRecv('go(P1)\n'))
	time.sleep(3)
	print(a.sendAndRecv('go(P2)\n'))
	time.sleep(3)
	print(a.sendAndRecv('go(P3)\n'))
	time.sleep(3)
	print(a.sendAndRecv('go(P4)\n'))
	time.sleep(3)
	
	"""
	print(a.sendAndRecv('move(575.386, -61.792, 398.352, 25.4295, -61.5302, 137.048)\n'))
	time.sleep(5)
	print(a.sendAndRecv('move(493.698, -298.9, 387.78, -47.2949, -53.5149, -166.395)\n'))
	time.sleep(5)
	print(a.sendAndRecv('move(428.781, 1.16398, 660.271, -103.347, -33.452, -89.4438)\n'))
	time.sleep(5)
	print(a.sendAndRecv('move(428.78, 1.16307, 391.269, -103.347, -33.4523, -89.4441)\n'))
	time.sleep(5)
	print(a.sendAndRecv('move(587.352, -33.6924, 357.695, -92.6452, 0.469375, -125.099)\n'))
	time.sleep(5)
	print(a.sendAndRecv('move(455.79, 264.188, 357.7, -92.6439, 0.467502, -125.098)\n'))
	time.sleep(5)
	print(a.sendAndRecv('move(397.152, 65.1874, 124.816, -92.6433, 0.466351, -125.099)\n'))
	time.sleep(5)
	"""
