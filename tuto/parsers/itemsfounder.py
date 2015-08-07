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
    self.minWordSize= 4


  def _filterText(self,text0,keyword=""):
    if (text0==None or len(text0)<=0):return ""
    text = text0.strip()
    if (len(keyword)>0):
      if (text.find(keyword)>=0):
        text = text[text.find(keyword)+len(keyword):len(text)]
      else:
        text = ""
    text = text.strip("：".decode(("utf-8")))
    return text

#根据关键词找节点文本，
 #文本不合法，找该节点child节点文本
  #文本不合法，找该节点右brother节点文本
  #还不合法，找该节点任意后代节点文本，并过滤tag
#找到的文本需要先过滤：等无意义符号
  def _findWordByElement(self,element,keyword=""):
    text = ""
    #1. 找自己及子节点文本:
    path = ("./descendant-or-self::*")
    if (len(keyword)>0):
      path += "[contains(text(),'"+keyword+"')]"
    texts = element.xpath(path+"/text()")
    if (len(texts)<=0):return False,""

    #1.1合并文本:
    for t in texts:
      text += t.strip()
    text = self._filterText(text,keyword=keyword)
    if (len(text)>=self.minWordSize):     #有效text
      return True,text

    #2. 找后续同级节点文本并合并
    relatetexts = element.xpath(path+"/following-sibling::*/text()")
    text0 = ""
    for t in relatetexts:
        text0 += t.strip()
    text = self._filterText(text0)
    if (len(text)>=self.minWordSize):     #有效text
      return True,text

    return False,text

#查找节点属性中某个关键字的value
  def _findAttrByElement(self,element,keyword):
    text = ""
    #1. 找自己及子节点属性:
    path = ("./descendant-or-self::*/attribute::*")
    # if (len(keyword)>0):
    #   path += "[contains(text(),'"+keyword+"')]"
    attrvalues = element.xpath(path)
    if (len(attrvalues)<=0):return False,""

    valueStr = ""
    for v in attrvalues:
      index = v.find(keyword)
      if (index>=0):
        valueStr = v[index+len(keyword)+1:len(v)]
        break

    if (len(valueStr)<=0):return False,""

    #根据&,等字符结束
    symbols = ["&"]
    for s in symbols:
      index = valueStr.find(s)
      if (index>0):
        valueStr = valueStr[0:index]
        break;

    return len(valueStr)>0,valueStr

#根据关键词找不到，递归相似关键词
#查找可能存在文本的标签有:div,span,p,h1,h2,h3,h4,table/tr/td
  def parse(self,eles,sitekey):
    keywords = ["微信号","功能介绍","认证","openid"]
    wordslist = []
    word1 = ""
    for e in eles:
      words = {}
      for key in keywords:
        keyword = key.decode("utf-8")
        found,word = self._findWordByElement(e,keyword)
        if (found):
          words[key]= word
        else:
          found,word = self._findAttrByElement(e,keyword)
          if (found):
            words[key]= word

      if (len(words)>0):
        wordslist.append(words)


    for words in wordslist:
      for k in words:
        print k,words[k]

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