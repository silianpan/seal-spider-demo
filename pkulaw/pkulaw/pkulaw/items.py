# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PkulawItem(scrapy.Item):
    # define the fields for your item here like:
    collection = table = 'law'
    title = scrapy.Field()
    pub_dept = scrapy.Field()
    pub_no = scrapy.Field()
    pub_date = scrapy.Field()
    law_type = scrapy.Field()
    force_level = scrapy.Field()
    time_valid = scrapy.Field()
    impl_date = scrapy.Field()
    content = scrapy.Field()
    url = scrapy.Field()
    type = scrapy.Field()
    deadline = scrapy.Field()
    appr_dept = scrapy.Field()
    appr_date = scrapy.Field()
    pdf_url = scrapy.Field()
