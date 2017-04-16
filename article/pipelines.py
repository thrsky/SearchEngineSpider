# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
import codecs
import json
from scrapy.exporters import JsonItemExporter
from twisted.enterprise import adbapi
import pymysql
import pymysql.cursors


class ArticlePipeline(object):
    def process_item(self, item, spider):
        return item


class JsonWithEncodingPipeline(object):
    #自定义json文件输出
    def __init__(self):
        self.file = codecs.open('article.json','w',encoding="utf-8")

    def process_item(self,item,spider):
        lines=json.dumps(dict(item),ensure_ascii=False) + "\n"
        self.file.write(lines)
        return item

    def spider_closed(self,spider):
        self.file.close()


class JsonExporterPipeline(object):
    #调用scrapy提供的json export导出json文件
    def __init__(self):
        self.file = open('articleexport.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding="utf-8", ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class MysqlPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect('localhost','root','19960411','articleSpider',charset="utf8",use_unicode=True)
        self.cursor=self.connect.cursor()

    def process_item(self,item,spider):
        insert_sql="""
            insert into jobbole_article(title,url,url_object_id,front_image_url,front_image_path,create_date,zan,remark,collect,tags,content)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        self.cursor.execute(insert_sql,(item["title"],item["url"],item["url_object_id"],item["front_image_url"],item["front_image_path"],item["create_date"],item["zan"],item["remark"],item["collect"],item["tags"],item["content"]))
        self.connect.commit()

#===================================================================================


#异步化数据库插入
class MysqlTwistedPipline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host = settings["MYSQL_HOST"],
            db = settings["MYSQL_DBNAME"],
            user = settings["MYSQL_USER"],
            passwd = settings["MYSQL_PASSWORD"],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("pymysql", **dbparms)

        return cls(dbpool)

    def process_item(self, item, spider):
        #使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider) #处理异常

    def handle_error(self, failure, item, spider):
        # 处理异步插入的异常
        print (failure)

    def do_insert(self,cursor,item):
        #执行具体插入
        insert_sql = """
                    insert into jobbole_article(title,url,url_object_id,front_image_url,front_image_path,create_date,zan,remark,collect,tags,content)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """
        cursor.execute(insert_sql, (
        item["title"], item["url"], item["url_object_id"], item["front_image_url"], item["front_image_path"],
        item["create_date"], item["zan"], item["remark"], item["collect"], item["tags"], item["content"]))


#============================================================================================


class ArticleImagePipeline(ImagesPipeline):
    #图片下载
    def item_completed(self, results, item, info):
        if "front_image_url" in item:
            for ok,value in results:
                image_file_path = value["path"]
            item["front_image_path"]=image_file_path
        return item