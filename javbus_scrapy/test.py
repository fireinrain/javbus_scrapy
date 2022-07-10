#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Description: simple file for test method for utils
@Author  : fireinrain
@Site    : https://github.com/fireinrain
@File    : test.py
@Software: PyCharm
@Time    : 2022/7/10 9:55 AM
"""
import requests

from javbus_scrapy.utils import make_actresses_header, make_star_page_header, BASE_URL, string_end_with_num, \
    magnet_to_torrent_file


def test_make_actresses_header():
    current_url = ""
    pre_page_url = ""
    print(make_actresses_header(current_url, pre_page_url))


def test_fetch_page_with_cookie_all():
    url = "https://www.javbus.com/star/okq"
    cookie_str = "PHPSESSID=hpf3qam0thtcll18d87peh2vk1; existmag=all"
    response = requests.get("https://www.javbus.com/star/okq", headers=make_star_page_header(BASE_URL, url))
    assert "OFJE-371" in response.text, "请求有问题"
    print(response.text)


def test_list_sort():
    a = ["censored_xxx", "uncensored_xxxx"]
    a.sort(key=lambda x: x.startswith("ce"), reverse=True)
    print(a)


def test_str_end_with_num():
    a = "https://www.javbus.com/star/2m3"
    print(string_end_with_num(a))


# 测试多行字符串换行
def test_multi_line_str_code():
    a = "xxxx"
    b = "sdsds"
    c = "sadsasiasds"
    d = "isdaisdajsdasdasdasda"
    e = "xxxsadalfsad"
    f = "asdasdc"
    strs = f"{a},{b}," \
           f"{c},{d}," \
           f"{e},{f}"
    print(strs)


def test_magnet_to_torrent():
    mag = "magnet:?xt=urn:btih:6CD02EA593812AA0A68D58D7DC8D90AA9DB3A723&dn=SSNI-388-C"
    magnet_to_torrent_file(mag, store_dir="../data_store")


def test_libtorrent_files():
    import libtorrent
    import warnings
    file_name = "./temp.torrent"
    info = libtorrent.torrent_info(file_name)
    # 抑制DeprecationWarning提示
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        max_size = 0
        max_file_path = ""
        for item in info.files():
            print(f"{item.path}->{item.size}")
            if item.size > max_size:
                max_size = item.size
                max_file_path = item.path
        print(max_size, max_file_path)

        file_name = max_file_path.replace("/", "-") + "-" + str(max_size // (1000 ** 3)) + "." + str(
            max_size % (1000 ** 3)) + "GB"
    print(file_name)


if __name__ == '__main__':
    # test_make_actresses_header()
    # test_fetch_page_with_cookie_all()
    # test_list_sort()
    # test_str_end_with_num()
    # test_multi_line_str_code()
    test_magnet_to_torrent()
    # test_libtorrent_files()
    pass
