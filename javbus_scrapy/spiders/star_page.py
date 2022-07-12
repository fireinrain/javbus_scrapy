import os
import re

import requests
import scrapy
from scrapy import signals, Request
from scrapy.exceptions import DontCloseSpider

from javbus_scrapy import utils
from javbus_scrapy.items import JavbusStarItemInfoScrapyItem, JavbusStarInfoScrapyItem


# 每一个star 页 默认的每一页作品数量为30
class StarPageSpider(scrapy.Spider):
    name = 'star_page'
    allowed_domains = ['javbus.com']
    base_url = "https://www.javbus.com"
    start_urls = ["https://www.javbus.com/star/okq", "https://www.javbus.com/uncensored/star/39p"]
    # start_urls = ["https://www.javbus.com/uncensored/star/3cj"]
    # "https://www.javbus.com/uncensored/star/39p"
    cookie_list = []
    cookies = {}
    actresses_file_exists = False

    handle_httpstatus_list = [404, 403]

    actresses_files = []

    # key is url,value is None
    interrupt_bad_url = {}

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        # 插入settings
        settings = crawler.settings
        spider = cls(crawler, settings, **kwargs)
        # 使用信号 在scrapy 触发特定时间 主动调用注册的方法
        # https://docs.scrapy.org/en/latest/topics/signals.html
        crawler.signals.connect(spider.spider_idle, signal=signals.spider_idle)
        return spider

    def __init__(self, crawler, settings, **kwargs):
        super().__init__(**kwargs)
        self.settings = settings
        self.crawler = crawler

        if not self.cookie_list:
            # 如果cookie列表不存在 那么就先请求cookie
            # 先去访问javbus.com 主页
            if not self.cookie_list:
                # 如果cookie列表不存在 那么就先请求cookie
                # 先去访问javbus.com 主页
                session = requests.Session()
                session.proxies = self.settings['REQUESTS_PROXIES']
                response = session.get(self.base_url)
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
                # 访问详情页需要加上该cookie项
                self.cookies.update(
                    {"starinfo": "glyphicon%20glyphicon-plus", "genreinfo": "glyphicon%20glyphicon-minus"})
                cookie_str = "; ".join(result)
                self.cookie_list.append(cookie_str)
                self.log(f"{self.__class__.__name__} 当前获取到cookie_strs: {self.cookie_list}")

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
        actress_file_dir = os.path.join(data_store_, self.settings['ACTRESSES_PATH_NAME'])
        if not os.path.exists(actress_file_dir):
            self.actresses_file_exists = False
        else:
            listdir = os.listdir(actress_file_dir)
            files = [i for i in listdir if i != ".DS_Store"]
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
                                         meta={"censored": True}, dont_filter=True)
                else:
                    yield scrapy.Request(url, self.parse,
                                         headers=utils.make_star_page_header(url, self.base_url), cookies=self.cookies,
                                         meta={"censored": False}, dont_filter=True)
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
                # 检查url是否合法
                valid_url = utils.check_a_str_is_valid_url(url)
                if not valid_url:
                    self.log(f"{self.__class__.__name__} 当前url:{url} 不合法,已跳过")
                    continue
                yield scrapy.Request(url, self.parse,
                                     headers=utils.make_star_page_header(url, self.base_url),
                                     cookies=self.cookies,
                                     meta={"censored": censored}, dont_filter=True)

    def parse(self, response):
        url = response.request.url
        if response.status != 200:
            self.log(f"无法访问当前页面: {url}")
            if response.status == 403:
                self.interrupt_bad_url[url] = None
            return

        if utils.is_first_star_page_url(url):
            # 只在访问第一页的时候 进行个人信息抽取
            # 个人信息抽取
            # https://www.javbus.com/uncensored/star/371/3
            # https://www.javbus.com/star/okq/6
            yield from self.fetch_star_info_item(response)

        yield from self.fetch_star_item_info(response)

        yield from self.fetch_next_page(response)

    # 获取star info item
    def fetch_star_info_item(self, response):
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
    def fetch_star_item_info(self, response):
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
            findall = None
            if movie_code is None:
                self.log(f"在star page: {response.request.url} 页面无法抽取movie_code:{movie_url}的番号,尝试使用正则抽取")
                text = item_node.get()
                findall = re.findall(r'<date>(.*?)</date>', text)
                movie_code = findall[0]

            item['movie_code'] = movie_code.strip()
            # 发布日期
            movie_publish_date = item_node.xpath('./div[2]/span/date[2]/text()').extract_first()
            if movie_publish_date is None:
                self.log(f"在star page: {response.request.url} 页面无法抽取movie_publish_date:{movie_url}的番号,尝试使用正则抽取")
                movie_publish_date = findall[1]

            item['movie_publish_date'] = movie_publish_date.strip()
            # 高清标识
            resolution = item_node.xpath('./div[2]/span/div/button[1]/text()').extract_first()
            if resolution is None:
                self.log(f"在star page: {response.request.url} 页面无法抽取resolution:{movie_url}的番号,尝试使用正则抽取")
                text = item_node.get()
                findall = re.findall(r'新種', text)
                if len(findall) > 0:
                    resolution = "高清"
            if resolution is not None:
                item['movie_has_magnet'] = True
                item['movie_resolutions'] = resolution.strip()
            # 字幕
            subtitle = item_node.xpath('./div[2]/span/div/button[2]/text()').extract_first()
            if subtitle is None:
                self.log(f"在star page: {response.request.url} 页面无法抽取subtitle:{movie_url}的番号,尝试使用正则抽取")
                text = item_node.get()
                findall = re.findall(r'字幕', text)
                if len(findall) > 0:
                    subtitle = "字幕"
            if subtitle is not None:
                item['movie_has_subtitle'] = True
                item['movie_subtitle_flag'] = subtitle.strip()
            yield item

        # 补全出现404 或者是403 没法访问的url 通过检测
        # 排除404 的url 对403的连接 采取新的cookie来访问

    def spider_idle(self, spider):
        self.log(f"{self.__class__.__name__} scrpay is going to be idle......")
        self.log(f"{self.__class__.__name__} 准备进行补爬......")
        if len(self.interrupt_bad_url) < 0:
            return
        result = utils.patch_new_cookie_for_403(self.interrupt_bad_url.keys())
        if result is None:
            return
        urls = result[0]
        if len(urls) <= 0:
            return
        cookies = result[1]

        for i in urls:
            self.log(f"{self.__class__.__name__} 正在进行补爬,url: {i}")
            censored = True
            if "uncensored" in i:
                censored = False
            req = Request(i,
                          callback=self.parse,
                          headers=utils.make_star_page_header(i, self.base_url),
                          cookies=cookies, meta={"censored": censored},
                          errback=lambda: self.log(f"{self.__class__.__name__} 补爬{i}出现错误!!!"), dont_filter=True)
            self.crawler.engine.crawl(req)
            # 及时移除已经patch的url 否则会进入无限循环
            self.interrupt_bad_url.pop(i)
            # 修改scrapy的统计
            self.crawler.stats.inc_value(f'downloader/response_status_count/403', spider=self, count=-1)

        raise DontCloseSpider(Exception("waiting for patch crawl......"))

    @staticmethod
    def close(spider, reason):
        return super().close(spider, reason)
