# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import logging
import pymysql
from scrapy.exceptions import DropItem

logger = logging.getLogger(__name__)


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
        self.is_connected = False

    def open_spider(self, spider):
        try:
            self.conn = pymysql.connect(self.host, self.user, self.password, self.database, charset='utf8', port=self.port)
            self.cursor = self.conn.cursor()
            self.is_connected = True
        except Exception as e:
            logger.error(e)

    def close_spider(self, spider):
        if self.conn:
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
        if not self.is_connected:
            logger.error("Mysql connection is lost!")
            return ret
        if not ret.get('content', False):
            raise DropItem('content is None!')
        # 更新content内容不完整的情况
        if u'还不是用户？' not in ret.get('content', ''):
            select_sql = """
                select t.title from law t where t.title = %s and t.url = %s and t.content like %s
            """
            self.cursor.execute(select_sql, (ret.get('title', ''), ret.get('url', ''), u'%还不是用户？%'))
            if self.cursor.rowcount == 1:
                # 更新content内容，更新后直接返回，不再插入
                update_sql = """
                    UPDATE law SET content = %s WHERE title = %s and url = %s
                """
                try:
                    self.cursor.execute(update_sql, (ret.get('content', ''), ret.get('title', ''), ret.get('url', '')))
                    self.conn.commit()
                    return ret
                except Exception as e:
                    logger.error(e)
        # # sql语句
        # insert_sql = """
        # INSERT INTO law(title, pub_dept, pub_no, pub_date, law_type, force_level, time_valid, impl_date, content, url, type, deadline, appr_dept, appr_date) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        # """
        # try:
        #     # 执行插入数据到数据库操作
        #     self.cursor.execute(insert_sql, (
        #         ret.get('title', ''), ret.get('pub_dept', ''), ret.get('pub_no', ''), ret.get('pub_date', ''),
        #         ret.get('law_type', ''), ret.get('force_level', ''),
        #         ret.get('time_valid', ''), ret.get('impl_date', ''), ret.get('content', ''), ret.get('url', ''),
        #         ret.get('type', ''), ret.get('deadline', ''),
        #         ret.get('appr_dept', ''),
        #         ret.get('appr_date', '')))
        #     # 提交，不进行提交无法保存到数据库
        #     self.conn.commit()
        #     return ret
        # except pymysql.err.IntegrityError:
        #     raise DropItem('Repeat Key')

        _data = dict(ret)
        _keys = ', '.join(_data.keys())
        _values = ', '.join(['%s'] * len(_data))
        sql = 'insert into %s (%s) values (%s)' % (ret.table, _keys, _values)
        try:
            self.cursor.execute(sql, tuple(_data.values()))
            self.conn.commit()
            return ret
        except Exception as e:
            logger.error(e)
