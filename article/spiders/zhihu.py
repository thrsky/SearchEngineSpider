# -*- coding: utf-8 -*-

"""
    知乎的模拟登录在 utils下的 zhiju_login_request中可以顺利完成
    但是在scrapy下，还有一些不稳定
    因为scrapy是基于twisted ， 所以很多请求可能是交叉进行的，
    每个request之间的session的一致性问题，需要注意
    
"""
import re
import json
import datetime
import requests
from article.items import ZhihuAnswerItem,ZhihuQuesItem,ZhihuQuesItemLoader
try:
    import urlparse as parse
except:
    from urllib import parse

from scrapy.http import Request
import scrapy,datetime
session =requests.session()

class ZhihuSpider(scrapy.Spider):
    name = "zhihu"
    allowed_domains = ["www.zhihu.com"]
    start_urls = ['https://www.zhihu.com/']

    # question的第一页answer的请求url
    start_answer_url = "https://www.zhihu.com/api/v4/questions/{0}/answers?sort_by=default&include=data%5B%2A%5D.is_normal%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccollapsed_counts%2Creviewing_comments_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Cmark_infos%2Ccreated_time%2Cupdated_time%2Crelationship.is_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B%2A%5D.author.is_blocking%2Cis_blocked%2Cis_followed%2Cvoteup_count%2Cmessage_thread_token%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&limit={1}&offset={2}"

    headers = {
        "HOST": "www.zhihu.com",
        "Referer": "https://www.zhizhu.com",
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0"
    }

    def parse(self, response):
        """
                    提取HTML中所有的URL，并跟踪这些URL
                    如果提取的URL中格式为 /question/******， 下载之后直接进入解析函数
                """
        all_urls = response.css("a::attr(href)").extract()
        # 拼接URL
        all_urls = [parse.urljoin(response.url, url) for url in all_urls]
        all_urls = filter(lambda x: True if x.startswith("https") else False, all_urls)
        for obj in all_urls:
            match_obj = re.match('(.*zhihu.com/question/(\d+))(/|$).*.', obj)
            if match_obj:
                request_url = match_obj.group(1)
                yield Request(request_url,headers=self.headers,callback=self.parse_question)
            else:
                yield Request(obj,headers=self.headers,callback=self.parse)

    #提取问题属性
    def parse_question(self, response):
        #处理question页面
        if "QuestionHeader-title" in response.text:
            qu_re=re.match("(.*zhihu.com/question/(\d+))(/|$).*",response.url)
            question_id=0
            if qu_re:
                question_id=int(qu_re.group(2))
            item_loader = ZhihuQuesItemLoader(item=ZhihuQuesItem(),response=response)
            item_loader.add_value('question_id',question_id)
            item_loader.add_css('title','h1.QuestionHeader-title::text')
            item_loader.add_css('content','.QuestionHeader-detail')
            item_loader.add_value("url",response.url)
            item_loader.add_css("answer_num",'.List-headerText span::text')
            item_loader.add_xpath("comments_num",'//*[@class="QuestionHeader-actions"]/button[1]/text()')
            item_loader.add_css('watch_user_num','.NumberBoard-value::text')
            item_loader.add_css("topic", ".QuestionHeader-topics .Popover div::text")
            question_item = item_loader.load_item()

        else:
            qu_re = re.match("(.*zhihu.com/question/(\d+))(/|$).*", response.url)
            question_id = 0
            if qu_re:
                question_id = int(qu_re.group(2))
            item_loader = ZhihuQuesItemLoader(item=ZhihuQuesItem(), response=response)
            # item_loader.add_css("title", ".zh-question-title h2 a::text")
            item_loader.add_xpath("title",
                                  "//*[@id='zh-question-title']/h2/a/text()|//*[@id='zh-question-title']/h2/span/text()")
            item_loader.add_css("content", "#zh-question-detail")
            item_loader.add_value("url", response.url)
            item_loader.add_value("question_id", question_id)
            item_loader.add_css("answer_num", "#zh-question-answer-num::text")
            item_loader.add_css("comments_num", "#zh-question-meta-wrap a[name='addcomment']::text")
            # item_loader.add_css("watch_user_num", "#zh-question-side-header-wrap::text")
            item_loader.add_xpath("watch_user_num",
                                  "//*[@id='zh-question-side-header-wrap']/text()|//*[@class='zh-question-followers-sidebar']/div/a/strong/text()")
            item_loader.add_css("topic", ".zm-tag-editor-labels a::text")
            question_item = item_loader.load_item()

        yield Request(url=self.start_answer_url.format(question_id, 20, 0), headers=self.headers, callback=self.parse_answer)
        yield question_item


    #回答的属性存储在一Json中
    def parse_answer(self, response):
        #传进来的是json字符串
        print(" --------------- parse ---------> answer \n")
        ans_json=json.loads(response.text)
        is_end=ans_json["paging"]["is_end"]
        next_url=ans_json["paging"]["next"]

        for answer in ans_json["data"]:
            answer_item = ZhihuAnswerItem()
            answer_item["answer_id"] = answer["id"]
            answer_item["url"] = answer["url"]
            answer_item["question_id"] = answer["question"]["id"]
            answer_item["author_id"] = answer["author"]["id"] if "id" in answer["author"] else None
            answer_item["content"] = answer["content"] if "content" in answer else None
            answer_item["parise_num"] = answer["voteup_count"]
            answer_item["comments_num"] = answer["comment_count"]
            answer_item["create_time"] = answer["created_time"]
            answer_item["update_time"] = answer["updated_time"]
            answer_item["crawl_time"] = datetime.datetime.now()

            yield answer_item

        if not is_end:
            yield scrapy.Request(next_url, headers=self.headers, callback=self.parse_answer)


    #scrapy爬虫的入口函数
    #一般都要重写来 执行我们自己的一些逻辑
    def start_requests(self):
        return [scrapy.Request('https://www.zhihu.com/#signin', headers=self.headers, callback=self.login)]

    #第一步的登录
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
                "phone_num": "18858903314",
                "password": "admin",
                "captcha":""
            }

            import time
            t = str(int(time.time() * 1000))
            captcha_url = "https://www.zhihu.com/captcha.gif?r={0}&type=login".format(t)
            yield scrapy.Request(captcha_url,headers=self.headers,
                                 meta={"post-data":post_data},callback=self.login_after_capctha)



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
            print("登录成功")
            for url in self.start_urls:
                yield scrapy.Request(url, dont_filter=True, headers=self.headers)
