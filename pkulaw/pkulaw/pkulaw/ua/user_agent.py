#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-02-07 09:44
# @Author  : liupan
# @Site    : 
# @File    : user_agent.py
# @Software: PyCharm

import random

from .ua_c import ua_list


class UserAgent(object):
    def __init__(self, browser=None):
        key_list = ua_list.keys()
        if browser and browser in key_list:
            self.user_agent_list = ua_list.get(browser, [])
        else:
            self.user_agent_list = [ua for key in key_list for ua in ua_list[key]]

    @property
    def rget(self):
        return random.choice(self.user_agent_list)


if __name__ == "__main__":
    u = UserAgent("Sleipnir")
    print(u.rget)
