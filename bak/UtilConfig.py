#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/2 15:43
# @Author  : Fcvane
# @Param   :
# @File    : UtilConfig.py
config={
    "job1": {
		"name":"test0801",
		"author": "fccc",
        "fileDir": "C:/ztesoft/python3/jobSchedule/conf/cron/Python",
        "fileExt": "py",
        "dbType":"",
        "cron": "* * * * *",
        "channel": 3,
		"enable": "Ture"
    },
    "job2": {
		"name":"test0802",
		"author": "fccc",
        "fileDir": "C:/ztesoft/python3/jobSchedule/conf/cron/Shell",
        "fileExt": "sh",
        "dbType":"",
        "cron": "* * * * *",
        "channel": 3,
		"enable": "Ture"
    },
    "job3": {
		"name":"test0802",
		"author": "fccc",
        "fileDir": "C:/ztesoft/python3/jobSchedule/conf/cron/SQL",
        "fileExt": "sql",
        "dbType":"ORACLE",
        "cron": "* * * * *",
        "channel": 3,
		"enable": "Ture"
    },
    "job4": {
		"name":"test0802",
		"author": "fccc",
        "fileDir": "C:/ztesoft/python3/jobSchedule/conf/cron/SQL",
        "fileExt": "sql",
        "dbType":"MYSQL",
        "cron": "* * * * *",
        "channel": 3,
		"enable": "False"
    }
}