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
    # 大头贴地址
    head_photo_url = scrapy.Field()
    # censored or uncensored
    # 有码 还是无码
    censored = scrapy.Field()

    def get_csv_str(self):
        return f"{self['name']},{self['star_page_url']},{self['head_photo_url']},{self['censored']}\n"


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
        return f"{self['star_name']},{self['movie_url']},{self['movie_cover_url']},{self['movie_title']},{self['movie_has_magnet']},{self['movie_resolutions']},{self['movie_has_subtitle']},{self['movie_subtitle_flag']},{self['movie_code']},{self['movie_publish_date']}\n"


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

    def get_csv_str(self):
        return f"{self['star_name']},{self['star_head_photo_url']},{self['all_item_counts']},{self['magnet_item_counts']},{self['censored_star']},{self['birthday']},{self['age']},{self['height']},{self['cup']},{self['chest_circumference']},{self['waistline']},{self['hip_circumference']},{self['birthplace']},{self['habbits']}\n"


# 作品详情
class JavbusMovieDetailItem(scrapy.Item):
    pass
