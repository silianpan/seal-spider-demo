#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-06-13 15:47
# @Author  : liupan
# @Site    : 获取ID、位置、标签名、大小
# @File    : demo12.py
# @Software: PyCharm

from selenium import webdriver

browser = webdriver.Chrome()
url = 'https://www.zhihu.com/explore'
browser.get(url)
input = browser.find_element_by_class_name('zu-top-add-question')
print(input.id)
print(input.location)
print(input.tag_name)
print(input.size)
