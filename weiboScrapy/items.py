# Define here the models for your scraped items
#

import scrapy

class ArticleItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    mid =  scrapy.Field()            # mid
    mblogid = scrapy.Field()         # mblogid
    wtext = scrapy.Field()           # 微博内容
    text_raw = scrapy.Field()        # 微博内容，去掉链接的
    created_at = scrapy.Field()       # 创建时间
    region_name = scrapy.Field()     # 发布区域
    source = scrapy.Field()          # 微博来源
    reposts_count = scrapy.Field()   # 转发数
    comments_count = scrapy.Field()  # 评论数
    attitudes_count = scrapy.Field() # 点赞数
    topic_title = scrapy.Field()     # 话题

    user_id = scrapy.Field()         # 用户ID
    screen_name = scrapy.Field()     # 用户昵称

# TODO 还没写完
class CommentItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    mid =  scrapy.Field()            # mid
    mblogid = scrapy.Field()         # mblogid
    wtext = scrapy.Field()           # 微博内容
    text_raw = scrapy.Field()        # 微博内容，去掉链接的
    created_at = scrapy.Field()       # 创建时间
    region_name = scrapy.Field()     # 发布区域
    source = scrapy.Field()          # 微博来源
    reposts_count = scrapy.Field()   # 转发数
    comments_count = scrapy.Field()  # 评论数
    attitudes_count = scrapy.Field() # 点赞数
    topic_title = scrapy.Field()     # 话题

    user_id = scrapy.Field()         # 用户ID
    screen_name = scrapy.Field()     # 用户昵称

# 微博内容
class WeiboItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    mid = scrapy.Field()
    bid = scrapy.Field()
    user_id = scrapy.Field()
    screen_name = scrapy.Field()
    text = scrapy.Field()
    article_url = scrapy.Field()
    location = scrapy.Field()
    at_users = scrapy.Field()
    topics = scrapy.Field()
    reposts_count = scrapy.Field()
    comments_count = scrapy.Field()
    attitudes_count = scrapy.Field()
    created_at = scrapy.Field()
    source = scrapy.Field()
    pics = scrapy.Field()
    video_url = scrapy.Field()
    retweet_id = scrapy.Field()
    ip = scrapy.Field()
    user_authentication = scrapy.Field()
    keywords = scrapy.Field()               # 关键词
    label = scrapy.Field()                  # 情感分析结果
