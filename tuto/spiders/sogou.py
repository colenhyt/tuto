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
        urls = self.datamgr.geturls(sitekey=self.sitekey)
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
          self.template = [temp_id,self.keysparser.itemskeys,self.keysparser.pagingkeys]
          purls = self.datamgr.inserturls(self.keysparser.pagingurls,temp_id)
          nextsiteurls.extend(purls)
      else:
        self.template = [stemplate[0],eval(stemplate[2]),eval(stemplate[3])]
        keys = [self.template[1],self.template[2]]
        found1,found2 = self.itemsfounder.find(response.body,baseurl,keys,self.sitekey)
        if (found2):
          purls = self.datamgr.inserturls(self.itemsfounder.pagingurls,self.template[0])
          nextsiteurls.extend(purls)

      self.datamgr.updateurl(baseurl,temp_id=self.temp_id)
      itemurls = []
      for url in nextsiteurls:
        print url
        itemurls.append(Request(url,callback=self.parse_siteurl))
      return itemurls

    def parse_siteurl(self, response):
      baseurl = response.url
      self.datamgr.updateurl(baseurl,temp_id=self.template[0])
      keys = [self.template[1],self.template[2]]
      found1,found2 = self.itemsfounder.find(response.body,baseurl,keys,self.sitekey)
      items = []
      # if (found1):

      return items