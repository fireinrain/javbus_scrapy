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

### 配置说明

```python3
# settings.py
# # 配置数据的保存目录
DATA_STORE = './data_store'
# 只爬取censored censored uncensored all
# 修改该值可以选择只爬取有码 或者无码 或者两者全部
CENSORED = 'censored'

# 文件及路径，log目录需要先建好
today = datetime.now()
setting_dir = os.path.dirname(__file__)
log_dir = os.path.dirname(setting_dir)
log_dir = os.path.join(log_dir, "logs")

# 日志输出
LOG_LEVEL = 'DEBUG'
# 开启log file 日志输出就不回输出到控制台了
# LOG_FILE = log_dir + "/" + "scrapy_{}_{}_{}.log".format(today.year, today.month, today.day)



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

### 数据增量更新

目前并没有实现数据增量更新的功能，初步的想法是，现将csv的数据 在数据库中建表 导入到数据库，然后以该日期的数据为一个节点，编写一个更新程序

每天定时爬取首页的前3页 抽取数据 加入到 stariteminfo 表中，插入前先查询一下表中数据是否存在如果不存在 就插入 存在就跳过。

插入时 先获取该star 在 数据库中查询时候是新人star 如果是 同时 获取starinfo 信息插入数据库，然后同步更新 stariteminfo 表 moviedetail表 和 torrentdetail表

