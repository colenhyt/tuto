# -*- coding: utf-8 -*-
__author__ = 'colen'

from lxml.html import fromstring
from lxml import etree
from io import StringIO, BytesIO

import lxml.html
import lxml.etree
from tuto.util.utils import *
from tuto.data.datamgr import *
from tuto.parsers.pagingtagparser import *

#parser得到itemskey,以及兄弟页key
class PageKeysParser():
    def __init__(self,itemCount=5,itemSame=1):
        self.type=0
        self.itemskeys = []
        self.pagingkeys = []
        self.pagingurls = []
        self.eleMaps={}
        self.itemMinCount = itemCount     #item数量阀值
        self.itemSame = itemSame        #item相似度阀值

    def parse(self,htmlStr,base_url):
        self.doc = lxml.html.fromstring(htmlStr, base_url)
        pagingparser = PagingTagParser()
        found = pagingparser.parse(self.doc,base_url)
        if (found):
          self.pagingkeys = pagingparser.pagingKeys
          self.pagingurls = pagingparser.urls
          print '找到当前页分页链接:'+str(len(self.pagingurls))

        tagNames = ["div","li","p"]
        itemkeys_pre = []
        for tagname in tagNames:
            itemkeys_pre = self.parse_itemskeys(tagname)
            if (len(itemkeys_pre)>0):break
        self.itemskeys = itemkeys_pre
        if (len(self.itemskeys)>0):
          print "找到itemkeys:",itemkeys_pre
        return True

    def getitemes(self):
      if (len(self.itemskeys)>0):
        return self.eleMaps[self.itemskeys[0]]

    def parse_itemskeys(self,tagName):
        tagkeys = self._findTags(tagName)
        chooseKeys = []
        if (len(tagkeys)==1):
            chooseKeys = tagkeys
        elif (len(tagkeys)>1):            #多个,仲裁取哪个:
            chooseKeys = self._judgeMultikeys(tagkeys)
            if (len(chooseKeys)<=0):
                chooseKeys = tagkeys
        return chooseKeys

    def _judgeMultikeys(self,tagkeys):
        countkeys = {}
        for k in tagkeys:
            count = k[1]
            if (countkeys.has_key(count)==False):
                countkeys[count]=[]
            countkeys[count].append(k[0])
        subcountkeyMap = {}
        relatekeys = []
        #判断一个tag是否为另一个的子节点:
        for k in countkeys:
            keys = countkeys[k]
            for key in keys:
                item = self.eleMaps[key][0]
                childcount = len(item.xpath("*"))
                subcountkeyMap[key] = childcount
                for key2 in keys:
                    childs = item.xpath("./..//"+key2)
                    if (len(childs)>1):         #不包含自己
                        relatekeys.append(key)
                        break
        if (len(relatekeys)<=0):                  #相互无关,根据子节点数量排序
            subkeymap2 = sort_by_value(subcountkeyMap)
            for k in subkeymap2:
                relatekeys.append(k[1])

        finalkeys = []
        if (len(relatekeys)>1):          #还是有多个,有链接优先
            for k in relatekeys:
                item = self.eleMaps[k][0]
                urlcount = len(item.xpath("./../a"))
                if (urlcount>0):
                    finalkeys.append(k)
        if (len(finalkeys)<=0):
            finalkeys = relatekeys
        return finalkeys

    def _findTags(self,tagname,hasUrl=False):
        elms = self.doc.xpath("//"+tagname)
        tagelems = {}
        for ele in elms:
            items = ele.items()
            allkey = ele.tag+"["
            inilen = len(allkey)
            for v in items:
                if (v[0]!='class'):continue
                if (len(allkey)>inilen):
                    allkey += " and "
                allkey += "@"+v[0]+"='"+v[1]+"'"
            allkey += "]"
            if (len(allkey)>50): continue           #属性名过长, 判断为无效invalid tag
            # print allkey,len(ele.xpath("*"))
            if (hasUrl==True):
                urles = ele.xpath("./../a")
                if (len(urles)<=0):continue
            tag = []
            if (tagelems.has_key(allkey)==True):
                tag = tagelems[allkey]
            tag.append(ele)
            tagelems[allkey] =tag
        #判断节点是否为相似节点:
        sameelems = {}
        for k in tagelems:
            if (len(tagelems[k])<self.itemMinCount):continue
            issame = tagSameScore(tagelems[k][0],tagelems[k][1])
            if (issame>=self.itemSame):
                sameelems[k]=tagelems[k]
        sortkeys = sort_by_valuelen(sameelems)
        self.eleMaps = sameelems
        return sortkeys

    def isCat(self):
        return 0

    def judgeCat(self,base_url):
        # div,li等内容块判断:找出数量大于某个阀值(5)内容块,
        ht_doc = lxml.html.fromstring(self.content, base_url)
        elms = ht_doc.xpath("//div")
        return 11

    def isItem(self):
        return 1

def test():
  f = open('../../file/sougou.html')
  # read all file content
  ht_string = f.read()
  page = PageKeysParser()
  page.parse(ht_string)
  datamgr = DataMgr()
  datamgr.insertSiteTemplate('sogou.com',page.itemskeys,page.pagingkeys)


# test()