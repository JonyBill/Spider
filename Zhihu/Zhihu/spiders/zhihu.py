# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import json
from Zhihu.items import ZhihuItem
# 分布式类
from scrapy_redis.spiders import RedisSpider


class ZhihuSpider(RedisSpider):
    name = "zhihu"
    # allowed_domains = ["www.zhihu.com"]
    # 用户,关注者和粉丝 的api
    user_url = 'https://www.zhihu.com/api/v4/members/{user}?include={include}'
    follows_url = 'https://www.zhihu.com/api/v4/members/{user}/followees?include={include}&offset={offset}&limit={limit}'
    followers_url = 'https://www.zhihu.com/api/v4/members/{user}/followers?include={include}&offset={offset}&limit={limit}'
    # 以轮子哥为开始
    start_user = 'excited-vczh'
    # get请求需要携带的固定参数include
    user_include = 'locations,employments,gender,educations,business,voteup_count,thanked_Count,follower_count,following_count,cover_url,following_topic_count,following_question_count,following_favlists_count,following_columns_count,avatar_hue,answer_count,articles_count,pins_count,question_count,columns_count,commercial_question_count,favorite_count,favorited_count,logs_count,included_answers_count,included_articles_count,included_text,message_thread_token,account_status,is_active,is_bind_phone,is_force_renamed,is_bind_sina,is_privacy_protected,sina_weibo_url,sina_weibo_name,show_sina_weibo,is_blocking,is_blocked,is_following,is_followed,is_org_createpin_white_user,mutual_followees_count,vote_to_count,vote_from_count,thank_to_count,thank_from_count,thanked_count,description,hosted_live_count,participated_live_count,allow_message,industry_category,org_name,org_homepage,badge[?(type=best_answerer)].topics'
    follow_include = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'
    followers_include = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'

    redis_key = 'zhihu_key'
    # start_url
    # https://www.zhihu.com/api/v4/members/excited-vczh?include=locations,employments,gender,educations,business,voteup_count,thanked_Count,follower_count,following_count,cover_url,following_topic_count,following_question_count,following_favlists_count,following_columns_count,avatar_hue,answer_count,articles_count,pins_count,question_count,columns_count,commercial_question_count,favorite_count,favorited_count,logs_count,included_answers_count,included_articles_count,included_text,message_thread_token,account_status,is_active,is_bind_phone,is_force_renamed,is_bind_sina,is_privacy_protected,sina_weibo_url,sina_weibo_name,show_sina_weibo,is_blocking,is_blocked,is_following,is_followed,is_org_createpin_white_user,mutual_followees_count,vote_to_count,vote_from_count,thank_to_count,thank_from_count,thanked_count,description,hosted_live_count,participated_live_count,allow_message,industry_category,org_name,org_homepage,badge[?(type=best_answerer)].topics

    def __init__(self, *args, **kwargs):
        domain = kwargs.pop('domain', '')
        self.allowed_domains = list(filter(None, domain.split(',')))
        super(ZhihuSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        # 对第一个用户构建请求
        yield Request(self.user_url.format(user=self.start_user, include=self.user_include), self.parse_user)

    def parse_user(self, response):
        result = json.loads(response.text)
        item = ZhihuItem()

        # 获取数据
        for field in item.fields:
            if field in result.keys():
                item[field] = result.get(field)

        # 返回数据
        yield item
        # 发送该用户的关注者api请求
        yield Request(
            self.follows_url.format(user=result.get('url_token'), include=self.follow_include, limit=20, offset=0),
            self.parse_follows)

        # 发送该用户的粉丝api请求
        yield Request(
            self.followers_url.format(user=result.get('url_token'), include=self.followers_include, limit=20, offset=0),
            self.parse_followers)

    def parse_follows(self, response):
        # 解析关注者api
        results = json.loads(response.text)

        # 遍历每个关注者获取其用户api进行递归
        if 'data' in results.keys():
            for result in results.get('data'):
                yield Request(self.user_url.format(user=result.get('url_token'), include=self.user_include),
                              self.parse_user)

        # 翻页
        if 'paging' in results.keys() and not results.get('paging').get('is_end'):
            next_page = results.get('paging').get('next')
            yield Request(next_page,
                          self.parse_follows)

    def parse_followers(self, response):
        # 解析粉丝api
        results = json.loads(response.text)

        if 'data' in results.keys():
            for result in results.get('data'):
                yield Request(self.user_url.format(user=result.get('url_token'), include=self.user_include),
                              self.parse_user)

        if 'paging' in results.keys() and not results.get('paging').get('is_end'):
            next_page = results.get('paging').get('next')
            yield Request(next_page,
                          self.parse_followers)