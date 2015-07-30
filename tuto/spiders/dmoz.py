__author__ = 'colen'

from scrapy.spider import Spider
from scrapy.selector import Selector
from tuto.items import DmozItem
from scrapy.http import Request
from bs4 import BeautifulSoup as bs
import scrapy

class DmozSpider(Spider):
    name = "dmoz"
    allowed_domains = ["dmoz.org"]
    start_urls = [
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Books/"]

    def parse(self, response):
        filename = response.url.split("/")[-2]
        open(filename, 'wb').write(response.body)
        sel = Selector(response)
        # soup = bs(response.body)
        # items = [(x[0].text, x[0].get('href')) for x in
        #              filter(None, [
        #                  x.findChildren() for x in
        #                  soup.findAll('ul', {'class': 'directory-url'})
        #              ])]
        # for item in items:
        #     print item[1]
        #     item = DmozItem()
        #     item['title'] = item[0]
        #     item['link'] = item[1]
        #     try:
        #         yield scrapy.Request(item[1], callback=self.parse)
        #     except ValueError:
        #             yield scrapy.Request( item[1], callback=self.parse)
        #     yield item
        sites = sel.xpath('//ul[@class="directory-url"]/li')
        items = []
        for site in sites:
            item = DmozItem()
            item['title'] = site.xpath('a/text()').extract()
            item['link'] = site.xpath('a/@href').extract()
            item['desc'] = site.xpath('text()').extract()
            items.append(item)
            print item['link']
            try:
                yield Request(item['link'], callback=self.parse)
            except ValueError:
                yield Request(item['link'], callback=self.parse)
            yield item
        # return items