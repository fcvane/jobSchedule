#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/2 14:48
# @Author  : Fcvane
# @Param   : 
# @File    : 3.py


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
    print(res)


def handle_nlist(val, ranges=(0, 60), res=[]):
    '''处理数字列表 如 1,2,3,6'''
    val_list = val.split(',')
    for tmp_val in val_list:
        tmp_val = int(tmp_val)
        if tmp_val >= ranges[0] and tmp_val <= ranges[1]:
            res.append(tmp_val)
    print(res)


def handle_star(val, ranges=(0, 60), res=[]):
    '''处理星号'''
    if val == '*':
        tmp_val = ranges[0]
        while tmp_val <= ranges[1]:
            res.append(tmp_val)
            tmp_val = tmp_val + 1
    print(res)


def handle_starnum(val, ranges=(0, 60), res=[]):
    '''星号/数字 组合 如 */3'''
    tmp = val.split('/')
    val_step = int(tmp[1])
    if val_step < 1:
        print(res)
    val_tmp = int(tmp[1])
    while val_tmp <= ranges[1]:
        res.append(val_tmp)
        val_tmp = val_tmp + val_step
    print(res)


def handle_range(val, ranges=(0, 60), res=[]):
    '''处理区间 如 8-20'''
    tmp = val.split('-')
    range1 = int(tmp[0])
    range2 = int(tmp[1])
    tmp_val = range1
    if range1 < 0:
        print(res)
    while tmp_val <= range2 and tmp_val <= ranges[1]:
        res.append(tmp_val)
        tmp_val = tmp_val + 1
    print(res)


def handle_rangedv(val, ranges=(0, 60), res=[]):
    '''处理区间/步长 组合 如 8-20/3 '''
    tmp = val.split('/')
    range2 = tmp[0].split('-')
    val_start = int(range2[0])
    val_end = int(range2[1])
    val_step = int(tmp[1])
    if (val_step < 1) or (val_start < 0):
        print(res)
    val_tmp = val_start
    while val_tmp <= val_end and val_tmp <= ranges[1]:
        res.append(val_tmp)
        val_tmp = val_tmp + val_step
    print(res)

def handle_nrangedv(val, ranges=(0, 60), res=[]):
    '''区间/步长 列表 组合，如 8-20/3,21,22,34'''
    val_list = val.split(',')
    tmp = val_list[0].split('/')
    range2 = tmp[0].split('-')
    val_start = int(range2[0])
    val_end = int(range2[1])
    val_step = int(tmp[1])
    if (val_step < 1) or (val_start < 0):
        print(res)
    val_tmp = val_start
    while val_tmp <= val_end and val_tmp <= ranges[1]:
        res.append(val_tmp)
        val_tmp = val_tmp + val_step
    for i in range(1,len(val_list)):
        tmp_val = int(val_list[i])
        if tmp_val >= ranges[0] and tmp_val <= ranges[1]:
            res.append(tmp_val)
        print(res)


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
    # 区间/步长 组合 如 8-20/3
    'range_div': '^[0-9]+[\-][0-9]+[\/][0-9]+$',
    # 区间/步长 列表 组合，如 8-20/3,21,22,34
    'range_div_list':'^([0-9]+[\-][0-9]+[\/][0-9]+)([,][0-9]+)+$'
}
# 各正则对应的处理方法
PATTEN_HANDLER = {
    'number': handle_num,
    'num_list': handle_nlist,
    'star': handle_star,
    'star_num': handle_starnum,
    'range': handle_range,
    'range_div': handle_rangedv

}

handle_num('1')
handle_nlist('1,2,3,4,5')
handle_star('*')
handle_starnum('*/3')
handle_range('10-20')
handle_rangedv('10-20/3')
handle_nrangedv('10-20/3,21,22,34')