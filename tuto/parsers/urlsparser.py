__author__ = 'colen'
# -*- coding: utf-8 -*-

import lxml.html
import lxml.etree
from tuto.util.utils import *

def _findUrlText(element):
  text = ""
  if (element.text!=None and len(element.text.strip())>0):
    text = element.text.strip()
  else:
    #找img:
    ae = element.xpath("./img")
    if (len(ae)>0):
      atts = ae[0].xpath("./attribute::*")
      for attri in atts:
        if (_isImgUrl(attri)==True):
          text = attri
          break
    else:   #子元素文本
      texts = element.xpath("./descendant-or-self::*/text()")
      for t in texts:
        text += t.strip()

  return text

#页面信息获取, 根据key, 得到items 以及兄弟页urls elements
class UrlsParser():

  def __init__(self):
    self.doc = None
    self.items = []
    self.minWordSize= 4

#根据关键词找urls
  def parse(self,htmlStr,base_url,keys=[],ignorekeys=[],catkeys=[]):
    self.doc = lxml.html.fromstring(htmlStr, base_url)
    path = "./descendant::a"
    links = []
    eles = []
    if (len(keys)<=0):
      print "没有提供keys,查找全部urls"
      eles = self.doc.xpath(path)
    else:
      for k in keys:
        eles1 = self.doc.xpath(path+"[contains(@href,'"+k+"')]")
        eles.extend(eles1)

    for le in eles:
        hrefAtt = le.xpath("./attribute::href")
        if (len(hrefAtt)>0):
          url = hrefAtt[0]
          ig = _filterIgnore(url,ignorekeys)
          if (ig==True):continue
          link = []
          link.append(hrefAtt[0])
          text = _findUrlText(le)
          if (len(text)<=0):
            print "no text",base_url,url
          link.append(text)
          catid = -1
          for index in range(len(catkeys)):
            if (url.find(catkeys[index])>0):
              catid =index
              break
          link.append(catid)
          links.append(link)
    return links

def test2():
  page = UrlsParser()
  f = open('../../file/jd.html')
  ht_string = f.read()
  keywords = ["http://channel.","http://list.","http://item."]
  links = page.parse(ht_string,"http://www.jd.com",keys=keywords,catkeys=keywords)
  print sorted(links, key=lambda d: d[2])


# test2()