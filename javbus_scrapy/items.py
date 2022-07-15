# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy


class JavbusScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


# actresses 页面
# 'item_scraped_count': 58948
# https://www.javbus.com/actresses
class JavbusActressScrapyItem(scrapy.Item):
    # 名字
    name = scrapy.Field()
    # 个人主页地址
    star_page_url = scrapy.Field()
    # 最新的一部作品url
    latest_movie_url = scrapy.Field()
    # 最新作品简介
    latest_movie_intro = scrapy.Field()
    # 大头贴地址
    head_photo_url = scrapy.Field()
    # censored or uncensored
    # 有码 还是无码
    censored = scrapy.Field()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 名字
        self['name'] = ""
        # 个人主页地址
        self['star_page_url'] = ""
        # 最新的一部作品url
        self['latest_movie_url'] = ""
        # 最新作品简介
        self['latest_movie_intro'] = ""
        # 大头贴地址
        self['head_photo_url'] = ""
        # censored or uncensored
        # 有码 还是无码
        self['censored'] = ""

    def get_csv_str(self):
        return f"{self['name']}|{self['star_page_url']}|{self['latest_movie_url']}|" \
               f"{self['head_photo_url']}|{self['latest_movie_intro']}|{self['censored']}\n"


# 个人主页 作品缩略项
# https://www.javbus.com/star/okq
class JavbusStarItemInfoScrapyItem(scrapy.Item):
    # 名字
    star_name = scrapy.Field()
    # 作品url
    movie_url = scrapy.Field()
    # 作品封面图片地址
    movie_cover_url = scrapy.Field()
    # 作品名
    movie_title = scrapy.Field()
    # 是否是有码作品 默认是True 有码
    movie_censored = scrapy.Field()
    # 是否有磁力链接 默认为False
    movie_has_magnet = scrapy.Field()
    # 作品清晰度  默认为""
    movie_resolutions = scrapy.Field()
    # 作品是否有字幕下载的磁力 默认为False
    movie_has_subtitle = scrapy.Field()
    # 作品字幕标识 默认为""
    movie_subtitle_flag = scrapy.Field()
    # 作品番号
    movie_code = scrapy.Field()
    # 作品发行日期
    movie_publish_date = scrapy.Field()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self['movie_has_magnet'] = False
        self['movie_resolutions'] = ''
        self['movie_has_subtitle'] = False
        self['movie_subtitle_flag'] = ''
        self['movie_censored'] = True

    def get_csv_str(self):
        return f"{self['star_name']}|{self['movie_url']}|{self['movie_cover_url']}|" \
               f"{self['movie_title']}|{self['movie_has_magnet']}|{self['movie_resolutions']}|" \
               f"{self['movie_has_subtitle']}|{self['movie_subtitle_flag']}|{self['movie_code']}|" \
               f"{self['movie_publish_date']}\n"


# 演员个人信息
class JavbusStarInfoScrapyItem(scrapy.Item):
    # 演员名
    star_name = scrapy.Field()
    # 大头贴url
    star_head_photo_url = scrapy.Field()
    # 所有作品数量
    all_item_counts = scrapy.Field()
    # 磁力作品数量
    magnet_item_counts = scrapy.Field()
    # 有码演员
    censored_star = scrapy.Field()
    # 生日
    birthday = scrapy.Field()
    # 年龄
    age = scrapy.Field()
    # 身高
    height = scrapy.Field()
    # 罩杯
    cup = scrapy.Field()
    # 胸围
    chest_circumference = scrapy.Field()
    # 腰围
    waistline = scrapy.Field()
    # 臀围
    hip_circumference = scrapy.Field()
    # 出生地
    birthplace = scrapy.Field()
    # 爱好
    habbits = scrapy.Field()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 演员名
        self['star_name'] = ""
        # 大头贴url
        self['star_head_photo_url'] = ""
        # 所有作品数量
        self['all_item_counts'] = ""
        # 磁力作品数量
        self['magnet_item_counts'] = ""
        # 有码演员
        self['censored_star'] = ""
        # 生日
        self['birthday'] = ""
        # 年龄
        self['age'] = ""
        # 身高
        self['height'] = ""
        # 罩杯
        self['cup'] = ""
        # 胸围
        self['chest_circumference'] = ""
        # 腰围
        self['waistline'] = ""
        # 臀围
        self['hip_circumference'] = ""
        # 出生地
        self['birthplace'] = ""
        # 爱好
        self['habbits'] = ""

    def get_csv_str(self):
        return f"{self['star_name']}|{self['star_head_photo_url']}|{self['all_item_counts']}|" \
               f"{self['magnet_item_counts']}|{self['censored_star']}|{self['birthday']}|" \
               f"{self['age']}|{self['height']}|{self['cup']}|" \
               f"{self['chest_circumference']}|{self['waistline']}|{self['hip_circumference']}|" \
               f"{self['birthplace']}|{self['habbits']}\n"


# 作品详情
class JavbusMovieDetailItem(scrapy.Item):
    # 作品名
    movie_title = scrapy.Field()
    # 是否为有码作品
    movie_censored = scrapy.Field()
    # 作品链接
    movie_url = scrapy.Field()
    # 封面缩略图
    movie_cover_url = scrapy.Field()
    # 番号
    movie_code = scrapy.Field()
    # 发行日期
    movie_publish_date = scrapy.Field()
    # 作品时长
    movie_duration = scrapy.Field()
    # 导演
    movie_directors = scrapy.Field()
    # 制作商
    movie_maker = scrapy.Field()
    # 发行商
    movie_publisher = scrapy.Field()
    # 系列
    movie_series = scrapy.Field()
    # 类别
    movie_tags = scrapy.Field()
    # 演员列表
    movie_stars = scrapy.Field()
    # 样品图链接
    movie_sample_photo_urls = scrapy.Field()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self['movie_title'] = ""
        # 是否为有码作品
        self['movie_censored'] = ""
        # 作品链接
        self['movie_url'] = ""
        # 封面缩略图
        self['movie_cover_url'] = ""
        # 番号
        self['movie_code'] = ""
        # 发行日期
        self['movie_publish_date'] = ""
        # 作品时长
        self['movie_duration'] = ""
        # 导演
        self['movie_directors'] = ""
        # 制作商
        self['movie_maker'] = ""
        # 发行商
        self['movie_publisher'] = ""
        # 系列
        self['movie_series'] = ""
        # 类别
        self['movie_tags'] = ""
        # 演员列表
        self['movie_stars'] = ""
        # 样品图链接
        self['movie_sample_photo_urls'] = ""

    def get_csv_str(self):
        return f"{self['movie_title']}|{self['movie_censored']}|{self['movie_url']}|{self['movie_cover_url']}|" \
               f"{self['movie_code']}|{self['movie_publish_date']}|{self['movie_duration']}|" \
               f"{self['movie_directors']}|{self['movie_maker']}|{self['movie_publisher']}|" \
               f"{self['movie_series']}|{self['movie_tags']}|{self['movie_stars']}|" \
               f"{self['movie_sample_photo_urls']}\n"


# 磁力链接
class JavbusMovieDetailTorrentItem(scrapy.Item):
    # 番号
    movie_code = scrapy.Field()
    # 是否为有码作品
    movie_censored = scrapy.Field()
    # 作品链接
    movie_url = scrapy.Field()

    torrent_list_str = scrapy.Field()

    # 磁力名称
    # torrent_name = scrapy.Field()
    # # 高清标识
    # torrent_resolution = scrapy.Field()
    # # 字幕标识
    # torrent_subtitle = scrapy.Field()
    # # 档案大小
    # torrent_movie_size = scrapy.Field()
    # # 分享日期
    # torrent_share_date = scrapy.Field()
    # # 磁力地址
    # torrent_str = scrapy.Field()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 番号
        self['movie_code'] = ""
        # 是否为有码作品
        self['movie_censored'] = ""
        # 作品链接
        self['movie_url'] = ""

        self['torrent_list_str'] = ""
        # 磁力名称
        # self['torrent_name'] = ""
        # # 高清标识
        # self['torrent_resolution'] = ""
        # # 字幕标识
        # self['torrent_subtitle'] = ""
        # # 档案大小
        # self['torrent_movie_size'] = ""
        # # 分享日期
        # self['torrent_share_date'] = ""
        # # 磁力地址
        # self['torrent_str'] = ""

    def get_csv_str(self):
        return f"{self['movie_code']}|{self['movie_censored']}|{self['movie_url']}|{self['torrent_list_str']}\n"
