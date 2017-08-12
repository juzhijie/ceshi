# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class DingdianItem(scrapy.Item):
    # define the fields for your item here like:
    author = scrapy.Field()
    article_title = scrapy.Field()
    content = scrapy.Field()
    book = scrapy.Field()


