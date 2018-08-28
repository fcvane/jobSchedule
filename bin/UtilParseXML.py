#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/9 10:46
# @Author  : Fcvane
# @Param   : 
# @File    : UtilParseXML.py
import sys
import os
import datetime
import logging
import UtilVariables
try:
    import xml.etree.cElementTree as etree
except ImportError:
    import xml.etree.ElementTree as etree
LOG_PATH = UtilVariables.LOG_PATH
currDate = datetime.datetime.now().strftime('%Y-%m-%d')
logFile = LOG_PATH + os.sep + 'jobSchedule_log_{currDate}.log'.format(currDate=currDate)

logging.basicConfig(filename=logFile,level=logging.DEBUG, format='%(asctime)s - %(levelname) -8s %(filename)s - %(name)s : %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger('xmlParse_LogDetail')  # 获取logger名称
logger.setLevel(logging.INFO) #设置日志级别


'''
解析脚本参数集 根目录为：C:/ztesoft/python3/jobSchedule/
格式为：
<?xml version='1.0' encoding='utf-8'?>
<configuration>
    <task type ="py">
        <path>C:/ztesoft/python3/jobSchedule/script/fircus_dkh/Python</path>
        <cron>* * * * *</cron>
        <channel>3</channel>
        <enable>Ture</enable>
    </task>
</configuration>
'''
# 解析项目脚本配置文件
# 所以配置文件都规定为小写
def parseCFGInfo(program,taskName):
    CONF_PATH = UtilVariables.CONF_PATH
    PROGRAM_PATH = CONF_PATH + os.sep + program
    logger.info('parse %s 目录下的文件.' % PROGRAM_PATH)
    result = {}
    try:
        logger.info( '%s parse start ...' %(PROGRAM_PATH + os.sep + taskName))
        tree = etree.parse(PROGRAM_PATH + os.sep + taskName)
        # 获得子元素
        elemlist = tree.findall('task')
        # 遍历task所有子元素
        for elem in elemlist:
            array = {}
            for child in elem.getchildren():
                # print (child.tag, ":", child.attrib, ":", child.text)
                array[child.tag] = child.text
            result[elem.attrib['type']] = array
            # print (array,"-----",result)
        logger.info('%s parse finished !.' % (PROGRAM_PATH + os.sep + taskName))
    except Exception as e:  # 捕获除与程序退出sys.exit()相关之外的所有异常
        logger.error('parse test.xml fail !!.')
        print('parse test.xml fail !!.')
        sys.exit()
    #print(result)
    return result

'''
解析数据库参数集 根目录为：C:/ztesoft/python3/jobSchedule/
格式为：
<?xml version='1.0' encoding='utf-8'?>
<configuration>
    <db type="oracle">
        <host>10.45.28.209</host>
        <port>1521</port>
        <sid>orcl</sid>
        <server_name></server_name>
        <username>ogg</username>
        <password>ogg</password>
    </db>
</configuration>
'''
def dbCFGInfo(program):
    CONF_PATH = UtilVariables.CONF_PATH
    taskName = CONF_PATH + os.sep + 'db_{program}.xml'.format(program = program)
    logger.info('parse %s 目录下的db_%s.xml文件.' % (CONF_PATH, program))
    result = {}
    try:
        logger.info('%s parse start ...' % taskName)
        tree = etree.parse(taskName)
        # 获得子元素
        elemlist = tree.findall('db')
        # 遍历task所有子元素
        for elem in elemlist:
            array = {}
            for child in elem.getchildren():
                # print (child.tag, ":", child.attrib, ":", child.text)
                array[child.tag] = child.text
            result[elem.attrib['type']] = array
            # print (array,"-----",result)
        logger.info('%sparse finished !.' % (taskName))
    except Exception as e:  # 捕获除与程序退出sys.exit()相关之外的所有异常
        logger.error('parse test.xml fail !!.')
        print('parse test.xml fail !!.')
        sys.exit()
    # print(result)
    return result

if __name__ == '__main__':
    # programConfig = parseCFGInfo('fircus_dkh',  'job_config.xml')
    # print (programConfig)
    dbConfig = dbCFGInfo('fircus_dkh')
    print(dbConfig)
