# -*- coding: utf-8 -*-
from tuto.parsers.itemsfounder import ItemsFounder

__author__ = 'colen'

from scrapy.spider import Spider
from tuto.items import DmozItem
from tuto.data.datamgr import DataMgr
from scrapy.http import Request
import scrapy
from tuto.parsers.pagekeysparser import *
from tuto.parsers.urlsparser import *
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule

class JdSpider(CrawlSpider):
    name = "jd"
    allowed_domains = ["jd.com"]
    start_urls = ['http://www.jd.com/']

    def __init__(self, category=None, *args, **kwargs):
        self.sitekey = "jd.com"
        self.temp_id = 0
        self.datamgr = DataMgr();
        self.start_urls = []
        urls = self.datamgr.geturls(urlkey=self.sitekey)
        links = []
        for uitem in urls:
          links.append(uitem[2])
        links = sorted(links, key=lambda d: d[2])
        self.start_urls.extend(links)

        if (len(self.start_urls)<=0):
         self.start_urls.append("http://www.jd.com")

        self.urlsparser = UrlsParser()
        self.urlkeys = ["http://channel.","http://list.","http://item."]
        self.ignorekeys = ["#comments-list","/adclick"]

    def parse(self, response):
        baseurl = response.url
        print "连上:"+baseurl
        self.datamgr.updateurl(baseurl,status=2)

        urlitems = []

        links = self.urlsparser.parse(response.body,baseurl,self.urlkeys,self.ignorekeys,catkeys=self.urlkeys)
        links = sorted(links, key=lambda d: d[2])
        urls = self.datamgr.inserturls(links,relate_url1=baseurl,status=1)
        siteitems = []
        for url in urls:
          if (url[0].find("http://item.")>=0):
            siteitems.append([url[0],url[1],baseurl])
          urlitems.append(Request(url[0],callback=self.parse))

        self.datamgr.insertitems(siteitems)

        return urlitems

    # def parse_urliteml(self, response):
    #   siteitem = []
    #   baseurl = response.url
    #   self.datamgr.updateurl(baseurl,temp_id=self.template[0])
    #
    #   return items