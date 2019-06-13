#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-06-13 14:54
# @Author  : liupan
# @Site    : 
# @File    : demo7.py
# @Software: PyCharm

import csv

with open('data.csv', 'r', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        print(row)