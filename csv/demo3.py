#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-06-13 14:52
# @Author  : liupan
# @Site    : 
# @File    : demo3.py
# @Software: PyCharm

import csv

with open('data.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['id', 'name', 'age'])
    writer.writerows([['10001', 'Mike', 20], ['10002', 'Bob', 22], ['10003', 'Jordan', 21]])
