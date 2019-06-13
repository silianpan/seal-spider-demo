#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-06-13 16:27
# @Author  : liupan
# @Site    : 
# @File    : demo16.py
# @Software: PyCharm

import time
from selenium import webdriver

browser = webdriver.Chrome()
browser.get('https://www.baidu.com/')
browser.get('https://www.taobao.com/')
browser.get('https://www.python.org/')
browser.back()
time.sleep(1)
browser.forward()
browser.close()
