# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class ZhihuItem(Item):
    # define the fields for your item here like:
    # 名字
    name = Field()
    # url识别
    url_token = Field()
    # 标题
    headline = Field()
    # 个人描述
    description = Field()
    # 工作行业
    business = Field()
    # 教育背景
    educations = Field()
    # 所在地
    locations = Field()
    # 入职公司
    employments = Field()

    # 回答数
    answer_count = Field()
    # 提问数
    question_count = Field()
    # 文章数
    articles_count = Field()
    # 专栏
    columns_count = Field()
    # 想法
    pins_count = Field()

    # 收到的赞
    voteup_count = Field()
    # 收到的感谢
    thanked_count = Field()
    # 被收藏数
    favorited_count = Field()
    # 参与公共编辑
    logs_count = Field()
    # 被知乎收录的回答
    included_answers_count = Field()
    # 被知乎收录到的文章
    included_articles_count = Field()

    # 关注数
    following_count = Field()
    # 粉丝数
    follower_count = Field()
    # 赞助的Live
    participated_live_count = Field()
    # 关注的话题
    following_topic_count = Field()
    # 关注的专栏
    following_columns_count = Field()
    # 关注的问题
    following_question_count = Field()
    # 关注的收藏夹
    following_favlists_count = Field()
