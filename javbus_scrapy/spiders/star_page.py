import os

import requests
import scrapy

from javbus_scrapy import utils
from javbus_scrapy.items import JavbusStarItemInfoScrapyItem, JavbusStarInfoScrapyItem


class StarPageSpider(scrapy.Spider):
    name = 'star_page'
    allowed_domains = ['javbus.com']
    base_url = "https://javbus.com"
    start_urls = ["https://www.javbus.com/star/okq", "https://www.javbus.com/uncensored/star/39p"]
    # "https://www.javbus.com/uncensored/star/39p"
    cookie_list = []
    cookies = {}
    actresses_file_exists = False

    actresses_files = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.cookie_list:
            # 如果cookie列表不存在 那么就先请求cookie
            # 先去访问javbus.com 主页
            response = requests.get(self.base_url)
            items = response.cookies.items()
            result = []
            for item in items:
                key = item[0]
                # 默认获取所有作品
                if key == "existmag":
                    value = "all"
                else:
                    value = item[1]
                key_value = key + "=" + value
                result.append(key_value)
                self.cookies.update({key: value})
            cookie_str = "; ".join(result)
            self.cookie_list.append(cookie_str)
            self.log(f"当前获取到cookie_strs: {self.cookie_list}")

    # 获取最新的actresses file
    @staticmethod
    def get_latest_actress_file_tuple(files) -> [[], ]:
        s = set()
        result = []
        for f in files:
            f_split = f.split("_")
            s.add(f_split[2])
        for date_str in s:
            pair = []
            for f in files:
                if date_str in f:
                    pair.append(f)
                    pair.sort(key=lambda x: x.startswith("censored"), reverse=True)
            result.append(pair)
        result.sort(key=lambda x: x[0].split("_")[2], reverse=True)
        return result

    def start_requests(self):
        # 读取最新的actresses 目录
        data_store_ = self.settings['DATA_STORE']
        actress_file_dir = os.path.join(data_store_, utils.ACTRESSES_PATH_NAME)
        if not os.path.exists(actress_file_dir):
            self.actresses_file_exists = False
        else:
            listdir = os.listdir(actress_file_dir)
            files = [i for i in listdir if listdir != ".DS_Store"]
            file_tuple = self.get_latest_actress_file_tuple(files)
            self.actresses_file_exists = True
            self.actresses_files = file_tuple[0]
        # print(data_store_)
        # 用作测试
        if len(self.start_urls) > 0 and (not self.actresses_file_exists):
            for url in self.start_urls:
                if "uncensored" not in url:
                    # 从文件中读取
                    yield scrapy.Request(url, self.parse,
                                         headers=utils.make_star_page_header(url, self.base_url), cookies=self.cookies,
                                         meta={"censored": True})
                else:
                    yield scrapy.Request(url, self.parse,
                                         headers=utils.make_star_page_header(url, self.base_url), cookies=self.cookies,
                                         meta={"censored": False})
        # 读取文件
        else:
            if self.settings['CENSORED'] == "all":
                for file in self.actresses_files:
                    path_join = os.path.join(actress_file_dir, file)
                    if file.startswith("censored"):
                        yield from self.fetch_all_actress_file_url(path_join, True)
                    elif file.startswith("uncensored"):
                        yield from self.fetch_all_actress_file_url(path_join, False)

            elif self.settings['CENSORED'] == "censored":
                censored_actresses = self.actresses_files[0]
                path_join = os.path.join(actress_file_dir, censored_actresses)
                yield from self.fetch_all_actress_file_url(path_join, True)
            elif self.settings['CENSORED'] == "uncensored":
                uncensored_actresses = self.actresses_files[1]
                path_join = os.path.join(actress_file_dir, uncensored_actresses)
                yield from self.fetch_all_actress_file_url(path_join, False)

    def fetch_all_actress_file_url(self, path_join, censored):
        with open(path_join, "r") as file:
            while True:
                readline = file.readline()
                if readline == "":
                    break
                readline_split = readline.split(",")
                # star main page url
                url = readline_split[1].strip()
                yield scrapy.Request(url, self.parse,
                                     headers=utils.make_star_page_header(url, self.base_url),
                                     cookies=self.cookies,
                                     meta={"censored": censored})

    def parse(self, response):
        url = response.request.url
        if response.status != 200:
            self.log(f"无法访问当前页面: {url}")
            return

        if utils.is_first_star_page_url(url):
            # 只在访问第一页的时候 进行个人信息抽取
            # 个人信息抽取
            # https://www.javbus.com/uncensored/star/371/3
            # https://www.javbus.com/star/okq/6
            yield from self.fetch_star_info_item(response)

        # yield from self.fetch_star_item_info(response)

        yield from self.fetch_next_page(response)

    # 获取star info item
    @staticmethod
    def fetch_star_info_item(response):
        star_name = response.xpath('//*[@id="waterfall"]/div[1]/div/div[2]/span/text()').extract_first()
        star_info_item = JavbusStarInfoScrapyItem()
        all_item_counts = response.xpath('//*[@id="resultshowall"]/text()').getall()
        all_item_counts = "".join(all_item_counts).replace("全部影片", "").strip()
        star_info_item['all_item_counts'] = all_item_counts
        magnet_item_counts = response.xpath('//*[@id="resultshowmag"]/text()').getall()
        magnet_item_counts = "".join(magnet_item_counts).replace("已有磁力", "").strip()
        star_info_item['magnet_item_counts'] = magnet_item_counts
        photo_info_nodes = response.xpath('//*[@id="waterfall"]/div[1]/div/div[2]/p')
        # 先给定默认值
        star_info_item['birthday'] = ''
        star_info_item['age'] = ''
        star_info_item['height'] = ''
        star_info_item['cup'] = ''
        star_info_item['chest_circumference'] = ''
        star_info_item['waistline'] = ''
        star_info_item['hip_circumference'] = ''
        star_info_item['birthplace'] = ''
        star_info_item['habbits'] = ''
        if len(photo_info_nodes) > 0:
            for item in photo_info_nodes:
                line = item.xpath('./text()').get()
                line_split = line.split(":")
                key = line_split[0].strip()
                value = line_split[1].strip()
                if "生日" == key:
                    star_info_item['birthday'] = value
                    continue
                if "年齡" == key:
                    star_info_item['age'] = value
                    continue
                if "身高" == key:
                    star_info_item['height'] = value
                    continue
                if "罩杯" == key:
                    star_info_item['cup'] = value
                    continue
                if "胸圍" == key:
                    star_info_item['chest_circumference'] = value
                    continue
                if "腰圍" == key:
                    star_info_item['waistline'] = value
                    continue
                if "臀圍" == key:
                    star_info_item['hip_circumference'] = value
                    continue
                if "出生地" == key:
                    star_info_item['birthplace'] = value
                    continue
                if "愛好" == key:
                    star_info_item['habbits'] = value
                    continue
        star_info_item['star_name'] = star_name
        star_photo_url = response.xpath('//*[@id="waterfall"]/div[1]/div/div[1]/img/@src').extract_first()
        star_info_item['star_head_photo_url'] = star_photo_url
        if not response.meta['censored']:
            star_info_item['censored_star'] = False
        else:
            star_info_item['censored_star'] = True
        yield star_info_item

    # 获取下一页
    def fetch_next_page(self, response):
        # next page forward
        next_page = response.xpath('//*[@id="next"]')
        if next_page is not None:
            relative_next_page = next_page.xpath('./@href').extract_first()
            # 存在next page 才进行请求
            if relative_next_page is not None:
                next_page = self.base_url + relative_next_page
                pre_page_url = response.request.url
                yield scrapy.Request(next_page, self.parse,
                                     headers=utils.make_star_page_header(next_page, pre_page_url), cookies=self.cookies,
                                     meta=response.meta)

    # 获取stariteminfo
    @staticmethod
    def fetch_star_item_info(response):
        star_name = response.xpath('//*[@id="waterfall"]/div[1]/div/div[2]/span/text()').extract_first()
        # 是否是有码作品
        censored_star = True
        if not response.meta['censored']:
            censored_star = False
        # 作品信息抽取
        star_item_info_nodes = response.xpath('//*[@id="waterfall"]/div/a')
        for item_node in star_item_info_nodes:
            item = JavbusStarItemInfoScrapyItem()
            # 作品封面图片地址
            movie_cover_url = item_node.xpath('./div[1]/img/@src').extract_first()
            item['movie_cover_url'] = movie_cover_url.strip()
            # 作品详情地址
            movie_url = item_node.xpath('./@href').extract_first()
            item['movie_url'] = movie_url.strip()
            # 演员名
            item['star_name'] = star_name
            # 是否有码标识
            item['movie_censored'] = censored_star
            # 作品名
            movie_title = item_node.xpath('./div[1]/img/@title').extract_first()
            item['movie_title'] = movie_title.strip()
            # 作品番号
            movie_code = item_node.xpath('./div[2]/span/date[1]/text()').extract_first()
            item['movie_code'] = movie_code.strip()
            # 发布日期
            movie_publish_date = item_node.xpath('./div[2]/span/date[2]/text()').extract_first()
            item['movie_publish_date'] = movie_publish_date.strip()
            # 高清标识
            resolution = item_node.xpath('./div[2]/span/div/button[1]/text()').extract_first()
            if resolution is not None:
                item['movie_has_magnet'] = True
                item['movie_resolutions'] = resolution.strip()
            # 字幕
            subtitle = item_node.xpath('./div[2]/span/div/button[2]/text()').extract_first()
            if subtitle is not None:
                item['movie_has_subtitle'] = True
                item['movie_subtitle_flag'] = subtitle.strip()
            yield item
