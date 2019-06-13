#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-06-13 15:09
# @Author  : liupan
# @Site    : 
# @File    : demo4.py
# @Software: PyCharm

from selenium import webdriver

browser = webdriver.Chrome()
browser.get('https://www.taobao.com')
input_first = browser.find_element_by_id('q')
input_second = browser.find_element_by_css_selector('#q')
input_third = browser.find_element_by_xpath('//*[@id="q"]')
print(input_first, input_second, input_third)
browser.close()