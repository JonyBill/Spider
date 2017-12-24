# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Tongcheng58Item(scrapy.Item):
    # define the fields for your item here like:
    # 城市
    city = scrapy.Field()
    # 城市url
    city_url = scrapy.Field()
    # 标题
    title = scrapy.Field()
    # 房屋链接
    house_url = scrapy.Field()
    # 房价
    total_price = scrapy.Field()
    # 均价
    avg_price = scrapy.Field()
    # 租价
    hire_price = scrapy.Field()
    # 户型
    type = scrapy.Field()
    # 大小
    size = scrapy.Field()
    # 房屋朝向
    house_where = scrapy.Field()
    # 地点小区
    village = scrapy.Field()
    # 所属区域
    area = scrapy.Field()
    # 交通位置
    sub_away = scrapy.Field()
    # 房子描述
    house_desc = scrapy.Field()
    # 联系电话
    phone = scrapy.Field()
    # 房屋来源
    house_from = scrapy.Field()
    pass
