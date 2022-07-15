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
from javbus_scrapy.settings import DATA_STORE
from javbus_scrapy.utils import *


def test_make_actresses_header():
    current_url = ""
    pre_page_url = ""
    print(make_actresses_header(current_url, pre_page_url))


def test_fetch_page_with_cookie_all():
    url = "https://www.javbus.com/star/okq"
    cookie_str = "PHPSESSID=hpf3qam0thtcll18d87peh2vk1; existmag=all"
    response = requests.get("https://www.javbus.com/star/okq", headers=make_star_page_header(DOMAIN_BASE_URL, url))
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


def test_select_from_file():
    from scrapy.selector import Selector
    with open("../torrent_response.html", "r") as file:
        readlines = file.readlines()

        body = ''.join(readlines)
        getall = Selector(text=body).xpath('//tr')
        for item in getall:
            torrent_line_nodes = item.xpath("//td")
            name_node = torrent_line_nodes[0]

            text__getall = name_node.xpath('.//a/text()').getall()

            size_node = torrent_line_nodes[1]

            file_size = size_node.xpath('./a/text()').get(default="")

            share_date = torrent_line_nodes[2]

            file_share_date = share_date.xpath('./a/text()').get(default="")
            print(share_date)


def test_re_extract_html_content():
    strs = """
    <a class="movie-box" href="https://www.javbus.com/th101-090-111233">
                    <div class="photo-frame">
                        <img src="/imgs/thumbs/11k2.jpg" title="Ｗキャスト&lt;Wハメ撮り編&gt;" class="img">
                    </div>
                    <div class="photo-info">
                        <span>Ｗキャスト<w><br>
                        <div style="white-space:normal;">
						                                                                                <button class="btn btn-xs btn-danger" disabled title="包含最新出種的磁力連結">上週新種</button>                          
                        </div>                          
                        <date>th101-090-111233</date> / <date>2018-02-21</date></w></span>
                    </div>
                </a>
    """
    import re
    findall = re.findall(r'<date>(.*?)</date>', strs)
    re_findall = re.findall(r"x", "abc")
    print(findall)
    print(re_findall)


def test_check_str_is_a_valid_url(cvs_file_path):
    url_not_valid = []
    index = 1
    with open("../data_store/actresses/censored_star_2022-07-10.csv", "r") as file:
        while True:
            readline = file.readline()
            # if readline == "":
            #     break
            split = readline.split("|")
            print(readline)
            url = split[1]
            valid_url = check_a_str_is_valid_url(url)
            if not valid_url:
                url_not_valid.append((index, readline))
            index += 1
    print(f"invalid url counts: {url_not_valid}")
    print(f"invalid urls: {url_not_valid}")


def test_process_str_with_rn():
    a = "\r\n              \r\n     \n saiwdwadwa \n \r\n sdasadsad \n"
    replace = a.replace("\r\n", "").replace("\r", "").replace("\n", "").strip()
    print(replace)


def test_pre_gen_url():
    start_urls = ['https://javbus.com/actresses' + "/" + str(i) for i in range(1, 931)]
    for index, ii in enumerate(start_urls):
        print(index)


def test_check_page_is_404():
    strs = """
    https://www.javbus.com/star/vkl
    https://www.javbus.com/star/q9k
    https://www.javbus.com/star/v1e
    https://www.javbus.com/star/v50
    https://www.javbus.com/star/swx
    https://www.javbus.com/star/p6u
    https://www.javbus.com/star/742
    https://www.javbus.com/star/90p
    https://www.javbus.com/star/sqv
    https://www.javbus.com/star/2at
    https://www.javbus.com/star/eac
    https://www.javbus.com/star/6au
    https://www.javbus.com/star/8p
    https://www.javbus.com/star/3cf
    https://www.javbus.com/star/f43
    https://www.javbus.com/star/3f6
    https://www.javbus.com/star/4pb
    https://www.javbus.com/star/340
    https://www.javbus.com/star/n4y
    https://www.javbus.com/star/uq
    https://www.javbus.com/star/xhj
    https://www.javbus.com/star/ps5
    https://www.javbus.com/star/cqg
    https://www.javbus.com/star/9de
    https://www.javbus.com/star/xwk
    https://www.javbus.com/star/w1v
    https://www.javbus.com/star/whm
    https://www.javbus.com/star/uoj
    https://www.javbus.com/star/pvd
    https://www.javbus.com/star/7mv
    https://www.javbus.com/star/2ah
    https://www.javbus.com/star/w86
    https://www.javbus.com/star/vrt
    https://www.javbus.com/star/wwx
    https://www.javbus.com/star/ref
    https://www.javbus.com/star/q81
    https://www.javbus.com/star/qu0
    https://www.javbus.com/star/a12
    https://www.javbus.com/star/6g0
    https://www.javbus.com/star/711
    https://www.javbus.com/star/p6h
    https://www.javbus.com/star/8b1
    https://www.javbus.com/star/6iv
    https://www.javbus.com/star/uua
    https://www.javbus.com/star/u1g
    https://www.javbus.com/star/e6x
    https://www.javbus.com/star/3bd
    https://www.javbus.com/star/6iq
    https://www.javbus.com/star/jya
    https://www.javbus.com/star/4jq
    https://www.javbus.com/star/6it
    https://www.javbus.com/star/op6
    https://www.javbus.com/star/ysc
    https://www.javbus.com/star/ysb
    https://www.javbus.com/star/ysa
    https://www.javbus.com/star/lcx
    https://www.javbus.com/star/ysg
    https://www.javbus.com/star/ysf
    https://www.javbus.com/star/yse
    https://www.javbus.com/star/ysd
    https://www.javbus.com/star/obr
    https://www.javbus.com/star/ysl
    https://www.javbus.com/star/4ys
    https://www.javbus.com/star/ysi
    https://www.javbus.com/star/obw
    https://www.javbus.com/star/obv
    https://www.javbus.com/star/obu
    https://www.javbus.com/star/obt
    https://www.javbus.com/star/obs
    https://www.javbus.com/star/bhl
    https://www.javbus.com/star/oc0
    https://www.javbus.com/star/obz
    https://www.javbus.com/star/gmn
    https://www.javbus.com/star/ege
    https://www.javbus.com/star/obx
    https://www.javbus.com/star/xm9
    https://www.javbus.com/star/oc2
    https://www.javbus.com/star/oc1
    https://www.javbus.com/star/1fh
    https://www.javbus.com/star/j7d
    https://www.javbus.com/star/v28
    https://www.javbus.com/star/f27
    https://www.javbus.com/star/o5k
    https://www.javbus.com/star/o5m
    https://www.javbus.com/star/o5l
    https://www.javbus.com/star/o5j
    https://www.javbus.com/star/z10
    https://www.javbus.com/star/z11
    https://www.javbus.com/star/yfk
    https://www.javbus.com/star/xuj
    https://www.javbus.com/star/p5u
    https://www.javbus.com/star/ig2
    https://www.javbus.com/star/nzd
    https://www.javbus.com/star/p67
    https://www.javbus.com/star/p66
    https://www.javbus.com/star/nlj
    https://www.javbus.com/star/nli
    https://www.javbus.com/star/8l8
    https://www.javbus.com/star/w3i
    https://www.javbus.com/star/3gf
    https://www.javbus.com/star/pz8
    https://www.javbus.com/star/pdu
    https://www.javbus.com/star/d5c
    https://www.javbus.com/star/a6t
    https://www.javbus.com/star/iok
    https://www.javbus.com/star/yos
    https://www.javbus.com/star/9zw
    https://www.javbus.com/star/fc2
    https://www.javbus.com/star/lni
    https://www.javbus.com/star/sdl
    https://www.javbus.com/star/kh4
    https://www.javbus.com/star/ywh
    https://www.javbus.com/star/at0
    https://www.javbus.com/star/alw
    https://www.javbus.com/star/4w5
    https://www.javbus.com/star/s75
    https://www.javbus.com/star/atn
    https://www.javbus.com/star/blz
    https://www.javbus.com/star/xc5
    https://www.javbus.com/star/tlg
    https://www.javbus.com/star/p8z
    https://www.javbus.com/star/gk3
    https://www.javbus.com/star/cls
    https://www.javbus.com/star/v6k
    https://www.javbus.com/star/li3
    https://www.javbus.com/star/cm3
    https://www.javbus.com/star/b89
    https://www.javbus.com/star/tsp
    https://www.javbus.com/star/e75
    https://www.javbus.com/star/kio
    https://www.javbus.com/star/noo
    https://www.javbus.com/star/gdq
    https://www.javbus.com/star/naj
    https://www.javbus.com/star/bu3
    https://www.javbus.com/star/yka
    https://www.javbus.com/star/em1
    https://www.javbus.com/star/hkm
    https://www.javbus.com/star/p2z
    """
    split = strs.strip().split("\n")

    results = patch_new_cookie_for_403(urls=set(split))
    print(results)


def test_key_value_of_dict():
    a = {"a": 1, "b": 2}
    for key, value in a.items():
        print(key, value)


def test_config_with_ini():
    from javbus_scrapy import global_config
    print(global_config.items('spider_config'))
    print(global_config.get('spider_config', 'data_store_name'))
    print(global_config['spider_config']['data_store_name'])
    print(global_config['spider_config']['proxy_detail'])


def test_latest_csv_pair_data_tuple_path():
    print(latest_csv_pair_data_tuple_path(DATA_STORE, "actresses"))


def change_store_line_formate(file_abs_path: str = None):
    with open(
            "/Users/sunrise/CodeGround/PycharmProjects/javbus_scrapy/data_store/starinfo/uncensored_starinfo_2022-07-13.csv",
            "r") as file:
        readlines = file.readlines()
        for line in readlines:
            split = line.split(",")
            new_line = None
            if len(split) > 14:
                padding = len(split) - 14
                habbits = ",".join(split[len(split) - padding - 1:])
                left = "|".join(split[:len(split) - padding - 1])
                join = ",".join(split).replace(habbits, "") + habbits
                print(left + "|" + habbits)
                # print(join)
                # print(padding)
                # print(habbits)
                # print(split)
                new_line = left + "|" + habbits
                line_strip = new_line.strip()
                new_line = line_strip + "\n"
            else:
                new_line = "|".join(split)
                strip = new_line.strip()
                new_line = strip + "\n"

            with open("new_line.txt", "a+") as f:
                f.write(new_line)


if __name__ == '__main__':
    # test_make_actresses_header()
    # test_fetch_page_with_cookie_all()
    # test_list_sort()
    # test_str_end_with_num()
    # test_multi_line_str_code()
    # test_magnet_to_torrent()
    # test_libtorrent_files()
    # test_select_from_file()
    # test_re_extract_html_content()
    # test_check_str_is_a_valid_url("")
    # test_process_str_with_rn()
    # test_check_page_is_404()
    # test_config_with_ini()
    # test_latest_csv_pair_data_tuple_path()
    # print(",".join(list(("?" * len([1, 2, 3])))))
    pass
