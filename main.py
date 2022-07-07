#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Description: run scrapy in here
@Author  : fireinrain
@Site    : https://github.com/fireinrain
@File    : main.py
@Software: PyCharm
@Time    : 2022/7/7 4:22 AM
"""
from scrapy import cmdline

if __name__ == '__main__':
    # cmdline.execute('scrapy crawl actresses'.split())
    cmdline.execute('scrapy crawl star_page'.split())
