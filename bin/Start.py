#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/2 15:57
# @Author  : Fcvane
# @Param   :
# @File    : Start.py
import os
import sys
import datetime
import logging.handlers
import time
import UtilVariables
import re
from UtilParseXML import parseCFGInfo
from DbConnect import getConnect
from apscheduler.schedulers.blocking import BlockingScheduler
from concurrent.futures import ThreadPoolExecutor
from UtilPreHandle import preHandle
from apscheduler.triggers.cron import CronTrigger


LOG_PATH = UtilVariables.LOG_PATH
currDate = datetime.datetime.now().strftime('%Y-%m-%d')
logFile = LOG_PATH + os.sep + 'jobSchedule_log_{currDate}.log'.format(currDate=currDate)

# fh=logging.FileHandler(logFile,mode='a')
# fh.setLevel(logging.INFO)

ch=logging.StreamHandler()
#ch.setLevel(logging.INFO)
ch.setLevel(logging.ERROR)

formatter=logging.Formatter('%(asctime)s - %(levelname) -8s %(filename)s - %(name)s : %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
logging.basicConfig(filename=logFile,level=logging.DEBUG, format=formatter,
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger('jobSchedule_LogDetail')  # 获取logger名称
logger.setLevel(logging.INFO) #设置日志级别

# fh.setFormatter(formatter)
ch.setFormatter(formatter)
# 控制台打印
# logger.addHandler(fh)
logger.addHandler(ch)

#cli执行
def execute(cmd, errorMessage):
    exitCode = os.system(cmd)
    if exitCode != 0:
        logger.error(errorMessage)
        exit(1)

#获取文件信息
def getFileName(fileDir, fileExt):
    logger.info('解析[%s]目录下的配置文件'%fileDir)
    filenameList = []
    for root, dirs, files in os.walk(fileDir):
        for file in files:
            if os.path.splitext(file)[1] == '.{fileExt}'.format(fileExt=fileExt):
                filenameList.append(os.path.abspath(root + os.sep + file))
    return filenameList

#执行
def execProgram(array):
    scriptFile = array[0]
    fileExt = array[1]
    if fileExt != 'sql':
        if fileExt == 'py':
            program = os.popen("which python").readline()[:-1]
            # program = "C:\Anaconda3\python"
            # python执行
            logger.info(
                "[%s] %s exec start ..." % (scriptFile, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')))
            cmd = "{program} {scriptFile}".format(program=program, scriptFile=scriptFile)
            errorMessage = '[%s]执行异常，请检查脚本文件' % scriptFile
            execute(cmd, errorMessage)
            logger.info(
                "[%s] %s exec finished !" % (scriptFile, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')))

        elif fileExt == 'sh':
            program = os.popen("which sh").readline()[:-1]
            # shell执行
            logger.info(
                "[%s] %s exec start ..." % (scriptFile, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')))
            cmd = "{program} {scriptFile}".format(program=program, scriptFile=scriptFile)
            errorMessage = '[%s]执行异常，请检查脚本文件' % scriptFile
            execute(cmd, errorMessage)
            logger.info(
                "[%s] %s exec finished !" % (scriptFile, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')))
        elif fileExt == 'hive':
            program = os.popen("which hive").readline()[:-1]
            # hql执行
            logger.info(
                "[%s] %s exec start ..." % (scriptFile, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')))
            cmd = "{program} -hivevar v_date='20180828' -S -f {scriptFile}".format(program=program, scriptFile=scriptFile)
            errorMessage = '[%s]执行异常，请检查脚本文件' % scriptFile
            execute(cmd, errorMessage)
            logger.info(
                "[%s] %s exec finished !" % (scriptFile, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')))
    else:
        print ('---------------------------',scriptFile)
        conn = getConnect('fircus_dkh')
        cur = conn.cursor()
        result = preHandle(scriptFile)
        logger.info('%s exec start ...' % scriptFile)
        for line in result.split(';'):
            if len(line.strip()) != 0:
                try:
                    # print(line,'+++')
                    cur.execute(line)
                    conn.commit()
                except :
                    logger.error('%s SQL执行异常,原因如下：' % scriptFile)
                    logger.exception(sys.exc_info())
                    sys.exit()
        logger.info('%s exec finish !' % scriptFile)
        cur.close()
        conn.close()

#并发数控制2`
def poolExecProgram(fileDir, fileExt, channel):
    logger.info('任务添加并发数控制，并发数为%s'%channel)
    parameterList = []
    for scriptFile in getFileName(fileDir, fileExt):
        parameterList.append([scriptFile, fileExt])
    # print(parameterList)
    pool = ThreadPoolExecutor(int(channel))
    pool.map(execProgram,parameterList)

#解析crontab时间配置参数
def getCronList(conf_string):
    '''
        Args:
            conf_string  配置内容(共五个值：分 时 日 月 周)
                         取值范围 分钟:0-59 小时:1-23 日期:1-31 月份:1-12 星期:0-6(0表示周日)
     '''
    clist = []
    conf_length = 5
    tmp_list = conf_string.split(' ')
    for val in tmp_list:
        if val:
            clist.append(val)
        res = 0
    if len(clist) != conf_length:
        res = -1
        logger.error(
            'config error with [%s] , the config is too long or too short , please check and try again !' % conf_string)

    # 解析crontab时间配置参数 分 时 日 月 周 各个取值范围
    if res == 0:
        logger.info('[%s]cron配置正确，可正常执行 ...' % cronStr)
        cron_time = clist
    else:
        logger.error('[%s]cron配置信息有误，请检查配置信息' % cronStr)
        exit(1)
    return {"minute": cron_time[0], "hour": cron_time[1], "day": cron_time[2], "month": cron_time[3],
            "week": cron_time[4]}

if __name__ == '__main__':
    scheduler = BlockingScheduler()
    # 调用xml解析获取脚本位置信息
    config = parseCFGInfo('fircus_dkh',  'job_config.xml')
    for cronName in config.keys():
        fileExt = cronName
        cronConfig = config[cronName]
        if cronConfig['enable'] == 'Ture':
            cronStr = cronConfig['cron']
            fileDir = cronConfig['path']
            channel = cronConfig['channel']
            print (fileDir, fileExt, channel,cronStr)
            #调用主程序
            def schedJob():
                logger.info('执行任务 ...')
                print(fileDir, fileExt, channel)
                nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                poolExecProgram(fileDir, fileExt, channel)
                # 打印当前时间
                print('nowTime: ' + nowTime)

            #获取时间
            cronDict = getCronList(conf_string=cronStr)
            scheduler.add_job(schedJob, 'cron',second = '*')
            trigger = CronTrigger(day_of_week=cronDict['week'], month=cronDict['month'], day=cronDict['day'],
                                  hour=cronDict['hour'], minute=cronDict['minute'])
            print(cronDict['week'], cronDict['month'], cronDict['day'], cronDict['hour'], cronDict['minute'])
            # scheduler.add_job(schedJob, 'cron', day_of_week=cronDict['week'], month=cronDict['month'], day=cronDict['day'], hour=cronDict['hour'], minute=cronDict['minute'])
            # scheduler.add_job(schedJob, trigger)
            trigger = CronTrigger(second='*')
            scheduler.add_job(schedJob, trigger)
            print('Press Ctrl + C to exit')
            try:
                # 采用的是阻塞的方式，只有一个线程专职做调度的任务
                logger.info('调度入口 ...')
                scheduler.start()
            except (KeyboardInterrupt, SystemExit):
                logger.error('任务异常退出,请检查调度是否正确.')
                scheduler.shutdown()
                print('Exit The Job!')

