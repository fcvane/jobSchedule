#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/14 18:56
# @Author  : Fcvane
# @Param   : 
# @File    : UtilPreHandle.py

import re
import os
import sys
import logging
import  UtilVariables
import datetime

LOG_PATH = UtilVariables.LOG_PATH
currDate = datetime.datetime.now().strftime('%Y-%m-%d')
logFile = LOG_PATH + os.sep + 'jobSchedule_log_{currDate}.log'.format(currDate=currDate)

# fh=logging.FileHandler(logFile,mode='a')
# fh.setLevel(logging.INFO)

ch=logging.StreamHandler()
#ch.setLevel(logging.INFO)
ch.setLevel(logging.ERROR)

formatter=logging.Formatter('%(asctime)s - %(levelname) -8s %(filename)s - %(name)s : %(message)s',
                    datefmt='%Y-%m-%d %H:%M:[%s]')
logging.basicConfig(filename=logFile,level=logging.DEBUG, format=formatter,
                    datefmt='%Y-%m-%d %H:%M:[%s]')
logger = logging.getLogger('filePreHandle_LogDetail')  # 获取logger名称
logger.setLevel(logging.INFO) #设置日志级别

# fh.setFormatter(formatter)
ch.setFormatter(formatter)
# 控制台打印
# logger.addHandler(fh)
logger.addHandler(ch)

#解析文件预处理
def preHandle(r_filename):
    # 初始化目标数组
    array = []
    comm = []
    nor_array = []
    s = []
    e = []
    nor_array4 = []
    normal = []
    # 文件不存在，退出程序
    if not os.path.isfile(r_filename):
        logger.error ('[%s] 文件不存在' % r_filename)
        sys.exit()
    try:
        file = open(r_filename, 'r', encoding="utf8")
        for lines in file.readlines():
            if not lines:
                logger.info ('[%s] 没有内容' % r_filename)
                # break
            array.append(lines)
        # logger.info('[%s] 编码为utf-8 ... ' % r_filename)
        file.close()
    except:
        # logger.info('[%s] 编码为gbk ...'%r_filename)
        file = open(r_filename, 'r')
        for lines in file.readlines():
            if not lines:
                logger.info ('[%s] 没有内容' % r_filename)
                # break
            array.append(lines)
        file.close()
    # 删除注释1
    for i in array:
        if len (re.findall(re.compile(r'.*?--.*?', re.S), str(i))) > 0 and ''.join(re.findall(re.compile(r'.*?--.*?', re.S), str(i))).split('--') [0] != '':
            # print (i,'--')
            #comm.append(i.split('--')[0])
            nor_array.append(i.split('--')[0])
        else:
            nor_array.append(i)
    # 删除注释2
    for i in nor_array:
        if len(re.findall(re.compile(r'/\*.*?', re.S), str(i))) > 0:
            s.append(i)
    for i in nor_array:
        if len(re.findall(re.compile(r'([\s\S]*?)\*/', re.S), str(i))) > 0:
            e.append(i)
    ss = []
    ee = []
    # 处理列表中重复出现的注释
    if len(s) != len (e):
        logger.error('[%s] comments is not formal !!.' %r_filename)
        sys.exit()
    else:
        for k,v in enumerate(nor_array):
            for i in range(0, len(s)):
                if v == s[i]:
                    ss.append(k)
                if v == e[i]:
                    ee.append(k)
    # 去重
    ee = list(set(ee))
    # ss,ee降序排列
    sss = sorted(ss, reverse=True)
    eee = sorted(ee, reverse=True)
    # 删除区间数据
    for i in range(0,len(sss)):
        del nor_array[ sss[i] : eee[i]+1 ]
    # 删除注释4
    for i in nor_array:
        if len(re.findall(re.compile(r".*?([\u4e00-\u9fa5]+).*?", re.S), str(i))) > 0 and re.findall(re.compile(r".*?\'.*?([\u4e00-\u9fa5]+).*?\'.*?", re.S), str(i))==[]:
             # print (i,'---------------------')
             pass
        else:
            nor_array4.append(i)
    # 删除文本换行符
    for line in nor_array4:
        normal.append (line.replace('\n', ' '))
    result = (''.join(normal))
    # print(nor_array,'----------3')
    # print(nor_array4,'----------')
    return  result

if __name__ == '__main__':

    result = preHandle('C:/ztesoft/python3/jobSchedule/script/fircus_dkh/SQL/METRIC_GATHER_AREA_3200002.sql')
    print (result)
