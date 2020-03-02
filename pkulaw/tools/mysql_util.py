#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/2 下午5:13
# @Author  : liupan
# @Site    : 
# @File    : MysqlUtil.py
# @Software: PyCharm

import pymysql


class MysqlUtil:
    def __init__(self):
        self.is_connected = False
        try:
            self.conn = pymysql.connect(host='localhost', user='root', password='Asdf@123', port=3306, db='pkulaw_other')
            self.cursor = self.conn.cursor()
            self.is_connected = True
        except Exception:
            print("Connect Mysql Error!")

    def insert(self, tablename = None, **values):
