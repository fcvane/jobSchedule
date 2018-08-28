#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/31 14:41
# @Author  : Fcvane
# @Param   : 全局变量
# @File    : UtilVariables.py

import os
import sys

#python脚本绝对路径
FILE_PATH = os.path.realpath(__file__)
#脚本路径
BIN_PATH = os.path.split(FILE_PATH)[0]
#配置文件路径
CONF_PATH = os.path.abspath(BIN_PATH + '/../conf')
#SQL文件路径
#路径下文件命名格式为 */项目/脚本类型/*
SQL_PATH = os.path.abspath(BIN_PATH + '/../script')
#日志文件路径
LOG_PATH = os.path.abspath(BIN_PATH + '/../log')
# 临时文件目录
TMP_PATH = os.path.abspath(BIN_PATH + '/../tmp')


CUR_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(CUR_PATH)
#ROOT_PATH = os.path.abspath(os.path.dirname(CUR_PATH) + os.path.sep + ".")
sys.path.append("..")
