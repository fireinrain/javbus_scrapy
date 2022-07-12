import os

import requests
import scrapy
from scrapy import signals, Request
from scrapy.exceptions import DontCloseSpider

from javbus_scrapy import utils
from javbus_scrapy.items import JavbusMovieDetailItem, JavbusMovieDetailTorrentItem


class MovieSpider(scrapy.Spider):
    name = 'movie'
    allowed_domains = ['javbus.com']
    base_url = "https://www.javbus.com"
    torrent_fetch_url = "https://www.javbus.com/ajax/uncledatoolsbyajax.php"

    # start_urls = ['https://www.javbus.com/SSNI-388']
    start_urls = []

    cookie_list = []
    cookies = {}

    staritem_info_file_exists = False

    staritem_info_files = []

    handle_httpstatus_list = [404, 403]

    # key is url,value is actresses_
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
            self.cookies.update({"starinfo": "glyphicon%20glyphicon-plus", "genreinfo": "glyphicon%20glyphicon-minus"})
            cookie_str = "; ".join(result)
            self.cookie_list.append(cookie_str)
            self.log(f"{self.__class__.__name__} 当前获取到cookie_strs: {self.cookie_list}")

    @staticmethod
    def get_latest_stariteminfo_file_tuple(files) -> [[], ]:
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
        star_item_info_dir = os.path.join(data_store_, self.settings['STARITEMINFO_PATH_NAME'])
        if not os.path.exists(star_item_info_dir):
            self.staritem_info_file_exists = False
        else:
            listdir = os.listdir(star_item_info_dir)
            files = [i for i in listdir if i != ".DS_Store"]
            file_tuple = self.get_latest_stariteminfo_file_tuple(files)
            self.staritem_info_file_exists = True
            self.staritem_info_files = file_tuple[0]
        # print(data_store_)
        # 用作测试
        if len(self.start_urls) > 0:
            self.staritem_info_file_exists = False
        if len(self.start_urls) > 0 and (not self.staritem_info_file_exists):
            for url in self.start_urls:
                # do not save to file
                yield scrapy.Request(url, self.parse,
                                     headers=utils.make_movie_detail_header(url, self.base_url),
                                     cookies=self.cookies,
                                     meta={"saveFile": False})

        # 读取文件
        else:
            if self.settings['CENSORED'] == "all":
                for file in self.staritem_info_files:
                    path_join = os.path.join(star_item_info_dir, file)
                    if file.startswith("censored"):
                        yield from self.fetch_all_stariteminfo_file_url(path_join, True)
                    elif file.startswith("uncensored"):
                        yield from self.fetch_all_stariteminfo_file_url(path_join, False)

            elif self.settings['CENSORED'] == "censored":
                censored_actresses = self.staritem_info_files[0]
                path_join = os.path.join(star_item_info_dir, censored_actresses)
                yield from self.fetch_all_stariteminfo_file_url(path_join, True)
            elif self.settings['CENSORED'] == "uncensored":
                uncensored_actresses = self.staritem_info_files[1]
                path_join = os.path.join(star_item_info_dir, uncensored_actresses)
                yield from self.fetch_all_stariteminfo_file_url(path_join, False)

    def fetch_all_stariteminfo_file_url(self, path_join, censored):
        with open(path_join, "r") as file:
            while True:
                readline = file.readline()
                if readline == "":
                    break
                readline_split = readline.split(",")
                # star main page url
                url = readline_split[1].strip()
                yield scrapy.Request(url, self.parse,
                                     headers=utils.make_movie_detail_header(url, self.base_url),
                                     cookies=self.cookies,
                                     meta={"censored": censored})

    def parse(self, response):
        url = response.request.url
        if response.status != 200:
            self.log(f"{self.__class__.__name__} 无法访问当前页面: {url}")
            if response.status == 403:
                self.interrupt_bad_url[url] = response.meta['censored']
            return

        movie_detail_item = JavbusMovieDetailItem()
        movie_title = response.xpath('/html/body/div[5]/h3/text()').get(default="")
        movie_detail_item['movie_title'] = movie_title

        if 'censored' in response.meta.keys():
            movie_detail_item['movie_censored'] = response.meta['censored']
        else:
            movie_detail_item['movie_censored'] = True
        movie_detail_item['movie_url'] = url

        movie_detail_item['movie_cover_url'] = response.xpath('/html/body/div[5]/div[1]/div[1]/a/img/@src').get(
            default="")

        # 右侧边栏信息
        info_nodes = response.xpath('/html/body/div[5]/div[1]/div[2]/p')
        process_later_nodes = {}
        if len(info_nodes) > 0:
            for index, item in enumerate(info_nodes):
                all_list = item.xpath('.//text()').getall()
                all_list = [i.strip() for i in all_list]
                line = "".join(all_list)

                # 类别和演员列表特殊处理
                if line == "類別:" or line == "演員:":
                    process_later_nodes[index + 1] = info_nodes[index + 1]
                    continue
                if index in process_later_nodes.keys():
                    continue

                line_split = line.split(":")
                key = line_split[0].strip()
                value = line_split[1].strip()
                if "識別碼" == key:
                    movie_detail_item['movie_code'] = value
                    movie_code = value
                    continue
                if "發行日期" == key:
                    movie_detail_item['movie_publish_date'] = value
                    continue
                if "長度" == key:
                    movie_detail_item['movie_duration'] = value
                    continue
                if "導演" == key:
                    movie_detail_item['movie_directors'] = value
                    continue
                if "製作商" == key:
                    movie_detail_item['movie_maker'] = value
                    continue
                if "發行商" == key:
                    movie_detail_item['movie_publisher'] = value
                    continue
                if "系列" == key:
                    movie_detail_item['movie_series'] = value
                    continue
                # if "類別" == key:
                #     movie_detail_item['movie_tags'] = value
                #     continue
                # if "演員" == key:
                #     movie_detail_item['movie_stars'] = value
                #     continue
        # 该xpath 可以获取span中的text和 span后的text
        tags = process_later_nodes[min(process_later_nodes.keys())].xpath(
            './/text()').getall()
        tags = [i.strip() for i in tags if i.strip() != ""]
        tags_line = "|".join(tags)
        movie_detail_item['movie_tags'] = tags_line

        stars = process_later_nodes[max(process_later_nodes.keys())].xpath(
            './/text()').getall()
        stars = [i.strip() for i in stars if i.strip() != ""]
        stars_line = "|".join(stars)
        movie_detail_item['movie_stars'] = stars_line
        sample_image_nodes = response.xpath('//*[@id="sample-waterfall"]/a')
        if sample_image_nodes is not None and len(sample_image_nodes) > 0:
            images = []
            for i in sample_image_nodes:
                img_url = i.xpath('./@href').get(default="")
                images.append(img_url)
            movie_detail_item['movie_sample_photo_urls'] = "|".join(images)

        # 如果只是测试 不需要写入文件
        # if 'saveFile' in response.meta.keys():
        #     return
        # else:
        yield movie_detail_item

        # 获取torrent列表
        # https://www.javbus.com/ajax/uncledatoolsbyajax.php?gid=50677872538&lang=zh&img=/pics/cover/90o5_b.jpg&uc=0&floor=953
        # ?gid=50677872538&lang=zh&img=/pics/cover/90o5_b.jpg&uc=0&floor=953
        torrent_req_params = response.xpath("/html/body/script[3]/text()").getall()[0]
        torrent_req_params = torrent_req_params.split(";")
        gid = torrent_req_params[0].strip().replace("var gid = ", "")
        uc = torrent_req_params[1].strip().replace("var uc = ", "")
        img = torrent_req_params[2].strip().replace("var img = ", "")
        # make "'xxxx'" to 'xxxx'
        img = eval(img)
        req_url = utils.make_torrent_req_url(self.torrent_fetch_url, {"gid": gid, "lang": "zh", "uc": uc, "img": img})
        yield scrapy.Request(req_url, self.parse_torrent_response,
                             headers=utils.make_torrent_req_header(req_url, url, self.torrent_fetch_url),
                             cookies=self.cookies,
                             meta={"movie_detail_item": movie_detail_item})

    # 解析torrent获取列表请求
    def parse_torrent_response(self, response):
        url = response.request.url
        movie_detail_item = response.meta['movie_detail_item']
        if response.status != 200:
            self.log(f"{self.__class__.__name__} 无法获取当前请求的torrent列表: {url}")
            return

        torrent_item = JavbusMovieDetailTorrentItem()
        torrent_item['movie_code'] = movie_detail_item['movie_code']
        torrent_item['movie_censored'] = movie_detail_item['movie_censored']
        torrent_item['movie_url'] = movie_detail_item['movie_url']
        torrent_nodes = response.xpath('//tr')

        if "暫時沒有磁力連結" in response.text:
            self.log(f"该番号: {movie_detail_item['movie_code']},暂无磁力链接！！！")
            return
        # if "" == torrent_nodes[0].xpath('./td/text()').get().strip():
        # torrent_is_checking = item.xpath('//tr/td/text()').get()
        #             if torrent_is_checking == "下方磁力連結尚在審核中":
        #                 continue

        all_torrent_list = []
        # 格式  name/magnet_str/resolution/subtitle/file_size/share_date
        for item in torrent_nodes:
            line = []
            if item.xpath('./td/text()').get().strip() == "下方磁力連結尚在審核中":
                continue
            # torrent_line_nodes = item.xpath("//td")
            # name_node = torrent_line_nodes[0]
            name_node = item.xpath('./td')[0]
            # torrent_nodes[1].xpath("./td").get()
            torrent_str = name_node.xpath('.//a/@href').get(default="")
            header_node = name_node.xpath('.//a/text()').getall()

            header_node = [i.strip() for i in header_node if i != ""]
            name = header_node[0]
            line.append(name)
            line.append(torrent_str)

            if "高清" in header_node:
                resolution = "高清"
            else:
                resolution = ""
            line.append(resolution)
            if "字幕" in header_node:
                subtitle = "字幕"
            else:
                subtitle = ""
            line.append(subtitle)

            size_node = item.xpath('./td')[1]
            file_size = size_node.xpath('./a/text()').get(default="")
            line.append(file_size.strip())

            share_date = item.xpath('./td')[2]
            file_share_date = share_date.xpath('./a/text()').get(default="")
            line.append(file_share_date.strip())

            torrent_line = "/".join(line)
            all_torrent_list.append(torrent_line)
        all_torrent_line = "|".join(all_torrent_list)

        torrent_item['torrent_list_str'] = all_torrent_line

        yield torrent_item

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
            req = Request(i,
                          callback=self.parse,
                          headers=utils.make_movie_detail_header(i, self.base_url),
                          cookies=cookies, meta={"censored": self.interrupt_bad_url[i]},
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
