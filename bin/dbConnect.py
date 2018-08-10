#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/7 10:31
# @Author  : Fcvane
# @Param   : 
# @File    : dbConnect.py

import os,sys
import datetime
import logging
import cx_Oracle
import psycopg2
import pymysql
import UtilVariables
from UtilParseXML import dbCFGInfo
try:
    import xml.etree.cElementTree as etree
except ImportError:
    import xml.etree.ElementTree as etree
LOG_PATH = UtilVariables.LOG_PATH
currDate = datetime.datetime.now().strftime('%Y-%m-%d')
logFile = LOG_PATH + os.sep + 'jobSchedule_log_{currDate}.log'.format(currDate=currDate)

logging.basicConfig(filename=logFile,level=logging.DEBUG, format='%(asctime)s - %(levelname) -8s %(filename)s - %(name)s : %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger('xmlDB_LogDetail')  # 获取logger名称
logger.setLevel(logging.INFO) #设置日志级别

# 获取数据库连接
def getConnect(program):
    config = dbCFGInfo(program)
    for cronName in config.keys():
        dbType = cronName
        cronConfig = config[cronName]
        if cronConfig['enable'] == 'Ture':
            host = cronConfig['host']
            port = cronConfig['port']
            sid = cronConfig['sid']
            serverName = cronConfig['serverName']
            userName = cronConfig['userName']
            passWord = cronConfig['passWord']
            #print(dbType, host, port, sid, serverName, userName, passWord)
            try:
                if dbType == 'oracle':
                    if sid is None or sid == '':
                        logger.error ('sid not exists , the %s config is error !'%program)
                        sys.exit()
                    else:
                        logger.info('exec connect oracle start ...')
                        connect = cx_Oracle.connect(userName, passWord,
                                                    '{host}:{port}/{sid}'.format(host = host, port = port , sid = sid))
                        logger.info('connect oracle sucessful ...')
                elif dbType == 'mysql':
                    if serverName is None or sid == '':
                        logger.error('serverName not exists , the %s config is error !' % program)
                        sys.exit()
                    else:
                        logger.info('exec connect mysql start ...')
                        connect = pymysql.connect(host = host, port = int(port), user = userName, passwd = passWord, db= serverName, charset='utf8')
                        logger.info('connect mysql sucessful ...')
                elif dbType == 'postgresql':
                        logger.info('exec connect postgresql start ...')
                        connect = psycopg2.connect(database= serverName, user = userName, password = passWord, host = host, port = port)
                        logger.info('connect postgresql sucessful ...')
            except:
                logger.info('connect to db error!')
            return connect
#
# #执行指定目录下的.sql文件
# def execute_sql(conn, path):
#     os.chdir(path)
#     for each in os.listdir("."):
#         count = 0   #读取行数
#         sql = ""    #拼接的sql语句
#         if "hisdatastock_replace.sql" in each:
#             with open(each, "r", encoding="utf-8") as f:
#                 for each_line in f.readlines():
#                     # 过滤数据
#                     if not each_line or each_line == "\n":
#                         continue
#                     # 读取2000行数据，拼接成sql
#                     elif count < 20000:
#                         sql += each_line
#                         count += 1
#                     # 读取达到2000行数据，进行提交，同时，初始化sql，count值
#                     else:
#                         cur.execute(sql)
#                         conn.commit()
#                         sql = each_line
#                         count = 1
#                 # 当读取完毕文件，不到2000行时，也需对拼接的sql 执行、提交
#                 if sql:
#                     cur.execute(sql)
#                     conn.commit()

if __name__ == '__main__':
    # conn = getConnect('fircus_dkh')
    # cur = conn.cursor()
    # cur.execute('select * from ttable_0409')
    # result = cur.fetchall()
    # print (result)

    conn = getConnect('fircus_dkh')
    cur = conn.cursor()
    cur.execute('SELECT * FROM testdb.company')
    result = cur.fetchall()
    print (result)
    cur.close()
    conn.close()
