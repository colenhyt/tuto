__author__ = 'colen'
# -*- coding: utf-8 -*-

import lxml.html
import lxml.etree

#页面信息获取, 根据key, 得到items 以及兄弟页urls elements
class ItemsFounder():

  def __init__(self):
    self.doc = None

  def find(self,htmlStr,base_url,keys):
    if (len(keys)<2):
      print "没有提供keys,无法查找"
      return False

    self.doc = lxml.html.fromstring(htmlStr, base_url)
    itemskeys = keys[0]
    pagingkeys = keys[1]
    eles = self.doc.xpath(itemskeys)
    if (len(eles)>5):
      return True
    return 0;