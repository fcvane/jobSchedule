#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/2 14:33
# @Author  : Fcvane
# @Param   : 解析 crontab 配置文件
# @File    : UtilParseCron(1).py

'''
1.解析 crontab 配置文件中的五个数间参数(分 时 日 月 周)，获取他们对应的取值范围
2.将时间戳与crontab配置中一行时间参数对比，判断该时间戳是否在配置设定的时间范围内
'''

import re, time, sys

def match_cont(patten, cont):
    '''
    正则匹配(精确符合的匹配)
    Args:
        patten 正则表达式
        cont____ 匹配内容
    Return:
        True or False
    '''
    res = re.match(patten, cont)
    if res:
        return True
    else:
        return False

def handle_num(val, ranges=(0, 60), res=[]):
    '''处理纯数字'''
    val = int(val)
    if val >= ranges[0] and val <= ranges[1]:
        res.append(val)
    return res

def handle_nlist(val, ranges=(0, 60), res=[]):
    '''处理数字列表 如 1,2,3,6'''
    val_list = val.split(',')
    for tmp_val in val_list:
        tmp_val = int(tmp_val)
        if tmp_val >= ranges[0] and tmp_val <= ranges[1]:
            res.append(tmp_val)
    return res

def handle_star(val, ranges=(0, 60), res=[]):
    '''处理星号'''
    if val == '*':
        tmp_val = ranges[0]
        while tmp_val <= ranges[1]:
            res.append(tmp_val)
            tmp_val = tmp_val + 1
    return res

def handle_starnum(val, ranges=(0, 60), res=[]):
    '''星号/数字 组合 如 */3'''
    tmp = val.split('/')
    val_step = int(tmp[1])
    if val_step < 1:
        return res
    val_tmp = int(tmp[1])
    while val_tmp <= ranges[1]:
        res.append(val_tmp)
        val_tmp = val_tmp + val_step
    return res

def handle_range(val, ranges=(0, 60), res=[]):
    '''处理区间 如 8-20'''
    tmp = val.split('-')
    range1 = int(tmp[0])
    range2 = int(tmp[1])
    tmp_val = range1
    if range1 < 0:
        return res
    while tmp_val <= range2 and tmp_val <= ranges[1]:
        res.append(tmp_val)
        tmp_val = tmp_val + 1
    return res

def handle_rangedv(val, ranges=(0, 60), res=[]):
    '''处理区间/步长 组合 如 10-20/3 '''
    tmp = val.split('/')
    range2 = tmp[0].split('-')
    val_start = int(range2[0])
    val_end = int(range2[1])
    val_step = int(tmp[1])
    if (val_step < 1) or (val_start < 0):
        return res
    val_tmp = val_start
    while val_tmp <= val_end and val_tmp <= ranges[1]:
        res.append(val_tmp)
        val_tmp = val_tmp + val_step
    return res

def handle_nrangedv(val, ranges=(0, 60), res=[]):
    '''区间/步长 列表 组合，如 10-20/3,21,22,34'''
    val_list = val.split(',')
    tmp = val_list[0].split('/')
    range2 = tmp[0].split('-')
    val_start = int(range2[0])
    val_end = int(range2[1])
    val_step = int(tmp[1])
    if (val_step < 1) or (val_start < 0):
        return res
    val_tmp = val_start
    while val_tmp <= val_end and val_tmp <= ranges[1]:
        res.append(val_tmp)
        val_tmp = val_tmp + val_step
    for i in range(1,len(val_list)):
        tmp_val = int(val_list[i])
        if tmp_val >= ranges[0] and tmp_val <= ranges[1]:
            res.append(tmp_val)
        return res

def parse_conf(conf, ranges=(0, 60), res=[]):
    '''解析crontab 五个时间参数中的任意一个'''
    # 去除空格，再拆分
    conf = conf.strip(' ').strip(' ')
    conf_list = conf.split(',')
    other_conf = []
    number_conf = []

    for conf_val in conf_list:
        if match_cont(PATTEN['number'], conf_val):
            # 记录拆分后的纯数字参数
            number_conf.append(conf_val)
        else:
            # if conf_val == '':
            #     return res
            #     break
            # 记录拆分后纯数字以外的参数，如通配符 * , 区间 0-8, 及 0－8/3 之类
            other_conf.append(conf_val)
    if other_conf:
        # 处理纯数字外各种参数
        for conf_val in other_conf:
            for key, ptn in PATTEN.items():
                if match_cont(ptn, conf_val):
                    res = PATTEN_HANDLER[key](val=conf_val, ranges=ranges, res=res)
    if number_conf:
        if len(number_conf) > 1 or other_conf:
            # 纯数字多于1，或纯数字与其它参数共存，则数字作为时间列表
            res = handle_nlist(val=','.join(number_conf), ranges=ranges, res=res)
        else:
            # 只有一个纯数字存在，则数字为时间 间隔
            res = handle_num(val=number_conf[0], ranges=ranges, res=res)
    return res

def parse_crontab_time(conf_string):
    '''
    解析crontab时间配置参数
    Args:
        conf_string  配置内容(共五个值：分 时 日 月 周)
                     取值范围 分钟:0-59 小时:1-23 日期:1-31 月份:1-12 星期:0-6(0表示周日)
    Return:
    crontab_range    list格式，分 时 日 月 周 五个传入参数分别对应的取值范围
    '''
    time_limit = ((0, 59), (0, 23), (1, 31), (1, 12), (0, 6))
    crontab_range = []
    clist = []
    conf_length = 5
    tmp_list = conf_string.split(' ')
    for val in tmp_list:
        if val:
            clist.append(val)
    if len(clist) != conf_length:
         return -1, 'config error with [%s] , the config is too long or too short , please check and try again !' % conf_string
    cindex = 0
    for conf in clist:
            res_conf = []
            res_conf = parse_conf(conf, ranges=time_limit[cindex], res=res_conf)
            if not res_conf:
                return -2, 'config error with [%s] , the config is bad configuration , please check and try again !' % conf_string
            crontab_range.append(res_conf)
            cindex = cindex + 1
    return 0, crontab_range

# crontab时间参数各种写法的正则匹配
PATTEN = {
    # 纯数字
    'number': '^[0-9]+$',
    # 数字列表,如 1,2,3,6
    'num_list': '^[0-9]+([,][0-9]+)+$',
    # 星号 *
    'star': '^\*$',
    # 星号/数字 组合，如 */3
    'star_num': '^\*\/[0-9]+$',
    # 区间 如 8-20
    'range': '^[0-9]+[\-][0-9]+$',
    # 区间/步长 组合 如 10-20/3
    'range_div': '^[0-9]+[\-][0-9]+[\/][0-9]+$',
    # 区间/步长 列表 组合，如 10-20/3,21,22,34
    'range_div_list':'^([0-9]+[\-][0-9]+[\/][0-9]+)([,][0-9]+)+$'
}
# 各正则对应的处理方法
PATTEN_HANDLER = {
    'number': handle_num,
    'num_list': handle_nlist,
    'star': handle_star,
    'star_num': handle_starnum,
    'range': handle_range,
    'range_div': handle_rangedv,
    'range_div_list':handle_nrangedv
}

def getCronList(conf_string):
    # 时间戳
    time_stamp = int(time.time())

    # 解析crontab时间配置参数 分 时 日 月 周 各个取值范围
    res, desc = parse_crontab_time(conf_string)

    if res == 0:
        cron_time = desc
    else:
        #print (desc)
        exit(-1)

    # print ("\nconfig:", conf_string)
    print (desc)
    return {"minute": cron_time[0], "hour": cron_time[1], "day": cron_time[2], "month": cron_time[3],
            "week": cron_time[4]}

# if __name__ == '__main__':
#     cronDict = getCronList(conf_string='* * * * *')
#     print (cronDict['week'], cronDict['month'], cronDict['day'], cronDict['hour'], cronDict['minute'])
