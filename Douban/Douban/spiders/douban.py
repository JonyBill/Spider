# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from Douban.items import DoubanItem


class DoubanSpider(CrawlSpider):
    name = 'douban'
    allowed_domains = ['douban.com']
    start_urls = ['https://movie.douban.com/top250']

    rules = (
        Rule(LinkExtractor(allow=r'start=\d+&filter='), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        node_list = response.xpath('//div[@class="info"]')
        # print(len(node_list))

        for node in node_list:
            item = DoubanItem()

            item['name'] = node.xpath('./div[1]/a/span[1]/text()').extract_first()
            item['score'] = node.xpath('./div[2]/div/span[2]/text()').extract_first()
            item['info'] = ''.join([data.strip() for data in node.xpath('./div[2]/p[1]/text()').extract()])
            item['desc'] = node.xpath('./div[2]/p[2]/span/text()').extract_first()

            yield item
