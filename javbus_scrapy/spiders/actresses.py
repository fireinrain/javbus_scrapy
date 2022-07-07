import os

import scrapy
import requests
from .. import utils

# 演员表爬取页面
from ..items import JavbusActressScrapyItem


class ActressesSpider(scrapy.Spider):
    name = 'actresses'
    base_url = 'https://javbus.com'
    allowed_domains = ['javbus.com']
    # 包含有码无码演员
    start_urls = ['https://javbus.com/actresses', 'https://www.javbus.com/uncensored/actresses']
    cookie_list = []
    cookies = {}

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
                value = item[1]
                key_value = key + "=" + value
                result.append(key_value)
                self.cookies.update({key: value})
            cookie_str = "; ".join(result)
            self.cookie_list.append(cookie_str)
            self.log(f"当前获取到cookie_strs: {self.cookie_list}")

    def start_requests(self):
        data_store_ = self.settings['DATA_STORE']
        actress_file_dir = os.path.join(data_store_, utils.ACTRESSES_PATH_NAME)
        if not os.path.exists(actress_file_dir):
            os.makedirs(actress_file_dir)
        if self.settings['CENSORED'] == "all":
            for url in self.start_urls:
                yield scrapy.Request(url, self.parse,
                                     headers=utils.make_actresses_header(url, self.base_url), cookies=self.cookies)
        elif self.settings['CENSORED'] == "censored":
            yield scrapy.Request(self.start_urls[0], self.parse,
                                 headers=utils.make_actresses_header(self.start_urls[0], self.base_url),
                                 cookies=self.cookies)
        elif self.settings['CENSORED'] == "uncensored":
            yield scrapy.Request(self.start_urls[1], self.parse,
                                 headers=utils.make_actresses_header(self.start_urls[1], self.base_url),
                                 cookies=self.cookies)

    def parse(self, response):
        if response.status != 200:
            self.log(f"无法访问当前页面: {response.request.url}")
            return
        # print(response.text)
        star_nodes = response.xpath('//*[@id="waterfall"]/div/a')
        for star_node in star_nodes:
            actresses = JavbusActressScrapyItem()
            actresses['censored'] = True
            if "uncensored" in response.request.url:
                actresses['censored'] = False
            actresses['name'] = star_node.xpath('./div[2]/span/text()').extract_first()
            actresses['head_photo_url'] = star_node.xpath('./div[1]/img/@src').extract_first()
            actresses['star_page_url'] = star_node.xpath('./@href').extract_first()
            self.log(f"------------------------------{actresses}")
            yield actresses

        # find next page
        next_page = response.xpath('//*[@id="next"]')
        if next_page is not None:
            relative_next_page = next_page.xpath('./@href').extract_first()
            # 存在next page 才进行请求
            if relative_next_page is not None:
                next_page = self.base_url + relative_next_page
                pre_page_url = response.request.url
                yield scrapy.Request(next_page, self.parse,
                                     headers=utils.make_actresses_header(next_page, pre_page_url), cookies=self.cookies)

    @staticmethod
    def close(spider, reason):
        return super().close(spider, reason)
