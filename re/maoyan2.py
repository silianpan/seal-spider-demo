#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-06-23 16:40
# @Author  : liupan
# @Site    : 
# @File    : maoyan2.py.py
# @Software: PyCharm

import requests
from lxml import etree

res = requests.get('https://maoyan.com/board')
ret = etree.HTML(res.text)
imgs = ret.xpath('//a[@class="image-link"]//img[@class="board-img"]/@data-src')
names = ret.xpath('//p[@class="name"]//a[@data-act="boarditem-click"]/text()')
stars = ret.xpath('//p[@class="star"]/text()')
scores1 = ret.xpath('//p[@class="score"]//i[@class="integer"]//text()')
scores2 = ret.xpath('//p[@class="score"]//i[@class="fraction"]//text()')

i = 0
while i < len(imgs):
    img = imgs[i].strip()
    name = names[i].strip()
    star = stars[i].strip()
    score1 = scores1[i].strip()
    score2 = scores2[i].strip()
    print(img, name, star, score1 + score2)
    i = i + 1
