__author__ = 'colen'
# -*- coding: utf-8 -*-

from lxml.html import fromstring
from lxml import etree
from io import StringIO, BytesIO
import lxml.html
import lxml.etree
from tuto.util.utils import *

PAGINGTYPE_KEYS             = 1
PAGINGTYPE_SAMEURL      = 2

class PagingTagParser():
  def __init__(self):
    self.pagingurles = []
    self.urls = []
    self.pagingKeys = [];
    self.pagingMinCount = 3

  def parse(self,htmlDoc,base_url):
    self.doc = htmlDoc
    self.base_url = base_url

    #1: find by keys:
    found = self.a1_findByKeys()
    if (found==False):
      #2: find with related url:
      found = self.a2_findWithBaseUrl()

    if (found==True):
      urls = []
      for urle in  self.pagingurles:
        url = urle.xpath("//a/@href")
        urls.append(url[0])
      self.urls = urls

    return found

  def a1_findByKeys(self):
    found = False
    foundtags,keytag,keyword=self._findKeytags();
    for k in foundtags:
      ae = k.xpath("a")
      if (len(ae)>=self.pagingMinCount):
        self.pagingurles = ae
        self.pagingKeys = [PAGINGTYPE_KEYS,keytag,keyword]
        found = True
        break
    # a = ("//*[contains(text(),'"+keyword+"')]/parent::"+keytag).decode("utf-8")
    # es = self.doc.xpath(a)
    return found

  def _findKeytags(self):
    words = ['下一页','上一页']
    tagnames = ['div','p']
    keyword = ""
    keytag = ""
    targetags = []
    for k in words:
      for tag in tagnames:
        a = ("//*[contains(text(),'"+k+"')]/parent::"+tag).decode("utf-8")
        eles = self.doc.xpath(a)
        if (len(eles)>0):
          targetags.append(eles[0])
          keyword = k
          keytag = tag
    return targetags,keytag,keyword

#url相似度分析:
  def a2_findWithBaseUrl(self):
    #完全重合:
    aes = self.doc.xpath("//a[contains(@href,'"+self.base_url+"')]")
    if (len(aes)>=self.pagingMinCount):
      self.pagingurles = aes
      self.pagingKeys = [PAGINGTYPE_SAMEURL,self.base_url]
      return True
    return False

  #根据提示自行构造兄弟链接
  def a3_createUrls(self):
    path = ("//div[contains(text(),'找到约')]").decode("utf-8")
    es = self.doc.xpath(path)
    print es