#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-06-22 16:05
# @Author  : liupan
# @Site    : 
# @File    : zhihu.py.py
# @Software: PyCharm

import requests
import re

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
}

# pattern = re.compile('<a class="question_link".*?>\s+(\S+)\s+</a>')
pattern = re.compile('<li class="title">\s+<a onclick="moreurl.*?>(\S+)</a>\s+</li>')

res = requests.get('https://movie.douban.com/', headers=headers)
pres = re.findall(pattern, res.text)
print(pres)
