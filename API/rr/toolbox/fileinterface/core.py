#!/usr/bin/env python
from __future__ import division, print_function
# -*- coding:utf-8 -*-
__author__ = 'hkh'
__date__ = '25/10/2016'
__version__ = '3.0'

import os
import yaml
import errno
import pickle as pk

__all__ = [
    'loadYaml',
    'loadAllYaml',
    'dumpYaml',
    'dumpAllYaml',
    'loadPk',
    'dumpPk',
    'isExist',
    'createFile',
    'createDir',
    'touchFile',
]

def loadYaml(fileName, method='r'):
    """
    Parse the first YAML document in a stream
    and produce the corresponding Python object.
    """
    with open(fileName, method) as file:
        return  yaml.load(stream=file)

def loadAllYaml(fileName, method='r'):
    """
    Parse all YAML documents in a stream
    and produce corresponding Python objects.
    """
    with open(fileName, method) as file:
        return yaml.load_all(stream=file)

def dumpYaml(data, fileName, method='w'):
    """
    Serialize a Python object into a YAML stream.
    If stream is None, return the produced string instead.
    """
    with open(fileName, method) as file:
        yaml.dump(data=data, stream=file)

def dumpAllYaml(data, fileName, method='w'):
    """
    Serialize a sequence of Python objects into a YAML stream.
    If stream is None, return the produced string instead.
    """
    with open(fileName, method) as file:
        yaml.dump_all(documents=data, stream=file)

def loadPk(fileName, method='r'):
    """
    Read a pickled object representation from the open file.
    Return the reconstituted object hierarchy specified in the file.
    """
    with open(fileName, method) as File:
        return pk.load(File)

def dumpPk(data, fileName, method='w'):
    """
    Write a pickled representation of obj to the open file.
    """
    with open(fileName, method) as File:
        pk.dump(obj=data, file=File)

def isExist(fileName):
    return os.path.exists(fileName)

def createFile(fileName):
    if not isExist(fileName):
        os.makedirs(fileName)
        return True
    return False

def createDir(dir, recursive=True):
    try:
        os.makedirs(dir)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(dir):
            return True
        else:
            return False

def touchFile(fileName):
    os.system('touch ' + fileName)