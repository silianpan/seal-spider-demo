# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from scrapy.exceptions import DropItem


class PkulawPipeline(object):
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def __init__(self, settings):
        self.host = settings.get('MYSQL_HOST')
        self.database = settings.get('MYSQL_DATABASE')
        self.user = settings.get('MYSQL_USER')
        self.password = settings.get('MYSQL_PASSWORD')
        self.port = settings.get('MYSQL_PORT')

        self.conn = None
        self.cursor = None

    def open_spider(self, spider):
        self.conn = pymysql.connect(self.host, self.user, self.password, self.database, charset='utf8', port=self.port)
        self.cursor = self.conn.cursor()

    def close_spider(self, spider):
        self.conn.close()

    # def process_item(self, item, spider):
    #     data = dict(item)
    #     keys = ', '.join(data.keys())
    #     values = ', '.join(['%s'] * len(data))
    #     sql = 'insert into %s (%s) values (%s)' % (item.table, keys, values)
    #     self.cursor.execute(sql, tuple(data.values()))
    #     self.conn.commit()
    #     return item

    def process_item(self, ret, spider):
        # sql语句
        insert_sql = """
        INSERT INTO law(title, pub_dept, pub_no, pub_date, law_type, force_level, time_valid, impl_date, content, url, type, deadline, appr_dept, appr_date) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        try:
            # 执行插入数据到数据库操作
            self.cursor.execute(insert_sql, (
                ret.get('title', ''), ret.get('pub_dept', ''), ret.get('pub_no', ''), ret.get('pub_date', ''),
                ret.get('law_type', ''), ret.get('force_level', ''),
                ret.get('time_valid', ''), ret.get('impl_date', ''), ret.get('content', ''), ret.get('url', ''),
                ret.get('type', ''), ret.get('deadline', ''),
                ret.get('appr_dept', ''),
                ret.get('appr_date', '')))
            # 提交，不进行提交无法保存到数据库
            self.conn.commit()
            return ret
        except pymysql.err.IntegrityError:
            raise DropItem('Repeat Key')
