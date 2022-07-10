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
import os
import re

import requests
from fake_useragent import UserAgent

BASE_URL = "https://www.javbus.com"
ACTRESSES_PATH_NAME = "actresses"
STARINFO_PATH_NAME = "starinfo"
STARITEMINFO_PATH_NAME = "stariteminfo"
MOVIE_DETAIL_PATH_NAME = "moviedetail"


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
    """
    判断是否是第一页
    :param url:
    :type url:
    :return:
    :rtype:
    """
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


# 将磁力链接转化为torrent file
def magnet_to_torrent_file(magnet_str, store_dir, file_name=None):
    convert_site_url1 = "http://magnet2torrent.com/"
    # convert_site_url2 = "https://btsow.com/convert/magnet"
    user_agent = {"user-Agent": UserAgent(verify_ssl=False).random}
    client_session = requests.Session()
    _ = client_session.get(convert_site_url1, headers=user_agent
                           )
    # upload magnet url
    # post url
    upload_url = "http://magnet2torrent.com/upload/"
    data = {"magnet": magnet_str}
    response = client_session.post(upload_url, data=data, headers=user_agent)
    if file_name is not None and file_name != "":
        torrent_store_path = os.path.join(store_dir, file_name)
        with open(torrent_store_path, "wb") as file:
            file.write(response.content)
    else:
        # 解析响应流 并解析出torrent内的文件列表 找出最大的文件 然后获取它的文件名  作为
        # torrent 的文件名
        import libtorrent
        import warnings

        # some bug here   temp.name is 8 ???
        # import tempfile
        # file_name = None
        # with tempfile.TemporaryFile(mode="w+b") as temp:
        #     temp.write(response.content)
        #     file_name = temp.name
        #     print(temp.name)
        file_name = os.path.join(store_dir, "temp.torrent")
        with open(file_name, "wb") as file:
            file.write(response.content)

        info = libtorrent.torrent_info(file_name)
        # 抑制DeprecationWarning提示
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            max_size = 0
            max_file_path = ""
            for item in info.files():
                # print(f"{item.path}->{item.size}")
                if item.size > max_size:
                    max_size = item.size
                    max_file_path = item.path
            # print(max_size, max_file_path)
            # SSNI-388-C-SSNI-388-C.mp4-5GB
            size_float = str(max_size % (1000 ** 3))[:2]
            new_file_name = max_file_path.replace("/", "-") + "-" + str(
                max_size // (1000 ** 3)) + "." + size_float + "GB" + ".torrent"
            new_file_name = os.path.join(store_dir, new_file_name)
            os.rename(file_name, new_file_name)
