#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/2 下午5:13
# @Author  : liupan
# @Site    :
# @File    : mysql_util.py
# @Software: PyCharm

import logging

import pymysql

logger = logging.getLogger(__name__)


class MysqlUtil:
    def __init__(self):
        self.is_connected = False
        try:
            self.conn = pymysql.connect(host='47.98.203.232', user='root', password='lxy1314', port=3306,
                                        db='bss_pro')
            self.cursor = self.conn.cursor()
            self.is_connected = True
        except Exception as e:
            logger.error(e)

    # def __del__(self):
    #     self.conn.close()

    def escape(self, string):
        return '%s' % string

    def insert(self, tablename=None, **ret):
        if self.is_connected:
            tablename = self.escape(tablename)
            _keys = ",".join(self.escape(k) for k in ret)
            _values = ",".join(['%s', ] * len(ret))
            insert_sql = "insert into %s (%s) values (%s)" % (tablename, _keys, _values)
            try:
                self.cursor.execute(insert_sql, tuple(ret.values()))
                self.conn.commit()
            except Exception as e:
                logger.error(e)