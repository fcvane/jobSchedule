#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/9 11:13
# @Author  : Fcvane
# @Param   : 
# @File    : 10.py
try:
    import xml.etree.cElementTree as etree
except ImportError:
    import xml.etree.ElementTree as etree
import sys

result = {}
try:
    tree = etree.parse('C:/ztesoft/python3/jobSchedule/conf/fircus_dkh/job_config.xml')
    # 获得子元素
    elemlist = tree.findall('task')
    # 遍历task所有子元素
    for elem in elemlist:
        array = []
        for child in elem.getchildren():
            #print (child.tag, ":", child.attrib, ":", child.text)
            array += [child.text]
        result[elem.attrib['type']] = array
        #print (array,"-----",result)
except Exception as e:  # 捕获除与程序退出sys.exit()相关之外的所有异常
    print("parse test.xml fail!")
    sys.exit()
print (result)