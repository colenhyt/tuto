# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field

class TutoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class DmozItem(Item):
    title = Field()
    link = Field()
    desc = Field()

class HnItem(Item):
    title = Field()
    link = Field()

class PublicItem(Item):
    hao = Field()
    name = Field()
    openid = Field()
    desc = Field()
    auth = Field()
    lastupdate = Field()
