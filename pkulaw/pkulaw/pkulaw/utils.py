#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-02-05 15:46
# @Author  : liupan
# @Site    : 
# @File    : utils.py
# @Software: PyCharm

from datetime import datetime


def is_expired(dt):
    """
    判断时间是否过期
    :param dt:日期字符串
    :return:True or False
    """
    if isinstance(dt, str):
        dt = datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')
        return datetime.now() > dt
