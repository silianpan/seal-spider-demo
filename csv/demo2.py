#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-06-13 14:52
# @Author  : liupan
# @Site    : 
# @File    : demo2.py
# @Software: PyCharm

import csv

with open('data.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=' ')
    writer.writerow(['id', 'name', 'age'])
    writer.writerow(['10001', 'Mike', 20])
    writer.writerow(['10002', 'Bob', 22])
    writer.writerow(['10003', 'Jordan', 21])