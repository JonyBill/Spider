#### Douban

利用`CrawlSpider`爬取豆瓣电影top250，数据包括：电影名，评分，简介和电影信息

#### Bilibili

`Scrapy` + `Selenium` 爬取bilibili共2930部番剧的追番人数，播放总量，弹幕量，开播时间，简介等番剧信息
`Selenium`用来处理ajax和js的动态加载数据，效率比较低

#### Qiushibaike

`request`来爬取糗事百科的段子，练手项

#### 12306

分析12306api接口， 解析其js来写出一个可以查询火车票的api， 利用到命令行库`docopt`和表格库`prettytable`， 效果展示如下：

输入出发地-目的地以及指定日期：例如 北京 天津 2017-12-25
![api](https://raw.githubusercontent.com/yycang/Pic/master/12306tickets.png)

#### 58tongcheng

`Scrapy`爬取存储到`MySQL`， 58同城的反爬措施是常见的ip速度限制， 当ip访问频率到达一定值的时候会重定向到滑块验证码页， 足够的ip代理池可解决此问题

#### zhihu

`Scrapy-redis`爬取知乎用户信息， 控制好访问速度， 不需要cookie也可以进行爬取， 最后数据持久化到`MongoDB`中
