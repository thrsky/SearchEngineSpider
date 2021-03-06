# -*- coding: utf-8 -*-
import scrapy
import re
import datetime
from scrapy.http import Request
from urllib import parse
from article.items import JobboleArticleItem,AriticleItemLoader
from article.utils.common import get_md5
from scrapy.loader import ItemLoader
from selenium import webdriver
#引入信号量 机制
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
#伯乐在线 文章爬取


class JobboleSpider(scrapy.Spider):
    name = "Jobbole"
    allowed_domains = ["blog.jobbole.com"]
    start_urls = ['http://blog.jobbole.com/all-posts/']


    #在这里我们初始化一个Chrome 这样一来就不会每个URL打开一个Chrome了
    def  __init__(self):
        self.browser=webdriver.Chrome(executable_path="G:/Python/爬虫/scrapy/chromedriver.exe")
        super(JobboleSpider,self).__init__()
        dispatcher.connect(self.spider_closed,signals.spider_closed)

    def spider_closed(self,spider):
        #当爬虫退出的时候  退出Chrome
        self.browser.quit()

    def parse(self, response):
        """
        1、获取文章列表页中的具体文件URL 并交给scrapy下载后 用解析函数进行具体字段的解析        
        2、获取下一页的URL 并交给scrapy下载       
        :param response: 
        :return: 
        """
        #解析列表页中所有文章URL
        post_nodes = response.css("#archive .floated-thumb .post-thumb a")
        for post_node in post_nodes:
            image_url=post_node.css("img::attr(src)").extract_first("")
            post_url=post_node.css("::attr(href)").extract_first("")
            yield Request(url=parse.urljoin(response.url,post_url), meta={"front_image_url":image_url}, callback=self.parse_detail)

        #提取下一页并交给scrapy
        next_url=response.css(".next.page-numbers::attr(href)").extract_first("")
        if next_url:
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

    def parse_detail(self,response):
        """
            提取文件具体字段
        :param response: 
        :return: 
        """

        # jobble_item=JobboleArticleItem()
        # #图片URL
        # front_image_url=response.meta.get("front_image_url","")
        # title = response.xpath('//*[@class="entry-header"]/h1/text()').extract_first("")
        # create_date = response.xpath('//*[@class="entry-meta"]/p[1]/text()').extract()[0].strip().replace("·","").strip()
        # content=response.xpath('//div[@class="entry"]').extract()[0]
        # #文章标签
        # classfiy_list=response.xpath('//p[@class="entry-meta-hide-on-mobile"]/a/text()').extract()
        # classfiy_list = [tag for tag in classfiy_list if not tag.strip().endswith("评论")]
        # tags = (",").join(classfiy_list)
        # #赞数
        # zan=int(response.xpath('//span[contains(@class,"vote-post-up")]/h10/text()').extract()[0])
        # #评论
        # remark=response.xpath('//span[contains(@class,"btn-bluet-bigger")]/text()').extract()[3]
        # match_re=re.match(".*?(\d+).*",remark)
        # if match_re:
        #     remark=int(match_re.group(1))
        # else:
        #     remark=0
        # #收藏
        # collect=response.xpath('//span[contains(@class,"btn-bluet-bigger")]/text()').extract()[2]
        # match_re = re.match(".*?(\d+).*", collect)
        # if match_re:
        #     collect =int(match_re.group(1))
        # else:
        #     collect=0
        #
        # # item赋值
        # jobble_item["title"]=title
        # jobble_item["url"]=response.url
        # jobble_item["url_object_id"]=get_md5(response.url)
        # try:
        #     create_date = datetime.datetime.strftime(create_date,"%Y/%m/%d").date()
        # except Exception as e:
        #     create_date = datetime.datetime.now().date()
        # jobble_item["create_date"]=create_date
        # jobble_item["front_image_url"]=[front_image_url]
        # jobble_item["zan"]=zan
        # jobble_item["collect"]=collect
        # jobble_item["remark"]=remark
        # jobble_item["tags"]=tags
        # jobble_item["content"]=content
        # #jobble_item["autor"]=autor


        #通过Itemloader加载item
        #item_loader=ItemLoader(item=JobboleArticleItem(),response=response)

        front_image_url = response.meta.get("front_image_url", "")  # 文章封面图
        item_loader = AriticleItemLoader(item=JobboleArticleItem(), response=response)
        item_loader.add_css("title", ".entry-header h1::text")
        item_loader.add_value("url", response.url)
        item_loader.add_value("url_object_id", get_md5(response.url))
        item_loader.add_css("create_date", "p.entry-meta-hide-on-mobile::text")
        item_loader.add_value("front_image_url", [front_image_url])
        item_loader.add_css("zan", ".vote-post-up h10::text")
        item_loader.add_css("remark", "a[href='#article-comment'] span::text")
        item_loader.add_css("collect", ".bookmark-btn::text")
        item_loader.add_css("tags", "p.entry-meta-hide-on-mobile a::text")
        item_loader.add_css("content", "div.entry")

        jobble_item=item_loader.load_item()

        yield jobble_item
