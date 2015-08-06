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
    found = self.a1_parseByKeys()
    if (found==False):
      #2: find with related url:
      found = self.a2_parseWithBaseUrl(base_url)

    if (found==True):
      urls = []
      for urle in  self.pagingurles:
        url = urle.get('href')
        if (url.find("http")==-1):
          if (urle.base_url.find("?")>0):
            base_url = urle.base_url[0:urle.base_url.find("?")]
          else:
            base_url = urle.base_url
          url = base_url+url
        urls.append(url)
      self.urls = urls

    return found

  def findUrls(self,htmlDoc,base_url,keys):
    self.doc = htmlDoc
    findtype = keys[0]
    targettags = []
    if (findtype==PAGINGTYPE_KEYS):
      eles = self.__finditems(keys[1],keys[2])
      if (len(eles)>0):
        ae = eles[0].xpath("a")
        if (len(ae)>=self.pagingMinCount):
          self.pagingurles = ae
    else:
      self.a2_parseWithBaseUrl(keys[1])

    urls = []
    for urle in  self.pagingurles:
      url = urle.get('href')
      if (url.find("http")==-1):
        if (urle.base_url.find("?")>0):
          base_url = urle.base_url[0:urle.base_url.find("?")]
        else:
          base_url = urle.base_url
        url = base_url+url
      urls.append(url)
    self.urls = urls
    return len(self.urls)>0

  def a1_parseByKeys(self):
    found = False
    foundtags,keytag,keyword=self._parseKeytags();
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

  def _parseKeytags(self):
    words = ['下一页','上一页']
    tagnames = ['div','p']
    keyword = ""
    keytag = ""
    targetags = []
    for k in words:
      for tag in tagnames:
        eles = self.__finditems(tag,k)
        if (len(eles)>0):
          targetags.append(eles[0])
          keyword = k
          keytag = tag
    return targetags,keytag,keyword

  def __finditems(self,tagname,keyword):
    a = ("//*[contains(text(),'"+keyword+"')]/parent::"+tagname).decode("utf-8")
    eles = self.doc.xpath(a)
    return eles

#url相似度分析:
  def a2_parseWithBaseUrl(self,relate_url):
    #完全重合:
    aes = self.doc.xpath("//a[contains(@href,'"+relate_url+"')]")
    if (len(aes)>=self.pagingMinCount):
      self.pagingurles = aes
      self.pagingKeys = [PAGINGTYPE_SAMEURL,relate_url]
      return True
    return False

  #根据提示自行构造兄弟链接
  def a3_createUrls(self):
    path = ("//div[contains(text(),'找到约')]").decode("utf-8")
    es = self.doc.xpath(path)
    print es