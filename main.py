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
    spider_num = input("请输入需要执行的爬虫序号(1.actresses/2.star_page/3.movie): ")
    if spider_num == "" or spider_num == "1":
        # 运行默认
        cmdline.execute('scrapy crawl actresses'.split())
    if spider_num == "2":
        cmdline.execute('scrapy crawl star_page'.split())
    if spider_num == "3":
        cmdline.execute('scrapy crawl movie'.split())
