#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-06-23 09:59
# @Author  : liupan
# @Site    : 
# @File    : baiduimage.py
# @Software: PyCharm

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import re
import requests

# browser = webdriver.Chrome()
browser = webdriver.PhantomJS()
pattern = re.compile('"objURL":"(http://.*?)"')
try:
    browser.get('http://image.baidu.com/')
    # 获取输入框
    input = browser.find_element_by_id('kw')
    # 输入搜索关键词
    input.send_keys('周杰伦')
    # 点击回车
    input.send_keys(Keys.ENTER)

    # 等待执行
    wait = WebDriverWait(browser, 20)
    wait.until(EC.presence_of_all_elements_located)
    # 获取网页源代码
    page_source = browser.page_source
    ret = re.findall(pattern, page_source)
    print(ret)

    # 下拉滚动
    js = "var q=document.documentElement.scrollTop=10000000"
    browser.execute_script(js)
    # 获取网页源代码
    page_source2 = browser.page_source
    ret2 = re.findall(pattern, page_source2)
    print(ret2)
    ret = ret + ret2

    # 保存到文件中
    i = 1
    for imgUrl in ret:
        imgRet = requests.get(imgUrl)
        with open('./baiduImage/' + str(i) + '.jpg', 'wb') as f:
            f.write(imgRet.content)
            i = i + 1
finally:
    browser.close()
