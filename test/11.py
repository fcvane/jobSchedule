#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/10 11:16
# @Author  : Fcvane
# @Param   : 
# @File    : 11.py
import os

file = open('C:\\ztesoft\\python3\\jobSchedule\\script\\fircus_dkh\\SQL\\1.sql','r')

#print (file.read())
count=0
for line in file:
    count +=1
    if line:
        lines=line[:line.find(';')]
        print (lines)
