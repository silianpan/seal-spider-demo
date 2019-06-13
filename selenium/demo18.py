#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-06-13 16:31
# @Author  : liupan
# @Site    : 选项卡管理
# @File    : demo18.py
# @Software: PyCharm

import time
from selenium import webdriver

browser = webdriver.Chrome()
browser.get('https://www.baidu.com')
browser.execute_script('window.open()')
print(browser.window_handles)
browser.switch_to_window(browser.window_handles[1])
browser.get('https://www.taobao.com')
time.sleep(1)
browser.switch_to_window(browser.window_handles[0])
browser.get('https://python.org')