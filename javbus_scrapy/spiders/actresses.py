import os

import requests
import scrapy
from scrapy import signals, Request
from scrapy.exceptions import DontCloseSpider

from .. import utils
# 演员表爬取页面
from ..items import JavbusActressScrapyItem


# https://www.javbus.com/actresses/913
# https://www.javbus.com/uncensored/actresses/437
class ActressesSpider(scrapy.Spider):
    name = 'actresses'
    base_url = 'https://www.javbus.com'
    allowed_domains = ['javbus.com']
    # 包含有码无码演员
    # start_urls = ['https://javbus.com/actresses', 'https://www.javbus.com/uncensored/actresses']
    censored_index_url = "https://javbus.com/actresses"
    uncensored_index_url = "https://www.javbus.com/uncensored/actresses"
    start_urls = None
    # start_urls = ["https://www.javbus.com/actresses/208", "https://www.javbus.com/uncensored/actresses/404"]
    cookie_list = []
    cookies = {}
    # 自己翻页默认为生成翻页
    pre_link_mode = True

    handle_httpstatus_list = [404, 403]

    # key is url,value is actresses_
    interrupt_bad_url = {}

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(ActressesSpider, cls).from_crawler(crawler, *args, **kwargs)
        # 使用信号 在scrapy 触发特定时间 主动调用注册的方法
        # https://docs.scrapy.org/en/latest/topics/signals.html
        crawler.signals.connect(spider.spider_idle, signal=signals.spider_idle)
        return spider

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 初始化url
        if self.start_urls is None and self.pre_link_mode:
            self.start_urls = [[self.censored_index_url + "/" + str(i) for i in range(1, 914)],
                               [self.uncensored_index_url + "/" + str(i) for i in range(1, 438)]]
        else:
            self.pre_link_mode = False

        if not self.cookie_list:
            # 如果cookie列表不存在 那么就先请求cookie
            # 先去访问javbus.com 主页
            session = requests.Session()
            session.proxies = utils.requests_proxies
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
            self.cookies.update({"starinfo": "glyphicon%20glyphicon-plus", "genreinfo": "glyphicon%20glyphicon-minus"})
            cookie_str = "; ".join(result)
            self.cookie_list.append(cookie_str)
            self.log(f"当前获取到cookie_strs: {self.cookie_list}")

    def start_requests(self):
        data_store_ = self.settings['DATA_STORE']
        actress_file_dir = os.path.join(data_store_, utils.ACTRESSES_PATH_NAME)
        if not os.path.exists(actress_file_dir):
            os.makedirs(actress_file_dir)
        if self.settings['CENSORED'] == "all":
            if len(self.start_urls) >= 2 and isinstance(self.start_urls[0], list):
                self.start_urls = self.start_urls[0] + self.start_urls[1]
            for url in self.start_urls:
                yield scrapy.Request(url, self.parse,
                                     headers=utils.make_actresses_header(url, self.base_url), cookies=self.cookies)

        elif self.settings['CENSORED'] == "censored":
            if len(self.start_urls) >= 2 and isinstance(self.start_urls[0], list):
                self.start_urls = self.start_urls[0]
                for index, url in enumerate(self.start_urls):
                    if index + 1 == 1:
                        pre_url = self.base_url
                    else:
                        pre_url = self.start_urls[index]
                    yield scrapy.Request(url, self.parse,
                                         headers=utils.make_actresses_header(url, pre_url),
                                         cookies=self.cookies)
            else:
                yield scrapy.Request(self.start_urls[0], self.parse,
                                     headers=utils.make_actresses_header(self.start_urls[0], self.base_url),
                                     cookies=self.cookies)
        elif self.settings['CENSORED'] == "uncensored":
            if len(self.start_urls) >= 2 and isinstance(self.start_urls[0], list):
                self.start_urls = self.start_urls[1]
                for index, url in enumerate(self.start_urls):
                    if index + 1 == 1:
                        pre_url = self.base_url
                    else:
                        pre_url = self.start_urls[index]
                    yield scrapy.Request(url, self.parse,
                                         headers=utils.make_actresses_header(url, pre_url),
                                         cookies=self.cookies)
            else:
                yield scrapy.Request(self.start_urls[1], self.parse,
                                     headers=utils.make_actresses_header(self.start_urls[1], self.base_url),
                                     cookies=self.cookies)

    def parse(self, response):
        if response.status != 200:
            self.log(
                f"无法访问当前页面: {response.request.url} \n response.status: {response.status} "
                f"\n当前客户端header: {response.request.headers} \n当前使用cookie:{response.request.cookies}")
            return
        # print(response.text)
        star_nodes = response.xpath('//*[@id="waterfall"]/div/a')
        for star_node in star_nodes:
            actresses = JavbusActressScrapyItem()
            actresses['censored'] = True
            if "uncensored" in response.request.url:
                actresses['censored'] = False
            name_node = star_node.xpath('./div[2]/span/text()').get()
            if name_node is None:
                # 从title中获取
                name_node = star_node.xpath('./div[1]/img/@title').get()
            actresses['name'] = name_node.strip()

            head_photo_url = star_node.xpath('./div[1]/img/@src').get()
            if head_photo_url is not None:
                actresses['head_photo_url'] = head_photo_url.strip()
            star_page_url = star_node.xpath('./@href').get()
            if star_page_url is not None:
                actresses['star_page_url'] = star_page_url.strip()
            page_url_ = actresses['star_page_url']
            # yield actresses
            yield scrapy.Request(page_url_, self.parse_for_latest_movie,
                                 headers=utils.make_star_page_header(page_url_, response.request.url),
                                 cookies=self.cookies,
                                 meta={"actresses": actresses})

        # find next page
        if not self.pre_link_mode:
            next_page = response.xpath('//*[@id="next"]')
            if next_page is not None:
                relative_next_page = next_page.xpath('./@href').extract_first()
                # 存在next page 才进行请求
                if relative_next_page is not None:
                    next_page = self.base_url + relative_next_page
                    pre_page_url = response.request.url
                    yield scrapy.Request(next_page, self.parse,
                                         headers=utils.make_actresses_header(next_page, pre_page_url),
                                         cookies=self.cookies)

    # 获取演员最新一部作品
    # 格式: 番号|时间|作品名
    def parse_for_latest_movie(self, response):
        actresses_ = response.meta['actresses']
        # make "" as default value
        actresses_['latest_movie_url'] = ""
        actresses_['latest_movie_intro'] = ""
        if response.status != 200:
            self.log(f"无法访问当前页面: {response.request.url}")
            # 加入到暂时无法访问url列表 404 403
            # 404 不需要,403换新的cookie 重新爬取一次
            if response.status == 403:
                self.interrupt_bad_url[response.request.url] = actresses_
            return
        first_node = response.xpath('//*[@id="waterfall"]/div/a')
        if first_node is not None and len(first_node) > 0:
            first_node = first_node[0]
            film_url = first_node.xpath('./@href').get().strip()
            film_date = first_node.xpath('./div[2]/span/date[2]/text()').get().strip()
            film_code = first_node.xpath('./div[2]/span/date[1]/text()').get().strip()
            file_name = first_node.xpath('./div[2]/span/text()[1]').get().strip()
            combine_str = "|".join([film_code, film_date, file_name])
            actresses_['latest_movie_url'] = film_url
            actresses_['latest_movie_intro'] = combine_str
        self.log(f"爬取到------------------------------{actresses_}")

        yield actresses_

    # 补全出现404 或者是403 没法访问的url 通过检测
    # 排除404 的url 对403的连接 采取新的cookie来访问
    def spider_idle(self, spider):
        self.log("scrpay is going to be idle......")
        self.log("准备进行补爬......")
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
            self.log(f"正在进行补爬,url: {i}")
            req = Request(i,
                          callback=self.parse_for_latest_movie,
                          headers=utils.make_star_page_header(i, self.base_url),
                          cookies=cookies, meta={"actresses": self.interrupt_bad_url[i]},
                          errback=lambda: self.log(f"补爬{i}出现错误!!!"), dont_filter=True)
            self.crawler.engine.crawl(req)
            # 及时移除已经patch的url 否则会进入无限循环
            self.interrupt_bad_url.pop(i)
            # 修改scrapy的统计
            self.crawler.stats.inc_value(f'downloader/response_status_count/403', spider=self, count=-1)

        raise DontCloseSpider(Exception("waiting for patch crawl......"))

    @staticmethod
    def close(spider, reason):
        return super().close(spider, reason)
