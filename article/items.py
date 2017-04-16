# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticleItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class JobboleArticleItem(scrapy.Item):
    title=scrapy.Field()
    create_date=scrapy.Field()
    url=scrapy.Field()
    url_object_id=scrapy.Field()
    front_image_url=scrapy.Field()
    front_image_path=scrapy.Field()
    zan=scrapy.Field()
    remark=scrapy.Field()
    collect=scrapy.Field()
    tags=scrapy.Field()
    content=scrapy.Field()
    autor=scrapy.Field()