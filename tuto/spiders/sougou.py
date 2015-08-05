# -*- coding: utf-8 -*-
from tuto.parsers.itemsfounder import ItemsFounder

__author__ = 'colen'

from scrapy.spider import Spider
from scrapy.selector import Selector
from tuto.items import DmozItem
from tuto.data.datamgr import DataMgr
from scrapy.http import Request
from bs4 import BeautifulSoup as bs
import scrapy
from tuto.parsers.pagekeysparser import *

class SougouSpider(Spider):
    name = "sougou"
    allowed_domains = ["sogou.com"]

    def __init__(self, category=None, *args, **kwargs):
        self.sitekey = "sougou.com"
        self.keysparser = PageKeysParser();
        self.itemsfounder = ItemsFounder();
        self.datamgr = DataMgr();
        self.start_urls = []

        if (len(self.start_urls)==0):
          print "没有任何下载url可爬"

    def parse(self, response):
        print "连上:"+self.sitekey

        urls = []
        #1:爬内容页:
        urlitems = self.datamgr.geturls(self.sitekey)
        for uitem in urls:
          url = uitem[2]
          urlitems.append(Request(url,callback=self.parse_siteurl))

        surlcount = len(urlitems)
        print "装载siteurl数量:",surlcount

        #2: 爬搜索页
        words = DataMgr.getwords(8)
        for word in words:
            url = "http://weixin.sogou.com/weixin?query="+word[1]
            url = url.decode("utf-8")
            urlitems.append(Request(url,callback=self.parse_rooturl))

        print "装载搜索页数量:",len(urlitems)-surlcount

        return urlitems

    def parse_rooturl(self, response):
      stemplate = self.datamgr.getsitetemplates(self.sitekey)
      itemurls = []
      if (len(stemplate)<=0):
        found = self.keysparser.parse(response.body)
        if (found):
          self.datamgr.insertSiteTemplate(self.sitekey,self.keysparser.itemskeys,self.keysparser.pagingkeys)
          for url in self.keysparser.pagingurls:
            itemurls.append(Request(url,callback=self.parse_siteurl))
      else:

      return itemurls

    def parse_siteurl(self, response):
        items = []
        item = DmozItem()
        item['title'] = 'abc'
        items.append(item)
        item = DmozItem()
        item['title'] = 'aaaeee'
        items.append(item)
        return items