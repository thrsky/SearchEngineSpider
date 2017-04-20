# _*_ coding=utf-8 _*_

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
    def from_crawl(cls,crawler):
        return cls(crawler)

    def process_request(self,request,spider):
        def get_ua():
            return  getattr(self.ua,self.ua_type)
        random_user_agent=get_ua()
        request.headers.setdefault('User_Agent',get_ua())