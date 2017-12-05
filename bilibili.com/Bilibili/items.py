# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BilibiliItem(scrapy.Item):
    # define the fields for your item here like:
    # 番剧连接
    url = scrapy.Field()
    # 番名
    name = scrapy.Field()
    # 总播放量
    play_count = scrapy.Field()
    # 追番人数
    play_nums = scrapy.Field()
    # 弹幕总数
    barrage = scrapy.Field()
    # 开播时间
    play_time = scrapy.Field()
    # 播放状态
    play_state = scrapy.Field()
    # 番剧简介
    desc = scrapy.Field()
    pass
