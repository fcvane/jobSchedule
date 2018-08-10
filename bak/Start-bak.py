#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/2 15:57
# @Author  : Fcvane
# @Param   : 
# @File    : Start.py
import datetime
import logging.handlers
import os
import time
from concurrent.futures import ThreadPoolExecutor

import cx_Oracle
from apscheduler.schedulers.blocking import BlockingScheduler

import UtilVariables
from bak.UtilConfig import config

LOG_PATH = UtilVariables.LOG_PATH
currDate = datetime.datetime.now().strftime('%Y-%m-%d')
logFile = LOG_PATH + os.sep + 'cron_run_{currDate}.log'.format(currDate=currDate)

logging.basicConfig(filename=logFile,level=logging.DEBUG, format='%(asctime)s - %(levelname) -8s %(filename)s - %(name)s : %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger('jobSchedule_LogDetail')  # 获取logger名称
logger.setLevel(logging.INFO) #设置日志级别

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

#数据库连接
# 执行sql
def conOracle(sql):
    logger.info('开始执行Oracle语句 ...')
    #conn = cx_Oracle.connect('DC_PD', 'DC_PD', '10.45.59.186:1521/orcl')
    conn = cx_Oracle.connect('ogg', 'ogg', '10.45.28.209:1521/orcl')
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        logger.info('执行Oracle语句成功 !')
    except:
        logger.error('执行Oracle语句失败 !')
        exit(0)
    # if re.findall(re.compile(r'.*?SELECT.*?', re.S), sql) and not re.findall(re.compile(r'.*?INSERT.*?', re.S), sql):
    #     result = cursor.fetchall()
    #     return result
    # elif re.findall(re.compile(r'.*?SELECT.*?NEXTVAL.*?', re.S), sql):
    #     result = cursor.fetchall()
    #     return result
    conn.commit()
    cursor.close()
    conn.close()

#执行
def execProgram(array):
    scriptFile = array[0]
    fileExt = array[1]
    if fileExt == 'py':
        #program = os.popen("which python").readline()[:-1]
        program = "C:\Anaconda3\python"
    # elif fileExt == 'sh':
    #     program = os.popen("which sh").readline()[:-1]
    # elif fileExt == 'sql':
    #     program = os.popen("which sql").readline()[:-1]

    # python和shell执行

    logger.info("[%s] %s exec start ..."%(scriptFile,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')))
    cmd = "{program} {scriptFile}".format(program=program, scriptFile=scriptFile)
    errorMessage = '[%s]执行异常，请检查脚本文件' % scriptFile
    execute(cmd, errorMessage)
    logger.info("[%s] %s exec finished !" % (scriptFile, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')))

#并发数控制2`
def poolExecProgram(fileDir, fileExt, channel):
    logger.info('任务添加并发数控制，并发数为%s'%channel)
    parameterList = []
    for scriptFile in getFileName(fileDir, fileExt):
        parameterList.append([scriptFile, fileExt])
    # print(parameterList)
    pool = ThreadPoolExecutor(channel)
    pool.map(execProgram,parameterList)

def parseCrontab(conf_string):
    '''
    解析crontab时间配置参数
    Args:
        conf_string  配置内容(共五个值：分 时 日 月 周)
                     取值范围 分钟:0-59 小时:1-23 日期:1-31 月份:1-12 星期:0-6(0表示周日)
    Return:
    '''
    clist = []
    conf_length = 5
    tmp_list = conf_string.split(' ')
    for val in tmp_list:
        if val:
            clist.append(val)
    if len(clist) != conf_length:
         return -1, logger.error('config error with [%s] , the config is too long or too short , please check and try again !' % conf_string)
    return 0, clist

def getCronList(conf_string):
    # 时间戳
    time_stamp = int(time.time())
    # 解析crontab时间配置参数 分 时 日 月 周 各个取值范围
    res, desc = parseCrontab(conf_string)
    if res == 0:
        logger.info('[%s]cron配置正确，可正常执行 ...' % cronStr)
        cron_time = desc
    else:
        logger.error('[%s]cron配置信息有误，请检查配置信息' % cronStr)
        exit(1)
    return {"minute": cron_time[0], "hour": cron_time[1], "day": cron_time[2], "month": cron_time[3],
            "week": cron_time[4]}

if __name__ == '__main__':
    scheduler = BlockingScheduler()
    for cronName in config.keys():
        cronConfig = config[cronName]
        if cronConfig['enable'] == "Ture":
            cronStr = cronConfig['cron']
            fileDir = cronConfig['fileDir']
            fileExt = cronConfig['fileExt']
            channel = cronConfig['channel']
            print(fileDir, fileExt, channel, cronStr)
            #调用主程序
            def schedJob():
                logger.info('任务入口，开始调用任务 ...')
                #parallelExecProgram(fileDir, fileExt, channel)
                poolExecProgram(fileDir, fileExt, channel)
                # 打印当前时间
                nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print('nowTime: ' + nowTime)

            #获取时间
            cronDict = getCronList(conf_string=cronStr)
            print(cronDict['week'], cronDict['month'], cronDict['day'], cronDict['hour'], cronDict['minute'])
            #scheduler.add_job(schedJob, 'cron', day_of_week=cronDict['week'], month=cronDict['month'], day=cronDict['day'], hour=cronDict['hour'], minute=cronDict['minute'])
            scheduler.add_job(schedJob, 'cron',second=5)
            print('Press Ctrl + C to exit')
            try:
                # 采用的是阻塞的方式，只有一个线程专职做调度的任务
                logger.info('调度入口 ...')
                scheduler.start()
            except (KeyboardInterrupt, SystemExit):
                logger.error('任务异常退出,请检查调度是否正确.')
                scheduler.shutdown()
                print('Exit The Job!')
