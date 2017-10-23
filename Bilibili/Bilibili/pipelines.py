# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json


class BilibiliPipeline(object):
    def __init__(self):
        self.file = open('bilibili_anime.csv', 'w')

    def process_item(self, item, spider):
        # 转换数据
        str_data = json.dumps(dict(item), ensure_ascii=False) + ',\n'
        self.file.write(str_data)

        return item

    def close_file(self, spider):
        self.file.close()