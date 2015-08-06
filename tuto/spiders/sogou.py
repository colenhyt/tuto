# -*- coding: utf-8 -*-
from tuto.parsers.itemsfounder import ItemsFounder

__author__ = 'colen'

from scrapy.spider import Spider
from tuto.items import DmozItem
from tuto.data.datamgr import DataMgr
from scrapy.http import Request
import scrapy
from tuto.parsers.pagekeysparser import *

class SogouSpider(Spider):
    name = "sogou"
    allowed_domains = ["sogou.com"]

    def __init__(self, category=None, *args, **kwargs):
        self.sitekey = "sogou.com"
        self.temp_id = 0
        self.keysparser = PageKeysParser();
        self.itemsfounder = ItemsFounder();
        self.datamgr = DataMgr();
        self.start_urls = ["http://weixin.sogou.com"]

    def parse(self, response):
        print "连上:"+self.sitekey

        urlitems = []
        #1:爬内容页:
        urls = self.datamgr.geturls(self.sitekey)
        for uitem in urls:
          url = uitem[2]
          urlitems.append(Request(url,callback=self.parse_siteurl))

        surlcount = len(urlitems)
        print "装载siteurl数量:",surlcount

        #2: 爬搜索页
        words = self.datamgr.getwords(8)
        for word in words:
            url = "http://weixin.sogou.com/weixin?query="+word[1]
            urlitems.append(Request(url,callback=self.parse_rooturl))

        print "装载搜索页数量:",len(urlitems)-surlcount

        if (len(urlitems)==0):
          print "没有任何下载url可爬"

        return urlitems

    def parse_rooturl(self, response):
      baseurl = response.url
      stemplate = self.datamgr.getsitetemplates(self.sitekey)
      nextsiteurls = []
      if (stemplate==None):
        found = self.keysparser.parse(response.body,baseurl)
        if (found):
          temp_id = self.datamgr.insertSiteTemplate(self.sitekey,self.keysparser.itemskeys,self.keysparser.pagingkeys)
          self.temp_id = temp_id
          purls = self.datamgr.inserturls(self.keysparser.pagingurls,temp_id)
          nextsiteurls.extend(purls)
      else:
        self.temp_id = stemplate[0]
        keys = [eval(stemplate[2]),eval(stemplate[3])]
        found1,found2 = self.itemsfounder.find(response.body,baseurl,keys)
        if (found2):
          purls = self.datamgr.inserturls(self.itemsfounder.pagingurls,stemplate[0])
          nextsiteurls.extend(purls)

      self.datamgr.updateurl(baseurl,temp_id=self.temp_id)
      itemurls = []
      for url in nextsiteurls:
        print url
        itemurls.append(Request(url,callback=self.parse_siteurl))
      return itemurls

    def parse_siteurl(self, response):
      baseurl = response.url
      self.datamgr.updateurl(baseurl,temp_id=self.temp_id)
      items = []
      item = DmozItem()
      item['title'] = 'abc'
      items.append(item)
      item = DmozItem()
      item['title'] = 'aaaeee'
      items.append(item)
      return items