# -*- coding: utf-8 -*-
import scrapy
import re
from article.items import ImportNewItemLoader,InputNewItem
from article.utils.common import get_md5
from scrapy.http import Request
from urllib import parse

class ImportnewSpider(scrapy.Spider):
    name = "importnew"
    allowed_domains = ["www.importnew.com"]
    start_urls = ['http://www.importnew.com/all-posts/']

    def parse(self, response):
        post_node=response.css('.post-meta .meta-title::attr(href)').extract()
        if post_node:
            for url in post_node:
                post_url=str(url)
                yield Request(url=parse.urljoin(response.url, post_url),callback=self.parse_detail)

        next_url=response.css('.next.page-numbers::attr(href)').extract_first()
        if next_url:
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

    def parse_detail(self,response):

        item_loader=ImportNewItemLoader(item=InputNewItem(),response=response)

        item_loader.add_xpath('title','//*[@class="entry-header"]/h1/text()')
        item_loader.add_value('url',response.url)
        item_loader.add_value('url_id',get_md5(response.url))
        #待提取
        item_loader.add_xpath('update_time','//*[@class="entry-meta-hide-on-mobile"]/text()')
        item_loader.add_xpath('category','//*[@class="entry-meta-hide-on-mobile"]/a[1]/text()')
        #从第2个 列表项开始
        item_loader.add_css('tags','.entry-meta-hide-on-mobile')
        item_loader.add_css('content','.entry')

        importNewItem=item_loader.load_item()

        yield importNewItem
