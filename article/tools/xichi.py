# _*_ coding:utf-8 -*-

import requests
from scrapy.selector import Selector
import pymysql

conn = pymysql.connect(host="localhost",user="root",passwd="19960411",db="articlespider",charset="utf8")
curosr = conn.cursor()

def crawl_ips():
    headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"
    }

    for i in range(1700):

        re=requests.get('http://www.xicidaili.com/nn/{0}'.format(i),headers=headers)
        selector=Selector(text=re.text)
        trs=selector.css("#ip_list tr")
        ip_list = []
        for tr in trs[1:]:
            speed=0
            speed_str=tr.css(".bar::attr(title)").extract()[0]
            if speed_str:
                speed=float(speed_str.split("秒")[0])
            all_texts=tr.css("td::text").extract()
            ip=all_texts[0]
            port=all_texts[1]
            proxy=all_texts[5]

            ip_list.append((ip,port,speed,proxy))

        for ip_info in ip_list:
            curosr.execute(
                    "insert into proxy_ip(ip,port,speed,proxy) VALUES ('{0}','{1}','{2}','HTTP')".format(
                        ip_info[0],ip_info[1],ip_info[2]
                    )
            )

            conn.commit()
        # print (re.text)


class getIp(object):

    def junge_ip(self,ip,port):
        #判断IP是否可用
        http_url="https://www.baidu.com"
        proxy_url="http://{0}:{1}".format(ip,port)
        import requests
        try:
            proxy_dict={
                "http":proxy_url,
            }
            response = requests.get(url = http_url, proxies = proxy_dict)
        except Exception as e:
            print("ip error")
            self.delete_ip(ip)
            return False
        else:
            code=response.status_code
            if code>=200 and code<300:
                print("effective ip")
                return True
            else:
                print("ip error")
                self.delete_ip(ip)
                return False


    def delete_ip(self,ip):
        detele_ip_sql="""
            delete from proxy_ip WHERE ip='{0}'
        """.format(ip)
        curosr.execute(detele_ip_sql)
        conn.commit()
        return True


    def get_random_ip(self):
        get_ip_sql="""
            select ip,port from proxy_ip 
            ORDER by RAND()
            limit 1           
        """
        result=curosr.execute(get_ip_sql)
        for ip_info in curosr.fetchall():
            ip=ip_info[0]
            port=ip_info[1]

            junge_re = self.junge_ip(ip,port)
            if junge_re:
                print("get ip ok ")
                return "http://{0}:{1}".format(ip,port)
            else:
                return self.get_random_ip()



if __name__ == "__main__":
    g=getIp()
    g.get_random_ip()