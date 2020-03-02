from __future__ import absolute_import

import sys

import scrapy

from items import CrawlerJijinItem

reload(sys)
sys.setdefaultencoding('utf-8')


class Crawler_jijin_spider(scrapy.Spider):
    name = "crawler_jijin"
    allowed_domains = ["http://gall.dcinside.com/"]
    start_urls = ["http://gall.dcinside.com/board/lists/?id=earthquake"]

    #def start_requests(self):
        #for i in range(0,21):
            #yield scrapy.Request("http://gall.dcinside.com/board/lists/?id=jijinhee&page=%d" % i, self.parsecro)

    def parse(self, response):
        for sel in response.xpath('//*[@id="dgn_gallery_left"]/div[3]/div[1]/table/tbody/tr'):
            item = CrawlerJijinItem()
            item['no'] = sel.xpath('//*[@id="dgn_gallery_left"]/div[3]/div[1]/table/tbody/tr/td[1]/text()').extract()
            item['title'] = sel.xpath("//*[@id='dgn_gallery_left']/div[3]/div[1]/table/tbody/tr/td[2]/a/text()|"
                                      "//*[@id='dgn_gallery_left']/div[3]/div[1]/table/tbody/tr/td[2]/a/b/text()").extract()
            item['link'] = sel.xpath('//*[@id="dgn_gallery_left"]/div[3]/div[1]/table/tbody/tr/td[2]/'
                                     'a[@class="icon_txt_n" or @class="icon_pic_n" or @class="icon_notice" or @class="icon_pic_b" or @class="icon_txt_b"]/@href').extract()
            item['writer'] = sel.xpath("//*[@id='dgn_gallery_left']/div[3]/div[1]/table/tbody/tr/td[3]/span/text()|"
                                       "//*[@id='dgn_gallery_left']/div[3]/div[1]/table/tbody/tr/td[3]/b/b/text()").extract()
            item['date'] = sel.xpath('//*[@id="dgn_gallery_left"]/div[3]/div[1]/table/tbody/tr/td[4]/@title').extract()
        yield item