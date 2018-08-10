#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/2 15:38
# @Author  : Fcvane
# @Param   : 
# @File    : UtilLogRecord.py
import os
import datetime
import logging.handlers


def logRecord(scriptFile):
    currDate = datetime.datetime.now().strftime('%Y-%m-%d')
    logFile = '../log/cron_run_{currDate}.log'.format(currDate=currDate)

    handler = logging.handlers.RotatingFileHandler(logFile, maxBytes=1024 * 1024, backupCount=5)  # 实例化handler
    fmt = '%(asctime)s - %(name)s - %(message)s '
          #- {scriptFile} '.format(scriptFile=scriptFile)

    formatter = logging.Formatter(fmt)  # 实例化formatterWW
    handler.setFormatter(formatter)  # 为handler添加formatter

    logger = logging.getLogger('jobSchedule_LogDetail')  # 获取logger名称
    logger.addHandler(handler)  # 为logger添加handler
    logger.setLevel(logging.DEBUG) #设置日志级别

    logger.info('{scriptFile} info message'.format(scriptFile=scriptFile))
    logger.debug('{scriptFile} debug message'.format(scriptFile=scriptFile))