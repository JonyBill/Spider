# -*- coding: utf-8 -*-
import scrapy
from Tongcheng58.items import Tongcheng58Item


class A58citySpider(scrapy.Spider):
    name = '58city'
    allowed_domains = ['www.58.com']
    start_urls = ['http://www.58.com/changecity.aspx']

    def parse(self, response):
        city_list = response.xpath('//*[@id="clist"]/dd/a')

        # 获取城市名和58城市的url(数目459条, 初步判断有重复, 中间件去重)
        for city in city_list:
            i = Tongcheng58Item()
            i['city'] = city.xpath('text()').extract_first()
            i['city_url'] = city.xpath('@href').extract_first()

            yield i
