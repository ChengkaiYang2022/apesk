# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AdvantageScoreItem(scrapy.Item):
    """
    记录评估人的每一项优势与分数
    """
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 评估人id
    id = scrapy.Field()
    # 评估人姓名
    name = scrapy.Field()
    # 提交时间
    submit_time = scrapy.Field()
    # 优势id
    advantage_id = scrapy.Field()
    # 优势名称
    advantage_name = scrapy.Field()
    # 分数
    score = scrapy.Field()
    # url = scrapy.Field()

    pass


class AdvantageItem(scrapy.Item):
    """
    记录36项优势的描述
    """
    # 优势名称
    advantage_name = scrapy.Field()
    # xxx的盖洛普五项优势
    advantage_desc = scrapy.Field()
    # xxx的第一优势：思维
    advantage_desc_more_info = scrapy.Field()
