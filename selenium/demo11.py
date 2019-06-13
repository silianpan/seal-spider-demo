#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-06-13 15:46
# @Author  : liupan
# @Site    : 获取文本值
# @File    : demo11.py
# @Software: PyCharm

from selenium import webdriver

browser = webdriver.Chrome()
url = 'https://www.zhihu.com/explore'
browser.get(url)
input = browser.find_element_by_class_name('zu-top-add-question')
print(input.text)