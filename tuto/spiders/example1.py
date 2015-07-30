# -*- coding: utf-8 -*-
import scrapy


class Example1Spider(scrapy.Spider):
    name = "example1"
    allowed_domains = ["baidu.com"]
    start_urls = (
        'http://www.baidu.com/',
    )

    def parse(self, response):
        filename = response.url.split("/")[-2]
        open(filename, 'wb').write(response.body)
