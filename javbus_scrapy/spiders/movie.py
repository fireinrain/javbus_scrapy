import scrapy


class MovieSpider(scrapy.Spider):
    name = 'movie'
    allowed_domains = ['javbus.com']
    start_urls = ['http://javbus.com/']

    def parse(self, response):
        pass
