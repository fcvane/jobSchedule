#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/4 11:16
# @Author  : Fcvane
# @Param   : 
# @File    : 4.py
import time
import threadpool
def sayhello(str):
    print ("Hello ",str)
    time.sleep(2)

name_list =['aa','bb','cc']
start_time = time.time()
pool = threadpool.ThreadPool(10)
requests = threadpool.makeRequests(sayhello, name_list)
[pool.putRequest(req) for req in requests]
pool.wait()



