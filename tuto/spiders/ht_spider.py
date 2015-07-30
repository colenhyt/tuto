__author__ = 'colen'

from bs4 import BeautifulSoup as bs
from scrapy.http import Request
from scrapy.spider import BaseSpider
from tuto.items import HnItem

class HnSpider(BaseSpider):
    name = 'hn'
    allowed_domains = ["dmoz.org"]
    start_urls = ['http://www.dmoz.org/Computers/Programming/Languages/Python/Books/']

    def parse(self, response):
        if 'www.dmoz.org' in response.url:
            # filename = response.url.split("/")[-2]
            # open(filename, 'wb').write(response.body)
            soup = bs(response.body)
            items = [(x[0].text, x[0].get('href')) for x in
                     filter(None, [
                         x.findChildren() for x in
                         soup.findAll('li')
                     ])]

            for item in items:
                print item
                hn_item = HnItem()
                hn_item['title'] = item[0]
                hn_item['link'] = item[1]
                try:
                    yield Request('http://www.dmoz.org'+item[1], callback=self.parse)
                except ValueError:
                    yield Request('http://www.dmoz.org/' + item[1], callback=self.parse)

                yield hn_item
