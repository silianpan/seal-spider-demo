#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-06-19 22:13
# @Author  : liupan
# @Site    : 
# @File    : demo1.py
# @Software: PyCharm

from scrapy import Selector
body= '<html><head><title>Hello World</title></head><body></body> </ html>'
selector = Selector(text=body)
title = selector.xpath('//title/text()').extract_first()
print(title)
