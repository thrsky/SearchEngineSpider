# _*_ coding=utf-8 _*_
from article.tools.xichi import getIp
import logging
from fake_useragent import UserAgent


logging=logging.getLogger(__name__)

class RandomUserAgentMiddleware(object):
    #随机切换user_agent

    def __init__(self,crawler):
        super(RandomUserAgentMiddleware, self).__init__()
        self.ua=UserAgent()
        self.ua_type=crawler.settings.get("RAMDOM_UA_TYPE","random")


    @classmethod
    def from_crawler(cls,crawler):
        return cls(crawler)

    def process_request(self,request,spider):
        def get_ua():
            return  getattr(self.ua,self.ua_type)
        random_user_agent=get_ua()
        request.headers.setdefault('User_Agent',get_ua())


class RandomProxyMiddleware(object):
    def process_request(self,request,spider):
        get_ip=getIp()
        request.meta["proxy"]=get_ip.get_random_ip()


from scrapy.http import HtmlResponse
class JsPageMiddleware(object):

    def process_request(self, request, spider):
        if spider.name == "Jobbole":
            spider.browser.get(request.url)
            import time
            time.sleep(3)
            print("访问：{0}".format(request.url))

            #请求过后就不用再用scrapy的下载器来下载了
            return HtmlResponse(url=spider.browser.current_url,
                                body=spider.browser.page_source,
                                encoding="utf-8",
                                request=request
                                )

        pass
