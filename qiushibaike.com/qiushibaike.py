import requests
from lxml import etree
import json


class Qiushibaike(object):
    """
    爬取糗事百科的段子,
    段子加载在html源码中,
    热门13页之后点更多跳转到24小时的段子,也是13页,
    一页25条,共650条
    """
    def __init__(self):
        self.hot_url = 'https://www.qiushibaike.com/hot/page/{}/'
        self.url = 'https://www.qiushibaike.com/8hr/page/{}/'
        self.host = 'https://www.qiushibaike.com'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36'
        }
        self.url_list = []

    def generate(self):
        self.url_list = [self.url.format(i) for i in range(1, 14)] + [self.hot_url.format(i) for i in range(1, 14)]

    def get_data(self, url):
        response = requests.get(url, headers=self.headers)
        return response.content.decode()

    def parse_data(self, data):
        html = etree.HTML(data)
        node_list = html.xpath('//*[@id="content-left"]/div')

        # print(len(node_list)) 打印一下以防出错

        data_list = []

        for node in node_list:
            temp = {}
            try:
                temp['user'] = node.xpath('./div[1]/a[2]/h2/text()')[0].strip()
                temp['user_link'] = self.host + node.xpath('./div[1]/a[2]/@href')[0]
            except:
                temp['user'] = '匿名用户'
                temp['user_link'] = None
            try:
                # 有图片就保存下
                temp['img_url'] = node.xpath('./div[2]/a/img/@src')[0]
            except:
                pass

            temp['hahaha'] = node.xpath('./div[2]/span[1]/i/text() | ./div[3]/span[1]/i/text()')[0]
            temp['content'] = node.xpath('./a[1]/div/span/text()')[0].strip()
            temp['content_url'] = self.host + node.xpath('./a[1]/@href')[0]
            # print(temp)
            data_list.append(temp)
        # print(len(data_list))
        return data_list

    def save_data(self, data_list):
        with open('qiushibaike.json', 'a') as f:
            for data in data_list:
                str_data = json.dumps(data, ensure_ascii=False) + ',\n'
                f.write(str_data)

    def run(self):
        self.generate()
        for url in self.url_list:
            # 获取源文件
            data = self.get_data(url)
            # 解析抽取
            data_list = self.parse_data(data)
            # 保存
            self.save_data(data_list)


if __name__ == '__main__':
    qiushi = Qiushibaike()
    qiushi.run()