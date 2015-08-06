__author__ = 'colen'
# -*- coding: utf-8 -*-

import lxml.html
import lxml.etree
from tuto.parsers.pagingtagparser import *

#页面信息获取, 根据key, 得到items 以及兄弟页urls elements
class ModelParser():

  def __init__(self):
    self.doc = None
    self.items = []

  def parse(self,eles,sitekey):
    keyword = "微信号".decode("utf-8")
    tagname = "div"
    for e in eles:
      #1.找最底层节点:
      a = ("./descendant::*[contains(text(),'"+keyword+"')]")
      es = e.xpath(a)
      text = ""
      if (len(es)>0):
        e1 = es[0]
        e1.text = e1.text.strip()
        if (len(e1.text)>len(keyword)+2):
          text = e1.text[e1.text.find(keyword)+len(keyword):len(e1.text)]
          text = text.strip("：".decode(("utf-8")))
      if (len(text)<4):     #无效text
        return True
    return False


  def parse_sogou(self):
    return

#页面信息获取, 根据key, 得到items 以及兄弟页urls elements
class ItemsFounder():

  def __init__(self):
    self.doc = None
    self.items = []
    self.pagingparser = PagingTagParser()
    self.modelparser = ModelParser()

  def find(self,htmlStr,base_url,keys,sitekey):
    if (len(keys)<2):
      print "没有提供keys,无法查找"
      return False,False

    self.doc = lxml.html.fromstring(htmlStr, base_url)
    itemskeys = keys[0]
    found1 = False
    if (len(itemskeys)>0):
      eles = self.doc.xpath("//"+itemskeys[0])
      if (len(eles)>5):
        self.items = self.modelparser.parse(eles,sitekey)
        found1 = True
    foundurls = self.pagingparser.findUrls(self.doc,base_url,keys[1])
    if (foundurls):
      self.pagingurls = self.pagingparser.urls
      print "itemsfounder找到分页链接:",len(self.pagingurls)
    return found1,foundurls