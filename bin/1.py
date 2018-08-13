#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/13 10:38
# @Author  : Fcvane
# @Param   : 
# @File    : 1.py

import cx_Oracle
import traceback
from dbConnect import getConnect

scriptFile = 'C:/ztesoft/python3/jobSchedule/script/fircus_dkh/SQL/METRIC_VALUE_CUST_5210005.sql'
file = open(scriptFile,'r')

conn = getConnect('fircus_dkh')
cur = conn.cursor()

for line in file.read().split(';'):
    if line:
        try:
            cur.execute(line)
            conn.commit()
            cur.close()
            conn.close()
            file.close()
        except cx_Oracle.IntegrityError as e:
            print( repr(e),'--------------------',e.message)



