import scrapy


# https://www.javbus.com/page/372
class IndexpageSpider(scrapy.Spider):
    name = 'indexpage'
    allowed_domains = ['javbus.com']
    start_urls = ['https://javbus.com/']

    def parse(self, response):
        pass
