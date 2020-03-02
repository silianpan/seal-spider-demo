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

    def insert(self, tablename=None, **values):
        if self.is_connected:
            self.save_to_mysql(tablename, values)

    # 保存到mysql
    def save_to_mysql(self, tablename=None, **ret):
        insert_sql = 'INSERT INTO ' + tablename + '(title, pub_dept, pub_no, pub_date, law_type, force_level, time_valid, impl_date, content, url, type, deadline, appr_dept, appr_date, remark) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        try:
            self.cursor.execute(insert_sql, (
                ret.get('title', ''), ret.get('pub_dept', ''), ret.get('pub_no', ''), ret.get('pub_date', ''),
                ret.get('law_type', ''), ret.get('force_level', ''),
                ret.get('time_valid', ''), ret.get('impl_date', ''), ret.get('content', ''), ret.get('url', ''),
                ret.get('type', ''), ret.get('deadline', ''),
                ret.get('appr_dept', ''),
                ret.get('appr_date', ''),
                ret.get('remark', '')))
            self.conn.commit()
        except pymysql.err.IntegrityError as ie:
            print('Repeat Key', ie)
        except Exception as e:
            print('other error', e)
