# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose,TakeFirst,Join
import datetime
import re
from scrapy.loader import ItemLoader


class ArticleItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


def date_format(value):
    try:
        create_date=datetime.datetime.strptime(value,"%Y%m%d").date()
    except Exception as e:
        create_date=datetime.datetime.now()
    return create_date


def get_nums(value):
    match_re=re.match(".*?(\d+).*",value)
    if match_re:
        nums=int(match_re.group(1))
    else:
        nums=0
    return nums


def getValue(value):
    return value


def remove_comment_tags(value):
    if "评论" in value:
        return ""
    else:
        return value


class AriticleItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class LagouJobItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class JobboleArticleItem(scrapy.Item):
    title=scrapy.Field()
    create_date=scrapy.Field(
        input_processor=MapCompose(date_format)
    )
    url=scrapy.Field()
    url_object_id=scrapy.Field()
    front_image_url=scrapy.Field(
        output_processor=MapCompose(getValue)
    )
    front_image_path=scrapy.Field()
    zan=scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    remark=scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    collect=scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    tags=scrapy.Field(
        input_processor=MapCompose(remove_comment_tags),
        output_processor=Join(",")
    )
    content=scrapy.Field()
    #autor=scrapy.Field()


class LagouJobItem(scrapy.Item):
    url=scrapy.Field()
    url_object_id=scrapy.Field()
    title=scrapy.Field()
    salary_min=scrapy.Field()
    salary_max=scrapy.Field()
    job_city=scrapy.Field()
    work_years_min=scrapy.Field()
    work_years_max=scrapy.Field()
    degree_need=scrapy.Field()
    job_time=scrapy.Field()
    publish_time=scrapy.Field()
    tags=scrapy.Field()
    job_advantage=scrapy.Field()
    job_desc=scrapy.Field()
    job_addr=scrapy.Field()
    company=scrapy.Field()
    company_url=scrapy.Field()
    crawl_time=scrapy.Field()
