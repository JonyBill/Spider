"""
解析车站js
"""
import requests
import re


def main():
    url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9035'
    # 要关闭证书
    res = requests.get(url, verify=False)
    # print(res.text)
    # 用正则匹配出我们需要的东西
    pattern = u'([\u4e00-\u9fa5]+)\|([A-Z]+)'
    result = dict(re.findall(pattern, res.text))
    print(list(result.keys()))
    print(list(result.values()))

if __name__ == '__main__':
    main()