__author__ = 'colen'

from scrapy.spider import Spider
from scrapy.selector import Selector
from tuto.items import DmozItem
from scrapy.http import Request
from bs4 import BeautifulSoup as bs
import scrapy

class DmozSpider(Spider):
    name = "dmoz"
    # allowed_domains = ["dmoz.org"]
    start_urls = [
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Books/"]

    def parse(self, response):
        filename = response.url.split("/")[-2]
        open(filename, 'wb').write(response.body)
        sel = Selector(response)
        soup = bs(response.body)
        itemsurls = []
        sites = sel.xpath('//ul[@class="directory-url"]/li')
        items = []
        for site in sites:
            item = DmozItem()
            item['title'] = site.xpath('a/text()').extract()
            item['link'] = site.xpath('a/@href').extract()
            item['desc'] = site.xpath('text()').extract()
            items.append(item)
            # print item['link']
            item['link'] = "http://www.pearsonhighered.com/educator/academic/product/0,,0130260363,00%2Ben-USS_01DBC.html"
            # qq = self.make_requests_from_url(item['link'])
            # qq.replace(callback=self.parse_post)
            # qq = Request(url=item['link'],callback=self.parse_post)
            # itemsurls.append(qq)
        return items

    def parse_post(self, response):
        # filename = response.url.split("/")[-2]
        print 'afaaaaaaaaaaaaaaaa'
        items = []
        item = DmozItem()
        item['title'] = 'abc'
        items.append(item)
        item = DmozItem()
        item['title'] = 'aaaeee'
        items.append(item)
        return items