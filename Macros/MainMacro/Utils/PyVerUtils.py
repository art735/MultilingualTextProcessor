# -*- coding: utf-8 -*-
import sys


def is_python2():
    return sys.version_info.major == 2


def is_python3():
    return sys.version_info.major == 3