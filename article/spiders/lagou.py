# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from article.items import LagouJobItemLoader
from article.items import LagouJobItem
from article.utils.common import get_md5,get_salary,get_year

class LagouSpider(CrawlSpider):
    name = 'lagou'
    allowed_domains = ['www.lagou.com']
    start_urls = ['https://www.lagou.com/']

    rules = (
        Rule(LinkExtractor(allow=r'jobs/\d+.html'), callback='parse_job', follow=True),
        Rule(LinkExtractor(allow="zhaopin/.*"),follow=True),
        Rule(LinkExtractor(allow=("gongsi/.*")),follow=True)
    )

    def parse_job(self, response):

        item_loader=LagouJobItemLoader(item=LagouJobItem(),response=response)
        item_loader.add_value("url",response.url)
        item_loader.add_value("url_object_id",get_md5(response.url))
        item_loader.add_css("title",'.job-name::attr("title")')
        salary=response.css('.job_request .salary::text').extract_first()
        item_loader.add_value('salary_min',get_salary(salary).__getitem__(0))
        item_loader.add_value('salary_max',get_salary(salary).__getitem__(1))
        item_loader.add_xpath('job_city','//*[@class="job_request"]/p/span[2]/text()')
        years=response.xpath('//*[@class="job_request"]/p/span[3]/text()').extract_first()
        item_loader.add_value('work_years_min',get_year(years).__getitem__(0))
        item_loader.add_value('work_years_max',get_year(years).__getitem__(1))
        item_loader.add_xpath('degree_need','//*[@class="job_request"]/p/span[4]/text()')
        item_loader.add_xpath('job_time','//*[@class="job_request"]/p/span[5]/text()')
        item_loader.add_css('publish_time','.publish_time::text')
        item_loader.add_xpath('tags','//*[@class="position-label clearfix"]/li/text()')
        item_loader.add_xpath('job_advantage','//*[@class="job-advantage"]/p/text()')
        item_loader.add_css('job_desc','.job_bt div')
        item_loader.add_css('job_addr','.work_addr')
        item_loader.add_css('company','#job_company dt a img::attr(alt)')
        item_loader.add_css('company_url','#job_company dt a::attr(href)')
        item_loader.add_value('crawl_time',datetime.now())

        jobItem=item_loader.load_item()

        return jobItem
