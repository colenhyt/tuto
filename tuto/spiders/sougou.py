# -*- coding: utf-8 -*-
__author__ = 'colen'

from scrapy.spider import Spider
from scrapy.selector import Selector
from tuto.items import DmozItem
from scrapy.http import Request
from bs4 import BeautifulSoup as bs
import scrapy

class SougouSpider(Spider):
    name = "sougou"
    # allowed_domains = ["sogou.com"]

    def __init__(self, category=None, *args, **kwargs):
        self.start_urls = []
        words=['育儿','早教']
        for word in words:
            url = "http://weixin.sogou.com/weixin?query="+word
            self.start_urls.append(url)
            print url

    def parse(self, response):
        # filename = response.url.split("/")[-2]
        # open(filename, 'wb').write(response.body)
        sel = Selector(response)
        soup = bs(response.body)
        itemsurls = []
        sites = sel.xpath('//ul[@class="directory-url"]/li')
        items = []
        for site in sites:
            item = DmozItem()
            item['title'] = site.xpath('a/text()').extract()
            item['link'] = site.xpath('a/@href').extract()
            item['desc'] = site.xpath('text()').extract()
            items.append(item)
        return items

    def parse_post(self, response):
        items = []
        item = DmozItem()
        item['title'] = 'abc'
        items.append(item)
        item = DmozItem()
        item['title'] = 'aaaeee'
        items.append(item)
        return items