# javbus_scrapy

scrapy for fetch javbus.com data
scrapy spider for fetch javbus.com data

### 如何使用

1. git clone 当前项目
2. 在项目目录 执行 pip3 install -r requirements.txt
3. 切换工作目录到main.py 坐在的目录
4. 执行 python3 main.py
5. 输入对于的选项 来选择所需要进行的爬虫

### 注意

因为是需要访问被GFW屏蔽的网站，所以需要在项目的middlewares.py 文件中指定代理 具体如下,
端口使用自己本地的代理端口

```python3
def process_request(self, request, spider):
    # Called for each request that goes through the downloader
    # middleware.

    # Must either:
    # - return None: continue processing this request
    # - or return a Response object
    # - or return a Request object
    # - or raise IgnoreRequest: process_exception() methods of
    #   installed downloader middleware will be called
    # set a proxy for request data
    proxy_url = "http://127.0.0.1:7892"
    request.meta["proxy"] = proxy_url
    spider.logger.info(f"正在使用本地代理: {proxy_url}")
    return None

```

### 数据说明

spider actresses:  爬取演员列表，并将有码和无码演员分类写入文本

actresses csv 数据格式：名字,个人主页地址,最新一部作品地址，最新作品简介,大头贴地址,有码还是无码

spider star_page 从演员的个人页面爬取,获得个人信息和所有个人作品信息

starinfo csv 数据格式: 演员名,大头贴url,所有作品数量,磁力作品数量,有码演员,生日,年龄,身高,罩杯,胸围,腰围,臀围,出生地,爱好

starinteminfo csv 数据格式: 演员名字,作品url,作品封面图片地址,作品名,是否是有码作品 默认是True 有码,是否有磁力链接 默认为False,作品清晰度 默认为"",作品是否有字幕下载的磁力
默认为False,作品字幕标识 默认为"",作品番号,作品发行日期

spider movie 爬取作品详情

moviedetail csv 数据格式：作品名,是否为有码作品,作品链接,封面缩略图,番号,发行日期,作品时长,导演,制作商,发行商,系列,类别,演员列表,样品图链接

torrentdetail csv 数据格式: 番号,是否为有码作品，作品链接，磁力字符串列表(格式:name/magnet_str/resolution/subtitle/file_size/share_date,多个磁力用|分隔)