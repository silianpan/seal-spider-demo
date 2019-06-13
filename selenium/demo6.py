#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-06-13 15:21
# @Author  : liupan
# @Site    : 查询淘宝左侧导航栏
# @File    : demo6.py
# @Software: PyCharm

from selenium import webdriver

browser = webdriver.Chrome()
browser.get('https://www.taobao.com')
lis = browser.find_elements_by_css_selector('.service-bd li')
print(lis)
browser.close()
