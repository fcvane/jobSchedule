#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/13 11:15
# @Author  : Fcvane
# @Param   : 
# @File    : 12.py
import traceback

try:
    1/0
except Exception as e:
    print ('str(Exception):\t', str(Exception))
    print ('str(e):\t\t'), str(e)
    print ('repr(e):\t', repr(e),'-------------------------')
    print ('e.message:\t', e.message,'---------')