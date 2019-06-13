#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-06-13 15:06
# @Author  : liupan
# @Site    : 
# @File    : demo3.py
# @Software: PyCharm

from selenium import webdriver

browser = webdriver.Chrome()
browser.get('https://www.taobao.com')
print(browser.page_source)
browser.close()