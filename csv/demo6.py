#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-06-13 14:53
# @Author  : liupan
# @Site    : 
# @File    : demo6.py
# @Software: PyCharm

import csv

with open('data.csv', 'a', encoding='utf-8') as csvfile:
    fieldnames = ['id', 'name', 'age']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writerow({'id': '10005', 'name': '王伟', 'age': 22})