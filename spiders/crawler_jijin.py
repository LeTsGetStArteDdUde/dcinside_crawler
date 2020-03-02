from __future__ import absolute_import

import scrapy

from items import CrawlerJijinItem

class Crawler_jijin_spider(scrapy.Spider):
    name = "crawler_jijin"
    allowed_domains = ["http://gall.dcinside.com/"]
    start_urls = ["http://gall.dcinside.com/board/lists/?id=earthquake"]

    def start_requests(self):
        for i in range(0,1):
            yield scrapy.Request("http://gall.dcinside.com/board/lists/?id=jijinhee&page=%d" % i, self.parse)
    
    def parse(self, response):
        for sel in response.xpath('//*[@id="container"]/section[1]/article[2]/div[2]/table/tbody/tr'):
            item = CrawlerJijinItem()
            item['no'] = sel.xpath('//*[@id="container"]/section[1]/article[2]/div[2]/table/tbody/tr/td[1]/text()').extract()
            item['title'] = sel.xpath("//*[@id='container']/section[1]/article[2]/div[2]/table/tbody/tr/td[2]/a/text()|"
                                      "//*[@id='container']/section[1]/article[2]/div[2]/table/tbody/tr/td[2]/a/b/text()").extract()
            item['link'] = sel.xpath('//*[@id="container"]/section[1]/article[2]/div[2]/table/tbody/tr/td[2]/a[1]/@href').extract()
            item['writer'] = sel.xpath("//*[@id='container']/section[1]/article[2]/div[2]/table/tbody/tr/td[3]/span/text()|"
                                       "//*[@id='container']/section[1]/article[2]/div[2]/table/tbody/tr/td[3]/b/b/text()").extract()
            item['date'] = sel.xpath('//*[@id="container"]/section[1]/article[2]/div[2]/table/tbody/tr/td[4]/@title').extract()
        yield item