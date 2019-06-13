#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-06-13 15:24
# @Author  : liupan
# @Site    : 节点交互
# @File    : demo7.py
# @Software: PyCharm
# 输入文字用 send_keys() 方法，清空文字用 clear() 方法，另外还有按钮点击，用 click() 方法

from selenium import webdriver
import time

browser = webdriver.Chrome()
browser.get('https://www.taobao.com')
input = browser.find_element_by_id('q')
input.send_keys('iPhone')
time.sleep(1)
input.clear()
input.send_keys('iPad')
button = browser.find_element_by_class_name('btn-search')
button.click()