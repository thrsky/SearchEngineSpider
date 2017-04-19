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
from article.utils.common import extract_num
from article.settings import SQL_DATE_FORMAT,SQL_DATETIME_FORMAT
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

#============================================================================

def remove_splash(value):
    return value.replace("/","")


def getJob_addr(value):
    li=re.findall(r'([\u4e00-\u9fa5].*[\u4e00-\u9fa5])',value)
    try:
        li.remove("查看地图")
    except Exception as e:
        pass
    return (" - ").join(li)

#拉钩网信息Item
class LagouJobItem(scrapy.Item):
    url=scrapy.Field()
    url_object_id=scrapy.Field()
    title=scrapy.Field()
    salary_min=scrapy.Field()
    salary_max=scrapy.Field()
    job_city=scrapy.Field(
        input_processor=MapCompose(remove_splash)
    )
    work_years_min=scrapy.Field()
    work_years_max=scrapy.Field()
    degree_need=scrapy.Field(
        input_processor=MapCompose(remove_splash)
    )
    degree_need=scrapy.Field(
        input_processor=MapCompose(remove_splash)
    )
    job_time=scrapy.Field()
    publish_time=scrapy.Field()
    tags=scrapy.Field(
        output_processor=Join(",")
    )
    job_advantage=scrapy.Field()
    job_desc=scrapy.Field(
        input_processor=MapCompose(getJob_addr)
    )
    job_addr=scrapy.Field(
        input_processor=MapCompose(getJob_addr)
    )
    company=scrapy.Field()
    company_url=scrapy.Field()
    crawl_time=scrapy.Field()

    def get_insert_sql(self):
        insert_sql="""
            insert into lagou_job(title,url,url_object_id,salary_min,salary_max,job_city,work_years_min,
              work_years_max,degree_need,job_time,publish_time,tags,job_advantage,job_desc,job_addr,company,company_url,crawl_time)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        parms=(
            self["title"],self["url"],self["url_object_id"],self["salary_min"],self["salary_max"],self["job_city"],
            self["work_years_min"],self["work_years_max"],self["degree_need"],self["job_time"],
            self["publish_time"],self["tags"],self["job_advantage"],self["job_desc"],self["job_addr"],self["company"],self["company_url"],self["crawl_time"]
        )
        return insert_sql,parms


#================================================================================================
#import new 网站文章爬取
def get_time(value):
    time=re.match('(\d+?/\d+?/\d+?) | 分类',value)
    if time:
        return time.group(1)


def get_tags(value):
    list=re.findall('>(.*?)</a>',value)
    res=list[2]
    for tag in list[3:]:
        res=res+" , "+tag
    return res


class ImportNewItemLoader(ItemLoader):
    default_output_processor = TakeFirst()

class InputNewItem(scrapy.Item):
    title=scrapy.Field()
    url=scrapy.Field()
    url_id=scrapy.Field()
    update_time=scrapy.Field(
        input_processor=MapCompose(get_time)
    )
    category=scrapy.Field()
    tags=scrapy.Field(
        input_processor=MapCompose(get_tags)
    )
    content=scrapy.Field()

    def get_insert_sql(self):
        insert_sql="""
            insert into inputnew(title,url,url_id,update_time,category,tags,content)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
        """
        parms=(
            self["title"],self["url"],self["url_id"],self["update_time"],self["category"],self["tags"],
            self["content"]
        )
        return insert_sql,parms


#====================================================================================
#电影
class MovieItemLoader(ItemLoader):
    default_output_processor = TakeFirst()

class movieItem(scrapy.Item):
    pass


#=====================================================================================
#知乎
class ZhihuQuesItemLoader(ItemLoader):
    default_output_processor = TakeFirst()

class ZhihuAnswerItemLoader(ItemLoader):
    default_output_processor = TakeFirst()

#知乎回答Item
class ZhihuAnswerItem(scrapy.Item):
    answer_id = scrapy.Field()
    url = scrapy.Field()
    question_id = scrapy.Field()
    author_id = scrapy.Field()
    content = scrapy.Field()
    parise_num = scrapy.Field()
    comments_num = scrapy.Field()
    create_time = scrapy.Field()
    update_time = scrapy.Field()
    crawl_time = scrapy.Field()

    def get_insert_sql(self):
        # 插入知乎question表的sql语句
        insert_sql = """
            insert into zhihu_answer(answer_id, url, question_id, author_id, content, parise_num, comments_num,
              create_time, update_time, crawl_time
              ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
              ON DUPLICATE KEY UPDATE content=VALUES(content), comments_num=VALUES(comments_num), parise_num=VALUES(parise_num),
              update_time=VALUES(update_time)
        """

        create_time = datetime.datetime.fromtimestamp(self["create_time"]).strftime(SQL_DATETIME_FORMAT)
        update_time = datetime.datetime.fromtimestamp(self["update_time"]).strftime(SQL_DATETIME_FORMAT)
        params = (
            self["answer_id"], self["url"], self["question_id"],
            self["author_id"], self["content"], self["parise_num"],
            self["comments_num"], create_time, update_time,
            self["crawl_time"].strftime(SQL_DATETIME_FORMAT),
        )

        return insert_sql, params

#知乎问题Item
class ZhihuQuesItem(scrapy.Item):
    question_id = scrapy.Field()
    title = scrapy.Field()
    topic = scrapy.Field()
    url = scrapy.Field()
    content = scrapy.Field()
    create_time = scrapy.Field()
    update_time = scrapy.Field()
    answer_num = scrapy.Field()
    comments_num = scrapy.Field()
    watch_user_num = scrapy.Field()
    click_num = scrapy.Field()
    crawl_time = scrapy.Field()

    def get_insert_sql(self):
        # 插入知乎question表的sql语句
        insert_sql = """
            insert into zhihu_question(question_id, title, topic, url,  content, answer_num, comments_num,
              watch_user_num, click_num, crawl_time
              )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE content=VALUES(content), answer_num=VALUES(answer_num), comments_num=VALUES(comments_num),
              watch_user_num=VALUES(watch_user_num), click_num=VALUES(click_num)
        """
        question_id = self["question_id"][0]
        topic = ",".join(self["topic"])
        url = self["url"][0]
        title = "".join(self["title"])
        content = "".join(self["content"])
        answer_num = extract_num("".join(self["answer_num"]))
        comments_num = extract_num("".join(self["comments_num"]))

        if len(self["watch_user_num"]) == 2:
            watch_user_num = int(self["watch_user_num"][0])
            click_num = int(self["watch_user_num"][1])
        else:
            watch_user_num = int(self["watch_user_num"][0])
            click_num = 0

        crawl_time = datetime.datetime.now().strftime(SQL_DATETIME_FORMAT)

        params = (question_id, title, topic, url,  content, answer_num, comments_num,
                  watch_user_num, click_num, crawl_time)

        return insert_sql, params
