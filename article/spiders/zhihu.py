# -*- coding: utf-8 -*-
import re
import json
import datetime
import requests

try:
    import urlparse as parse
except:
    from urllib import parse

import scrapy
from scrapy.loader import ItemLoader
from article.items import ZhihuQuestionItem, ZhihuAnswerItem

session =requests.session()

class ZhihuSpider(scrapy.Spider):
    name = "zhihu"
    allowed_domains = ["www.zhihu.com"]
    start_urls = ['https://www.zhihu.com/']

    #question的第一页answer的请求url
    start_answer_url = "https://www.zhihu.com/api/v4/questions/{0}/answers?sort_by=default&include=data%5B%2A%5D.is_normal%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccollapsed_counts%2Creviewing_comments_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Cmark_infos%2Ccreated_time%2Cupdated_time%2Crelationship.is_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B%2A%5D.author.is_blocking%2Cis_blocked%2Cis_followed%2Cvoteup_count%2Cmessage_thread_token%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&limit={1}&offset={2}"

    headers = {
        "HOST": "www.zhihu.com",
        "Referer": "https://www.zhizhu.com",
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0"
    }

    def parse(self, response):
        pass

    def parse_question(self, response):
        pass

    def parse_answer(self, reponse):
        pass


    def start_requests(self):
        return [scrapy.Request('https://www.zhihu.com/#signin', headers=self.headers, callback=self.login)]

    def login(self, response):
        response_text = response.text
        match_obj = re.match('.*name="_xsrf" value="(.*?)"', response_text, re.DOTALL)
        xsrf = ''
        if match_obj:
            xsrf = (match_obj.group(1))

        if xsrf:
            post_url = "https://www.zhihu.com/login/phone_num"
            post_data = {
                "_xsrf": xsrf,
                "phone_num": "18782902568",
                "password": "admin123",
                "captcha":""
            }

            import time
            t = str(int(time.time() * 1000))
            captcha_url = "https://www.zhihu.com/captcha.gif?r={0}&type=login".format(t)
            yield scrapy.Request(captcha_url,headers=self.headers,callback=self.login_after_capctha)



    def login_after_capctha(self,response):
        post_data=response.meta.get("post-data",{})
        post_url = "https://www.zhihu.com/login/phone_num"
        with open("images/captcha.jpg", 'wb') as f:
            f.write(response.body)
            f.close()
        from PIL import Image
        try:
            im = Image.open('images/captcha.jpg')
            im.show()
            im.close()
        except:
            pass

        captcha = input("输入验证码\n")
        post_data["captcha"]=captcha
        return [scrapy.FormRequest(
            url=post_url,
            formdata=post_data,
            headers=self.headers,
            callback=self.check_login
        )]


    def check_login(self, response):
        #验证服务器的返回数据判断是否成功
        text_json = json.loads(response.text)
        if "msg" in text_json and text_json["msg"] == "登录成功":
            for url in self.start_urls:
                yield scrapy.Request(url, dont_filter=True, headers=self.headers)

