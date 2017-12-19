# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
from scrapy.conf import settings
from pymysql import *
import json


class Tongcheng58Pipeline(object):
    def process_item(self, item, spider):
        return item


class DuplicatesPipeline(object):
    # 去重
    def __init__(self):
        self.urls_seen = set()

    def process_item(self, item, spider):
        if item['city'] in self.urls_seen or '//g.58.com/' in item['city_url']:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.urls_seen.add(item['city'])
            return item


class City58Pipeline(object):

    def __init__(self):
        self.f = open('58all_city_url.py', 'a')

    def process_item(self, item, spider):
        # 这一句相当于关掉中间件
        if spider.name != '58city':
            return item

        i = 1

        # 获取全部二手房租房的url, 不排除一些不可到达页数
        # 最大70页
        while i < 71:
            i_str = str(i)
            ershoufang = '\t\t\'' + item['city_url'] + 'chuzu/pn' + i_str + '\',\n'
            # chuzu = '\'' + item['city_url'] + 'chuzu/pn' + i_str + '\',\n'
            self.f.write(ershoufang)
            i += 1

        return item

    def close_spider(self, spider):
        self.f.close()


class MysqlPipeline(object):
    def __init__(self):
        host = settings['MYSQL_HOST']
        port = settings['MYSQL_PORT']
        user = settings['MYSQL_USER']
        passwd = settings['MYSQL_PASSWD']
        dbname = settings['MYSQL_DBNAME']
        charset = settings['MYSQL_CHARSET']

        # 连接数据库
        self.con = connect(host=host,
                           port=port,
                           user=user,
                           password=passwd,
                           database=dbname,
                           charset=charset,
                        )

        # 获取操作对象
        self.cur = self.con.cursor()

    def process_item(self, item, spider):
        # 编写sql语句
        create_table = 'CREATE TABLE ershoufang (' \
                       'id int PRIMARY KEY NOT NUll auto_increment,' \
                       'house_url VARCHAR(50),' \
                       'title VARCHAR (100),' \
                       't_price VARCHAR(10),' \
                       'a_price VARCHAR(20),' \
                       'area VARCHAR (30),' \
                       'house_desc TEXT ,' \
                       'house_from VARCHAR (30),' \
                       'house_where VARCHAR(5),' \
                       'phone VARCHAR(15),' \
                       'house_size VARCHAR(20),' \
                       'house_type VARCHAR(10),' \
                       'village VARCHAR (30)' \
                    ');'

        # 插入数据语句
        insert_sql = """
                     insert into ershoufang(
                     house_url,title,t_price,a_price,area,house_desc,house_from,
                     house_where,phone,house_size,house_type,village)
                     VALUES (%s, %s, %s, %s, %s, %s,
                     %s, %s, %s, %s, %s, %s);
                      """

        try:
            # self.cur.execute(create_table)
            self.cur.execute(insert_sql,
                             (item['house_url'], item['title'], item['total_price'], item['avg_price'],
                             item['area'], item['house_desc'], item['house_from'], item['house_where'],
                             item['phone'], item['size'], item['type'], item['village']))
            self.con.commit()

        except Exception as e:
            print(e)

        return item

    def close_sql(self, spider):
        self.cur.close()
        self.con.close()


class FilePipeline(object):
    def __init__(self):
        self.file = open('house.json', 'a')

    def process_item(self, item, spider):
        str_data = json.dumps(dict(item), ensure_ascii=False) + ',\n'

        self.file.write(str_data)

        return item

    def close_item(self, spider):
        self.file.close()