#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-06-13 16:39
# @Author  : liupan
# @Site    : 
# @File    : demo20.py
# @Software: PyCharm

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException

browser = webdriver.Chrome()
try:
    browser.get('https://www.baidu.com')
except TimeoutException:
    print('Time Out')
try:
    browser.find_element_by_id('hello')
except NoSuchElementException:
    print('No Element')
finally:
    browser.close()
