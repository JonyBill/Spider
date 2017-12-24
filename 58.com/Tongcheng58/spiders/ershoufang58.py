# -*- coding: utf-8 -*-
import scrapy
from Tongcheng58.items import Tongcheng58Item
from Tongcheng58.spiders.all_city_url import AllCityUrl
from scrapy.http import Request
from Tongcheng58.spiders.headers import Headers
import random
import base64


class Ershoufang58Spider(scrapy.Spider):
    name = 'ershoufang58'
    allowed_domains = ['58.com']
    start_urls = AllCityUrl.erShouFangUrl

    # 重写start_requests方法
    def start_requests(self):

        for url in self.start_urls:
            yield Request(url,
                          headers={
                                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                                "Accept-Language": "zh-CN,zh;q=0.8",
                                "Connection": "keep-alive",
                                "Host": url.split('/')[2],
                                "Upgrade-Insecure-Requests": "1",
                                "User-Agent": random.choice(Headers.agents),
                                "Cookie": "f=n; userid360_xml=9723E1DC821147DFDE66629B98746103; time_create=1516017353349; id58=c5/nn1n4au99jfXvEZptAg==; Hm_lvt_5bcc464efd3454091cf2095d3515ea05=1511962806; als=0; commontopbar_myfeet_tooltip=end; wmda_visited_projects=%3B2385390625025; wmda_uuid=450aba6df0c4b0a1fd03b35372a42c67; wmda_new_uuid=1; commontopbar_ipcity=bj%7C%E5%8C%97%E4%BA%AC%7C0; defraudName=defraud; Hm_lvt_dcee4f66df28844222ef0479976aabf1=1513354001,1513404444; Hm_lpvt_dcee4f66df28844222ef0479976aabf1=1513408681; ppStore_fingerprint=ED4899C6B4D6EDCCE4AC37989324B22DF6BC29056259D01A%EF%BC%BF1513408711970; jy=2018015171623; cs=2018015171946; huaibei=2018015173420; _ga=GA1.2.240506950.1513409419; _gid=GA1.2.212703961.1513414045; __utma=253535702.240506950.1513409419.1513412384.1513419612.3; __utmc=253535702; __utmz=253535702.1513409419.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); bj=2018015205546; f=n; city=bj; 58home=bj; 58tj_uuid=f56b2396-c918-4f4f-9ec7-40a0873059c5; new_session=0; new_uv=7; utm_source=; spm=; init_refer=http%253A%252F%252Fwww.58.com%252Fchangecity.aspx; commontopbar_new_city_info=1%7C%E5%8C%97%E4%BA%AC%7Cbj; xxzl_deviceid=vmqkvj3RYNETTo8U3vUGt2zmaq67Z6fJSJJjYyQNwvSsG%2BY5lB%2Fp1EfmtqIo0SQu",
                            })

    def parse(self, response):

        house_list = response.xpath('/html/body/div[4]/div[5]/div[1]/ul/li')

        for house in house_list:
            i = Tongcheng58Item()
            i['house_url'] = house.xpath('./div[2]/h2/a/@href').extract_first()
            i['title'] = house.xpath('./div[2]/h2/a/text()').extract_first().strip()
            i['total_price'] = house.xpath('./div[3]/p[1]/b/text()').extract_first() + '万'
            i['avg_price'] = house.xpath('./div[3]/p[2]/text()').extract_first()
            i['type'] = house.xpath('./div[2]/p[1]/span[1]/text()').extract_first().replace(' ', '')
            i['size'] = house.xpath('./div[2]/p[1]/span[2]/text()').extract_first().strip()
            try:
                i['house_where'] = house.xpath('./div[2]/p[1]/span[3]/text()').extract_first().strip()
            except Exception:
                i['house_where'] = None

            yield scrapy.Request(i['house_url'], callback=self.detail_parse,
                                 meta={'item': i}, dont_filter=True)

    def detail_parse(self, response):

        i = response.meta['item']

        pic_li = []

        i['village'] = ''.join(response.xpath('/html/body/div[4]/div[2]/div[2]/ul/li[1]/span[2]/a/text()').extract()).replace(' ', '')
        i['area'] = ''.join(response.xpath('/html/body/div[4]/div[2]/div[2]/ul/li[2]/span[2]/a/text()').extract())
        i['house_desc'] = ''.join(response.xpath('//*[@id="generalDesc"]/div/div[1]/p/text()').extract()).replace('\r\n', '').strip('\n').replace(' ', '')
        i['house_from'] = response.xpath('/html/body/div[4]/div[2]/div[2]/div[2]/p[1]/span/text()').extract_first().replace(' 说', '').strip()
        i['phone'] = response.xpath('//*[@id="houseChatEntry"]/div/p[3]/text()').extract_first()

        yield i


