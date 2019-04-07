#!/usr/bin/env python
from __future__ import division, print_function

"""
io is a library that includes several functions of file interface.
"""

from .core import *

from numpy.testing.nosetester import NoseTester
test = NoseTester().test
bench = NoseTester().bench
