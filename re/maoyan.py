#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-06-23 15:46
# @Author  : liupan
# @Site    : 
# @File    : maoyan.py
# @Software: PyCharm

import re
import requests

pattern_img = re.compile('<img.*?data-src="(.*?)".*?>', re.S)
pattern_text = re.compile('<p.*?<a.*?data-act="boarditem-click".*?>(\S+?)</a></p>', re.S)
pattern_text2 = re.compile('<p.*?class="star">(.*?)</p>', re.S)
ret = requests.get('https://maoyan.com/board')

images = re.findall(pattern_img, ret.text)
text = re.findall(pattern_text, ret.text)
text2 = re.findall(pattern_text2, ret.text)

print(text)
i = 0
while i < len(images):
    img = images[i].strip()
    name = text[i].strip()
    auth = text2[i].strip()
    print(img, name, auth)
    i = i + 1
