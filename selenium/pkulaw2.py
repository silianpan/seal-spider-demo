# !/usr/bin/env python
# encoding: utf-8

import os
import random
import ssl
import time
from io import BytesIO

import cv2
# -*- coding: utf-8 -*-
# @contact: ybsdeyx@foxmail.com
# @software: PyCharm
# @time: 2019/4/25 16:39
# @author: liupan
# @file: captcha_qq.py
# @desc:
import numpy as np
from PIL import Image
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

ssl._create_default_https_context = ssl._create_unverified_context


class Login(object):
    """
    腾讯防水墙滑动验证码破解
    使用OpenCV库
    成功率大概90%左右：在实际应用中，登录后可判断当前页面是否有登录成功才会出现的信息：比如用户名等。循环
    https://open.captcha.qq.com/online.html
    破解 腾讯滑动验证码
    腾讯防水墙
    python + seleniuum + cv2
    """

    def __init__(self):
        # 如果是实际应用中，可在此处账号和密码
        self.url = "https://www.pkulaw.com/"
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 20)

    @staticmethod
    def show(name):
        cv2.imshow('Show', name)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    @staticmethod
    def webdriverwait_send_keys(dri, element, value):
        """
        显示等待输入
        :param dri: driver
        :param element:
        :param value:
        :return:
        """
        WebDriverWait(dri, 10, 5).until(lambda dr: element).send_keys(value)

    @staticmethod
    def webdriverwait_click(dri, element):
        """
        显示等待 click
        :param dri: driver
        :param element:
        :return:
        """
        WebDriverWait(dri, 10, 5).until(lambda dr: element).click()

    @staticmethod
    def get_postion(chunk, canves):
        """
        判断缺口位置
        :param chunk: 缺口图片是原图
        :param canves:
        :return: 位置 x, y
        """
        otemp = chunk
        oblk = canves
        target = cv2.imread(otemp, 0)
        template = cv2.imread(oblk, 0)
        # w, h = target.shape[::-1]
        temp = 'temp.jpg'
        targ = 'targ.jpg'
        cv2.imwrite(temp, template)
        cv2.imwrite(targ, target)
        target = cv2.imread(targ)
        target = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
        target = abs(255 - target)
        cv2.imwrite(targ, target)
        target = cv2.imread(targ)
        template = cv2.imread(temp)
        result = cv2.matchTemplate(target, template, cv2.TM_CCOEFF_NORMED)
        x, y = np.unravel_index(result.argmax(), result.shape)
        return x, y
        # # 展示圈出来的区域
        # cv2.rectangle(template, (y, x), (y + w, x + h), (7, 249, 151), 2)
        # cv2.imwrite("yuantu.jpg", template)
        # show(template)

    @staticmethod
    def get_track(distance):
        """
        模拟轨迹 假装是人在操作
        :param distance:
        :return:
        """
        # 初速度
        v = 0
        # 单位时间为0.2s来统计轨迹，轨迹即0.2内的位移
        t = 0.2
        # 位移/轨迹列表，列表内的一个元素代表0.2s的位移
        tracks = []
        # 当前的位移
        current = 0
        # 到达mid值开始减速
        mid = distance * 7 / 8

        distance += 10  # 先滑过一点，最后再反着滑动回来
        # a = random.randint(1,3)
        while current < distance:
            if current < mid:
                # 加速度越小，单位时间的位移越小,模拟的轨迹就越多越详细
                a = random.randint(2, 4)  # 加速运动
            else:
                a = -random.randint(3, 5)  # 减速运动

            # 初速度
            v0 = v
            # 0.2秒时间内的位移
            s = v0 * t + 0.5 * a * (t ** 2)
            # 当前的位置
            current += s
            # 添加到轨迹列表
            tracks.append(round(s))

            # 速度已经达到v,该速度作为下次的初速度
            v = v0 + a * t

        # 反着滑动到大概准确位置
        for i in range(4):
            tracks.append(-random.randint(2, 3))
        for i in range(4):
            tracks.append(-random.randint(1, 3))
        return tracks

    @staticmethod
    def urllib_download(imgurl, imgsavepath):
        """
        下载图片
        :param imgurl: 图片url
        :param imgsavepath: 存放地址
        :return:
        """
        from urllib.request import urlretrieve
        urlretrieve(imgurl, imgsavepath)

    def after_quit(self):
        """
        关闭浏览器
        :return:
        """
        self.driver.quit()

    def open(self):
        """
        打开网页输入用户名密码
        :return: None
        """
        # 点击法律更多
        self.driver.maximize_window()
        self.driver.get(self.url)
        # email = self.wait.until(EC.presence_of_element_located((By.ID, 'email')))
        # password = self.wait.until(EC.presence_of_element_located((By.ID, 'password')))
        # email.send_keys(self.email)
        # password.send_keys(self.password)
        law_more = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@groupvalue="XA01" and @class="more"]')))
        law_more.click()
        time.sleep(2)

        # 点击分页100
        self.driver.execute_script(
            "var x=document.querySelector(\"dl[prop='TokenNum']\");"
            "x.style.display='block';"
            "x.style.opacity=1"
        )
        page_show = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '//dl[@prop="TokenNum"]/dd[@filter_value="100"]')))
        page_show.click()
        time.sleep(2)

        # 点击第三页弹出验证码
        page_index3 = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '//a[@pageindex="3" and @href="javascript:void(0);"]')))
        page_index3.click()
        time.sleep(2)

    def get_position_crop(self, img_id='bgImg'):
        """
        获取验证码位置
        :return: 验证码位置元组
        """
        # img = self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[id="Verification"]/div[id="bgImg"]')))
        img = self.wait.until(EC.presence_of_element_located((By.ID, img_id)))
        time.sleep(2)
        location = img.location
        size = img.size
        top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size[
            'width']
        return (top, bottom, left, right)

    def get_screenshot(self):
        """
        获取网页截图
        :return: 截图对象
        """
        screenshot = self.driver.get_screenshot_as_png()
        screenshot = Image.open(BytesIO(screenshot))
        return screenshot

    def get_geetest_image(self, name='captcha.png', img_id='bgImg'):
        """
        获取验证码图片
        :return: 图片对象
        """
        top, bottom, left, right = self.get_position_crop(img_id)
        print('验证码位置', top, bottom, left, right)
        screenshot = self.get_screenshot()
        screenshot.save(name + '2.png')
        captcha = screenshot.crop((left, top, right, bottom))
        captcha.save(name)
        return captcha

    def get_slider(self):
        """
        获取滑块
        :return: 滑块对象
        """
        slider = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'handler_bg')))
        return slider

    def login_main(self):
        # ssl._create_default_https_context = ssl._create_unverified_context
        self.open()
        driver = self.driver

        # click_keyi_username = driver.find_element_by_xpath("//div[@class='wp-onb-tit']/a[text()='可疑用户']")
        # self.webdriverwait_click(driver, click_keyi_username)
        #
        # login_button = driver.find_element_by_id('code')
        # self.webdriverwait_click(driver, login_button)
        # time.sleep(1)

        # layui_dialog = driver.find_element_by_class_name('layui-layer-dialog')
        # driver.switch_to.active_element  # switch 到 滑块激活元素
        time.sleep(0.5)
        bk_block = driver.find_element_by_xpath('//div[@id="bgImg"]')  # 大图
        web_image_width = bk_block.size
        web_image_width = web_image_width['width']
        bk_block_x = bk_block.location['x']

        slide_block = driver.find_element_by_xpath('//div[@id="xy_img"]')  # 小滑块
        slide_block_x = slide_block.location['x']

        # bk_block = driver.find_element_by_xpath('//img[@id="slideBg"]').get_attribute('src')  # 大图 url
        # slide_block = driver.find_element_by_xpath('//img[@id="slideBlock"]').get_attribute('src')  # 小滑块 图片url
        # slid_ing = driver.find_element_by_xpath('//div[@id="tcaptcha_drag_thumb"]')  # 滑块

        os.makedirs('./image/', exist_ok=True)
        self.get_geetest_image('./image/bkBlock.png')
        # 点按呼出缺口
        slid_ing = self.get_slider()
        slid_ing.click()
        self.get_geetest_image('./image/slideBlock.png', 'xy_img')
        # self.urllib_download(bk_block, './image/bkBlock.png')
        # self.urllib_download(slide_block, './image/slideBlock.png')

        time.sleep(0.5)
        img_bkblock = Image.open('./image/bkBlock.png')
        real_width = img_bkblock.size[0]
        width_scale = float(real_width) / float(web_image_width)
        position = self.get_postion('./image/bkBlock.png', './image/slideBlock.png')
        real_position = position[1] / width_scale
        real_position = real_position - (slide_block_x - bk_block_x)
        track_list = self.get_track(real_position + 4)

        ActionChains(driver).click_and_hold(on_element=slid_ing).perform()  # 点击鼠标左键，按住不放
        time.sleep(0.2)
        # print('第二步,拖动元素')
        for track in track_list:
            ActionChains(driver).move_by_offset(xoffset=track, yoffset=0).perform()  # 鼠标移动到距离当前位置（x,y）
            time.sleep(0.002)
        # ActionChains(driver).move_by_offset(xoffset=-random.randint(0, 1), yoffset=0).perform()   # 微调，根据实际情况微调
        time.sleep(1)
        # print('第三步,释放鼠标')
        ActionChains(driver).release(on_element=slid_ing).perform()
        time.sleep(1)

        print('登录成功')
        self.after_quit()


if __name__ == '__main__':
    phone = "****"
    login = Login()
    login.login_main()
