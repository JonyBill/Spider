# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import pymongo
from scrapy.exceptions import DropItem


class ZhihuPipeline(object):
    def process_item(self, item, spider):
        return item


class DuplicatesPipeline(object):
    # 去重
    def __init__(self):
        self.urls_seen = set()

    def process_item(self, item, spider):
        if item['url_token'] in self.urls_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.urls_seen.add(item['url_token'])
            return item


class FilePipeline(object):
    def __init__(self):
        self.file = open('user.json', 'w')

    def process_item(self, item, spider):
        str_data = json.dumps(dict(item), ensure_ascii=False) + ',\n'

        self.file.write(str_data)

        return item

    def close_item(self, spider):
        self.file.close()


class MongoPipeline(object):
    """官方文档中的存入mongo数据库demo"""
    collection_name = 'users'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        # 更新数据, 第三个参数表示如果没有查找到原先的数据则插入一条新数据(在数据库上完成去重)
        self.db[self.collection_name].update({'url_token': item['url_token']}, {'$set': dict(item)}, True)
        return item