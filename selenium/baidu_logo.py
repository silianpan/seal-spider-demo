#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-01-23 21:18
# @Author  : liupan
# @Site    : 
# @File    : baidu_logo.py
# @Software: PyCharm

# -*- coding: utf-8 -*-

import math
from base64 import b64decode
from io import StringIO

from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
# from wand.image import Image


def get_element_screenshot(element: WebElement) -> bytes:
    driver = element._parent
    ActionChains(driver).move_to_element(element).perform()  # focus
    src_base64 = driver.get_screenshot_as_base64()
    scr_png = b64decode(src_base64)
    scr_img = Image(blob=scr_png)

    x = element.location["x"]
    y = element.location["y"]
    w = element.size["width"]
    h = element.size["height"]
    scr_img.crop(
        left=math.floor(x),
        top=math.floor(y),
        width=math.ceil(w),
        height=math.ceil(h),
    )
    return scr_img.make_blob()


print("开始爬取")
# 创建chrome参数对象
options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在的报错
# options.add_argument('--window-size=1920,1080')  # 指定浏览器窗口大小
options.add_argument('--start-maximized')  # 浏览器窗口最大化
options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
options.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
# options.add_argument('--blink-settings=imagesEnabled=false')  # 不加载图片,加快访问速度
options.add_argument('--headless')  # 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
options.add_argument('test-type')
options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors",
                                                    "enable-automation"])  # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
# options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})  # 不加载图片,加快访问速度

driver = webdriver.Chrome(options=options)
driver.maximize_window()
# driver.set_window_size(1366, 768)
# driver.viewportSize = {'width': 1366, 'height': 768}
driver.get('http://www.baidu.com')
print(driver.title)
baidu_img = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, '.index-logo-srcnew'))
)
# get_element_screenshot(baidu_img)
img = driver.get_screenshot_as_png()  # 对整个浏览器页面进行截图
print(baidu_img.size)
# x, y = baidu_img.location.values()
x = baidu_img.location_once_scrolled_into_view['x']
y = baidu_img.location_once_scrolled_into_view['y']
# x = 580
# y = 160
right = x + baidu_img.size['width']
bottom = y + baidu_img.size['height']

# im = Image.open('screenshot.png')
im = Image.open(StringIO(img))
# im.resize((1600, 1200))
print((x, y, right, bottom))
im = im.crop((x, y, right, bottom))  # 对浏览器截图进行裁剪
im.save('baidu.png')
# driver.quit()
print("爬取完成")
