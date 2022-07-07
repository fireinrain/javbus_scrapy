import requests
import scrapy

from javbus_scrapy import utils
from javbus_scrapy.items import JavbusStarItemInfoScrapyItem, JavbusStarInfoScrapyItem


class StarPageSpider(scrapy.Spider):
    name = 'star_page'
    allowed_domains = ['javbus.com']
    base_url = "https://javbus.com"
    start_urls = ["https://www.javbus.com/star/okq", "https://www.javbus.com/uncensored/star/39p"]
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

    def start_requests(self):
        for url in self.start_urls:
            if "uncensored" not in url:
                yield scrapy.Request(url, self.parse,
                                     headers=utils.make_star_page_header(url, self.base_url), cookies=self.cookies,
                                     meta={"censored": True})
            else:
                yield scrapy.Request(url, self.parse,
                                     headers=utils.make_star_page_header(url, self.base_url), cookies=self.cookies,
                                     meta={"censored": False})

    def parse(self, response):
        if response.status != 200:
            self.log(f"无法访问当前页面: {response.request.url}")
            return
        # 个人信息抽取
        star_name = response.xpath('//*[@id="waterfall"]/div[1]/div/div[2]/span/text()').extract_first()

        star_info_item = JavbusStarInfoScrapyItem()
        star_info_item['star_name'] = star_name
        star_photo_url = response.xpath('//*[@id="waterfall"]/div[1]/div/div[1]/img/@src').extract_first()
        star_info_item['star_head_photo_url'] = star_photo_url
        photo_info_node = response.xpath('//*[@id="waterfall"]/div[1]/div/div[2]')

        yield star_info_item

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
