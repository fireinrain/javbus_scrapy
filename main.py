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
from multiprocessing import Process

import uvicorn
from scrapy import cmdline

from javbus_scrapy import server

proc = None


def server_run():
    """
       This function to run configured uvicorn server.
    """
    uvicorn.run(app=server.app, host='127.0.0.1', port=9000)


def server_start():
    """
        This function to start a new process (start the server).
    """
    global proc
    # create process instance and set the target to run function.
    # use daemon mode to stop the process whenever the program stopped.
    proc = Process(target=server_run, args=(), daemon=True)
    proc.start()
    proc.join()


def server_stop():
    """
        This function to join (stop) the process (stop the server).
    """
    global proc
    # check if the process is not None
    if proc:
        # join (stop) the process with a timeout setten to 0.25 seconds.
        # using timeout (the optional arg) is too important in order to
        # enforce the server to stop.
        proc.join(0.25)


if __name__ == '__main__':
    # cmdline.execute('scrapy crawl actresses'.split())
    run_option = input("请输入需要执行的爬虫序号(1.actresses/2.star_page/3.movie/4.deploy webserver): ")
    if run_option == "" or run_option == "1":
        # 运行默认
        cmdline.execute('scrapy crawl actresses'.split())
    if run_option == "2":
        cmdline.execute('scrapy crawl star_page'.split())
    if run_option == "3":
        cmdline.execute('scrapy crawl movie'.split())
    if run_option == "4":
        server_start()
        # server_stop()
        # uvicorn.run(app=server.app, host='127.0.0.1', port=9000)
