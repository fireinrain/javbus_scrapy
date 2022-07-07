# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os
import time
from javbus_scrapy import utils

from javbus_scrapy.items import JavbusActressScrapyItem, JavbusStarInfoScrapyItem, JavbusStarItemInfoScrapyItem


class JavbusScrapyPipeline:
    def process_item(self, item, spider):
        return item


# 处理actresses item
class JavbusScrapyActressesPipeline:
    # 日期字符串
    process_item_data_str = time.strftime("%Y-%m-%d", time.localtime())
    # 有码文件名
    censored_star_file_name = f"censored_star_{process_item_data_str}.csv"
    # 无码文件名
    uncensored_star_file_name = f"uncensored_star_{process_item_data_str}.csv"
    # 有码存储路径
    censored_path = None
    # 无码存储路径
    uncensored_path = None

    # buffer容器
    censored_star_str_buffer = []
    uncensored_star_str_buffer = []

    # 触发写入文件的buffer大小
    trigger_write_size = 1000
    # 今天已经下载过
    today_has_download = False
    # 没有多余的item需要处理
    no_more_items = False

    @classmethod
    def from_crawler(cls, spider):
        return cls(spider)

    def __init__(self, spider) -> None:
        # 初始化存储目录
        store_path = spider.settings['DATA_STORE'].strip()
        actresses_data_path = os.path.join(store_path, utils.ACTRESSES_PATH_NAME)
        if not os.path.exists(actresses_data_path):
            os.makedirs(actresses_data_path)
        # 判断文件是否下载过
        self.censored_path = os.path.join(actresses_data_path, self.censored_star_file_name)
        self.uncensored_path = os.path.join(actresses_data_path, self.uncensored_star_file_name)
        if os.path.exists(self.censored_path) and (self.process_item_data_str in self.censored_path) \
                and os.path.exists(self.uncensored_path) and (self.process_item_data_str in self.uncensored_path):
            self.today_has_download = True

    # 该方法需要实现的功能为判断当前已经不会有下一个item过来
    def is_no_more_items(self):
        # do something
        self.no_more_items = True
        return self.no_more_items

    # 该方法有bug 无法在pipeline中知道是最后的item
    def write_with_buffered(self, item):
        csv_str = item.get_csv_str()
        if item['censored']:
            self.censored_star_str_buffer.append(csv_str)
            if len(self.censored_star_str_buffer) < self.trigger_write_size:
                return
        else:
            self.uncensored_star_str_buffer.append(csv_str)
            if len(self.uncensored_star_str_buffer) < self.trigger_write_size:
                return

        if len(self.censored_star_str_buffer) == self.trigger_write_size:
            with open(self.censored_path, 'a+') as file:
                # print(f"csv_str:{csv_str}")
                for i in self.censored_star_str_buffer:
                    file.write(i)
                file.flush()
            self.censored_star_str_buffer = []
        if len(self.uncensored_star_str_buffer) == self.trigger_write_size:
            with open(self.uncensored_path, 'a+') as file:
                # print(f"csv_str:{csv_str}")
                for i in self.uncensored_star_str_buffer:
                    file.write(i)
                file.flush()
            self.uncensored_star_str_buffer = []

        if self.is_no_more_items():
            with open(self.censored_path, 'a+') as file:
                # print(f"csv_str:{csv_str}")
                for i in self.censored_star_str_buffer:
                    file.write(i)
                file.flush()
            with open(self.uncensored_path, 'a+') as file:
                # print(f"csv_str:{csv_str}")
                for i in self.uncensored_star_str_buffer:
                    file.write(i)
                file.flush()
            self.censored_star_str_buffer = []
            self.uncensored_star_str_buffer = []

    def process_item(self, item, spider):
        if not isinstance(item, JavbusActressScrapyItem):
            return item

        # process item
        if self.today_has_download:
            spider.log(f"当天下载文件已存在: {self.censored_path}|{self.uncensored_path}")
            return item

        csv_str = item.get_csv_str()
        if item['censored']:
            with open(self.censored_path, 'a+') as file:
                # print(f"csv_str:{csv_str}")
                file.write(csv_str)
        else:
            with open(self.uncensored_path, 'a+') as file:
                file.write(csv_str)


# 处理stariteminfo item
class JavbusScrapyStarItemInfoPipeline:
    # 日期字符串
    process_item_data_str = time.strftime("%Y-%m-%d", time.localtime())
    # 有码文件名
    censored_star_item_info_file_name = f"censored_staritem_{process_item_data_str}.csv"
    # 无码文件名
    uncensored_star_item_info_file_name = f"uncensored_staritem_{process_item_data_str}.csv"
    # 有码存储路径
    censored_path = None
    # 无码存储路径
    uncensored_path = None

    today_has_download = False

    @classmethod
    def from_crawler(cls, spider):
        return cls(spider)

    def __init__(self, spider) -> None:
        # 初始化存储目录
        store_path = spider.settings['DATA_STORE'].strip()
        iteminfo_data_path = os.path.join(store_path, utils.STARITEMINFO_PATH_NAME)
        if not os.path.exists(iteminfo_data_path):
            os.makedirs(iteminfo_data_path)
        # 判断文件是否下载过
        self.censored_path = os.path.join(iteminfo_data_path, self.censored_star_item_info_file_name)
        self.uncensored_path = os.path.join(iteminfo_data_path, self.uncensored_star_item_info_file_name)
        if os.path.exists(self.censored_path) and (self.process_item_data_str in self.censored_path) \
                and os.path.exists(self.uncensored_path) and (self.process_item_data_str in self.uncensored_path):
            self.today_has_download = True

    def process_item(self, item, spider):
        if not isinstance(item, JavbusStarItemInfoScrapyItem):
            return item
        # 处理
        # print(item.get_csv_str())
        if self.today_has_download:
            spider.log(f"当天下载文件已存在: {self.censored_path}|{self.uncensored_path}")
            return item

        is_censored = item['movie_censored']
        csv_str = item.get_csv_str()
        if is_censored:
            with open(self.censored_path, 'a+') as file:
                # print(f"csv_str:{csv_str}")
                file.write(csv_str)
        else:
            with open(self.uncensored_path, 'a+') as file:
                file.write(csv_str)


# 处理starinfo item
class JavbusScrapyStarInfoPipeline:
    # 日期字符串
    process_item_data_str = time.strftime("%Y-%m-%d", time.localtime())
    # 有码文件名
    censored_star_info_file_name = f"censored_starinfo_{process_item_data_str}.csv"
    # 无码文件名
    uncensored_star_info_file_name = f"uncensored_starinfo_{process_item_data_str}.csv"
    # 有码存储路径
    censored_path = None
    # 无码存储路径
    uncensored_path = None

    today_has_download = False

    @classmethod
    def from_crawler(cls, spider):
        return cls(spider)

    def __init__(self, spider) -> None:
        # 初始化存储目录
        store_path = spider.settings['DATA_STORE'].strip()
        iteminfo_data_path = os.path.join(store_path, utils.STARINFO_PATH_NAME)
        if not os.path.exists(iteminfo_data_path):
            os.makedirs(iteminfo_data_path)
        # 判断文件是否下载过
        self.censored_path = os.path.join(iteminfo_data_path, self.censored_star_info_file_name)
        self.uncensored_path = os.path.join(iteminfo_data_path, self.uncensored_star_info_file_name)
        if os.path.exists(self.censored_path) and (self.process_item_data_str in self.censored_path) \
                and os.path.exists(self.uncensored_path) and (self.process_item_data_str in self.uncensored_path):
            self.today_has_download = True

    def process_item(self, item, spider):
        if not isinstance(item, JavbusStarInfoScrapyItem):
            return item
        if self.today_has_download:
            spider.log(f"当天下载文件已存在: {self.censored_path}|{self.uncensored_path}")
            return item
        # 处理
        is_censored = item['censored_star']
        csv_str = item.get_csv_str()
        if is_censored:
            with open(self.censored_path, 'a+') as file:
                # print(f"csv_str:{csv_str}")
                file.write(csv_str)
        else:
            with open(self.uncensored_path, 'a+') as file:
                file.write(csv_str)
