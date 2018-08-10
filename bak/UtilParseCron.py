#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/2 14:33
# @Author  : Fcvane
# @Param   : 解析 crontab 配置文件
# @File    : UtilParseCron(1).py

import time

def parseCrontab(conf_string):
    '''
    解析crontab时间配置参数
    Args:
        conf_string  配置内容(共五个值：分 时 日 月 周)
                     取值范围 分钟:0-59 小时:1-23 日期:1-31 月份:1-12 星期:0-6(0表示周日)
    Return:
    crontab_range    list格式，分 时 日 月 周 五个传入参数分别对应的取值范围
    '''
    clist = []
    conf_length = 5
    tmp_list = conf_string.split(' ')
    for val in tmp_list:
        if val:
            clist.append(val)
    if len(clist) != conf_length:
         return -1, 'config error with [%s] , the config is too long or too short , please check and try again !' % conf_string
    return 0, clist

def getCronList(conf_string):
    # 时间戳
    time_stamp = int(time.time())

    # 解析crontab时间配置参数 分 时 日 月 周 各个取值范围
    res, desc = parseCrontab(conf_string)

    if res == 0:
        cron_time = desc
    else:
        #print (desc)
        exit(-1)

    # print ("\nconfig:", conf_string)
    # print (desc)
    return {"minute": cron_time[0], "hour": cron_time[1], "day": cron_time[2], "month": cron_time[3],
            "week": cron_time[4]}

# if __name__ == '__main__':
#     cronDict = getCronList(conf_string='*/3 1-2 1-31 1-12 0-6')
#     print (cronDict['week'], cronDict['month'], cronDict['day'], cronDict['hour'], cronDict['minute'])
