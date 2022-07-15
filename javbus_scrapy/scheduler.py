#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Description: 定时任务 定时获取首页
@Author  : fireinrain
@Site    : https://github.com/fireinrain
@File    : scheduler.py
@Software: PyCharm
@Time    : 2022/7/16 1:59 AM
"""

import time

import schedule


# TODO add scheduler
def job():
    print("I'm working...")


schedule.every(10).minutes.do(job)
schedule.every().hour.do(job)
schedule.every().day.at("10:30").do(job)
schedule.every().monday.do(job)
schedule.every().wednesday.at("13:15").do(job)
schedule.every().minute.at(":17").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)

if __name__ == '__main__':
    pass
