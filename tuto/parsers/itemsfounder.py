__author__ = 'colen'
# -*- coding: utf-8 -*-

import lxml.html
import lxml.etree
from tuto.parsers.pagingtagparser import *

#页面信息获取, 根据key, 得到items 以及兄弟页urls elements
class ItemsFounder():

  def __init__(self):
    self.doc = None
    self.pagingparser = PagingTagParser()

  def find(self,htmlStr,base_url,keys):
    if (len(keys)<2):
      print "没有提供keys,无法查找"
      return False,False

    self.doc = lxml.html.fromstring(htmlStr, base_url)
    itemskeys = keys[0]
    found1 = False
    if (len(itemskeys)>0):
      eles = self.doc.xpath("//"+itemskeys[0])
      if (len(eles)>5):
        found1 = True
    foundurls = self.pagingparser.findUrls(self.doc,base_url,keys[1])
    if (foundurls):
      self.pagingurls = self.pagingparser.urls
      print "itemsfounder找到分页链接:",len(self.pagingurls)
    return found1,foundurls