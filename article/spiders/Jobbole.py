# -*- coding: utf-8 -*-
import scrapy


class JobboleSpider(scrapy.Spider):
    name = "Jobbole"
    allowed_domains = ["blog.jobbole.com"]
    start_urls = (
        'http://blog.jobbole.com/110860/',
    )

    def parse(self, response):
        title = response.xpath('//*[@class="entry-header"]/h1/text()').extract()[0]
        create_date = response.xpath('//*[@class="entry-meta"]/p[1]/text()').extract()/[0].strip()
        autor = response.xpath('//*[@class="copyright-area"]/a/text()').extract()
        print(title+" "+create_date+" "+autor)

        pass
