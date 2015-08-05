__author__ = 'colen'
# -*- coding: utf-8 -*-

from lxml.html import fromstring
from lxml import etree
from io import StringIO, BytesIO
import lxml.html
import lxml.etree
from tuto.util.utils import *

class PagingTagParser():
  def __init__(self):
    self.pagingurles = []
    self.pagingMinCount = 3

  def parse(self,htmlDoc,base_url):
    self.doc = htmlDoc
    self.base_url = base_url

    #1: find by keys:
    found = self.a1_findByKeys()
    if (found):
      return True

    #2: find with related url:
    found = self.a2_findWithBaseUrl()
    return found

  def a1_findByKeys(self):
    keytags=self._findKeytags();
    for k in keytags:
      ae = k.xpath("a")
      if (len(ae)>=self.pagingMinCount):
        self.pagingurles = ae
        return True
    return False

  def _findKeytags(self):
    words = ['下一页','上一页']
    tagnames = ['div','p']
    targetags = []
    for k in words:
      for tag in tagnames:
        a = ("//*[contains(text(),'"+k+"')]/parent::"+tag).decode("utf-8")
        eles = self.doc.xpath(a)
        if (len(eles)>0):
          targetags.append(eles[0])
    return targetags

#url相似度分析:
  def a2_findWithBaseUrl(self):
    #完全重合:
    aes = self.doc.xpath("//a[contains(@href,'"+self.base_url+"')]")
    if (len(aes)>=self.pagingMinCount):
      self.pagingurles = aes
      return True
    return False

  #根据提示自行构造兄弟链接
  def a3_createUrls(self):
    path = ("//div[contains(text(),'找到约')]").decode("utf-8")
    es = self.doc.xpath(path)
    print es