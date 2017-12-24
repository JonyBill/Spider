# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import requests
import json
import base64
import random


class ZhihuSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class RandomIpProxyMiddleware(object):
    def __init__(self):
        self.url = 'http://dps.kuaidaili.com/api/getdps/?orderid=911367392272041&num=50&ut=1&format=json&sep=1'

    def process_request(self, request, spider):
        r = requests.get(self.url)

        PROXIES = json.loads(r.content.decode())['data']['proxy_list']

        user = 'cyy_dfh:vubkq0wc'
        b64_user_pwd = base64.b64encode(user.encode())

        # 随机获取一个代理
        proxy = random.choice(PROXIES)
        # print (proxy)

        # 设置代理认证
        request.headers['Proxy-Authorization'] = "Basic " + b64_user_pwd.decode()

        # 使用IP代理
        request.meta['proxy'] = "http://" + proxy
