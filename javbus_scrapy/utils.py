#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Description: 
@Author  : fireinrain
@Site    : https://github.com/fireinrain
@File    : utils.py
@Software: PyCharm
@Time    : 2022/7/7 4:31 AM
"""
import re

import requests
from fake_useragent import UserAgent

BASE_URL = "https://www.javbus.com"
ACTRESSES_PATH_NAME = "actresses"
STARINFO_PATH_NAME = "starinfo"
STARITEMINFO_PATH_NAME = "stariteminfo"


def make_default_header():
    """
    默认主页header
    :return:
    :rtype:
    """
    header_str = f"""
        authority: www.javbus.com
        :method: GET
        :path: /
        :scheme: https
        accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
        accept-encoding: gzip, deflate, br
        accept-language: zh
        cache-control: no-cache
        pragma: no-cache
        sec-ch-ua: " Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"
        sec-ch-ua-mobile: ?0
        sec-ch-ua-platform: "macOS"
        sec-fetch-dest: document
        sec-fetch-mode: navigate
        sec-fetch-site: none
        sec-fetch-user: ?1
        upgrade-insecure-requests: 1
        user-agent: {UserAgent(verify_ssl=False).random}
    
    """
    fake_header = parse_and_make_header(header_str)
    # print(fake_header)
    return fake_header


def make_star_page_header(current_url, pre_page_url):
    """
    演员个人主页请求头
    :param current_url:
    :type current_url:
    :param pre_page_url:
    :type pre_page_url:
    :param cookie:
    :type cookie:
    :return:
    :rtype:
    """
    header_str = f"""
                :authority: www.javbus.com
                :method: GET
                :path: {current_url.replace(BASE_URL, "")}
                :scheme: https
                accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
                accept-encoding: gzip, deflate, br
                accept-language: zh,en;q=0.9,zh-TW;q=0.8,zh-CN;q=0.7,ja;q=0.6
                cache-control: no-cache
                pragma: no-cache
                referer: {pre_page_url}
                sec-ch-ua: " Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"
                sec-ch-ua-mobile: ?0
                sec-ch-ua-platform: "macOS"
                sec-fetch-dest: document
                sec-fetch-mode: navigate
                sec-fetch-site: same-origin
                sec-fetch-user: ?1
                upgrade-insecure-requests: 1
                user-agent: {UserAgent(verify_ssl=False).random}
                """
    # cookie: {cookie}
    fake_header = parse_and_make_header(header_str)
    # print(fake_header)
    return fake_header


def make_actresses_header(current_url, pre_page_url):
    """
    获取演员页面的请求头
    :param current_url:
    :type current_url:
    :param pre_page_url:
    :type pre_page_url:
    :param cookie:
    :type cookie:
    :return:
    :rtype:
    """
    header_str = f"""
            :authority: www.javbus.com
            :method: GET
            :path: {current_url.replace(BASE_URL, "")}
            :scheme: https
            accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
            accept-encoding: gzip, deflate, br
            accept-language: zh,en;q=0.9,zh-TW;q=0.8,zh-CN;q=0.7,ja;q=0.6
            cache-control: no-cache
            pragma: no-cache
            referer: {pre_page_url}
            sec-ch-ua: " Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"
            sec-ch-ua-mobile: ?0
            sec-ch-ua-platform: "macOS"
            sec-fetch-dest: document
            sec-fetch-mode: navigate
            sec-fetch-site: same-origin
            sec-fetch-user: ?1
            upgrade-insecure-requests: 1
            user-agent: {UserAgent(verify_ssl=False).random}
            """
    # cookie: {cookie}
    fake_header = parse_and_make_header(header_str)
    # print(fake_header)
    return fake_header


def parse_and_make_header(header_str):
    """
    解析header模板并生成header字典
    :param header_str:
    :type header_str:
    :return:
    :rtype:
    """
    fake_header = {}
    header_str_split = header_str.split("\n")
    header_items = [i.strip() for i in header_str_split if len(i) > 0]
    # 去除空白项
    header_items = [i.strip() for i in header_items if len(i) > 0]
    # 分割键值对
    for i in header_items:
        key = ""
        value = ""
        if i.startswith(":"):
            rfind_index = i.rfind(":")
            key = i[:rfind_index]
            value = i[rfind_index + 1:]

        else:
            find_index = i.find(":")
            key = i[:find_index]
            value = i[find_index + 1:]
        fake_header.update({key.strip(): value.strip()})
    return fake_header


def is_first_star_page_url(url: str) -> bool:
    if "uncensored" in url:
        replace = url.replace("https://www.javbus.com/uncensored/star/", "")
        split = replace.split("/")
        if len(split) == 1:
            return True
    else:
        replace = url.replace("https://www.javbus.com/star/", "")
        split = replace.split("/")
        if len(split) == 1:
            return True
    return False


def string_end_with_num(string):
    """
    判断字符串以数字结尾
    :param string:
    :type string:
    :return:
    :rtype:
    """
    # 以一个数字结尾字符串
    text = re.compile(r".*[0-9]$")
    if text.match(string):
        return True
    else:
        return False


def test_make_actresses_header():
    current_url = ""
    pre_page_url = ""
    cookie = "ccc"
    print(make_actresses_header(current_url, pre_page_url, cookie))


def test_fetch_page_with_cookie_all():
    url = "https://www.javbus.com/star/okq"
    cookie_str = "PHPSESSID=hpf3qam0thtcll18d87peh2vk1; existmag=all"
    response = requests.get("https://www.javbus.com/star/okq", headers=make_star_page_header(BASE_URL, url, cookie_str))
    assert "OFJE-371" in response.text, "请求有问题"
    print(response.text)


def test_list_sort():
    a = ["censored_xxx", "uncensored_xxxx"]
    a.sort(key=lambda x: x.startswith("ce"), reverse=True)
    print(a)


def test_str_end_with_num():
    a = "https://www.javbus.com/star/2m3"
    print(string_end_with_num(a))


if __name__ == '__main__':
    # test_make_actresses_header()
    # test_fetch_page_with_cookie_all()
    test_list_sort()
    test_str_end_with_num()

    pass
