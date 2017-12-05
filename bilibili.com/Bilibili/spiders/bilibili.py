# -*- coding: utf-8 -*-
import scrapy
from Bilibili.items import BilibiliItem


class BilibiliSpider(scrapy.Spider):
    name = 'bilibili'
    allowed_domains = ['http://bilibili.com/']
    base_url = 'https://bangumi.bilibili.com/anime/index#p={}'
    page = 1
    start_urls = [base_url.format(page)]

    def parse(self, response):
        # 获取所有节点
        node_list = response.xpath('//div[@class="info_wrp"]/div')
        # print(len(node_list), 'dddddddddddddd')

        for node in node_list:
            item = BilibiliItem()
            item['url'] = node.xpath('./a/@href').extract_first()
            item['name'] = node.xpath('./a/@title').extract_first()
            # 构建对详细页面的情求
            yield scrapy.Request(item['url'], callback=self.parse_desc, meta={'item': item}, dont_filter=True)

        if len(node_list) == 20:
            self.page += 1
            next_url = self.base_url.format(self.page)
            # print(next_url)
            yield scrapy.Request(next_url, dont_filter=True)

    def parse_desc(self, response):

        item = response.meta['item']

        item['play_count'] = response.xpath('//div[@class="info-count"]/span[1]/em/text()').extract_first()
        item['play_nums'] = response.xpath('//div[@class="info-count"]/span[2]/em/text()').extract_first()
        item['barrage'] = response.xpath('//div[@class="info-count"]/span[3]/em/text()').extract_first()
        item['play_time'] = response.xpath('//div[@class="info-row info-update"]/em/span[1]/text()').extract_first().strip().split('\n')[0]
        item['play_state'] = response.xpath('//div[@class="info-row info-update"]/em/span[2]/text()').extract_first()
        item['desc'] = response.xpath('//div[@class="info-desc"]/text()').extract_first().replace('\n', '')

        yield item

