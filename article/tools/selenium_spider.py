# _*_ coding:utf8 _*_

from selenium import webdriver
from scrapy.selector import Selector
from urllib.request import urlopen
import re,random,os
# brower = webdriver.Chrome(executable_path="G:/Python/爬虫/scrapy/chromedriver.exe")
# image_path="E:/Picture"
# import time
# brower.get("http://www.polayoutu.com/collections")
        
#==================================================================
"""
    selenium使用基本流程
    from selenium import webdriver
    import scrapy.selector import Selector
    brower=webdriver.Chrome(executable_path="下载好的对应浏览器的插件")  Chrome也要换成自己电脑上的浏览器
    例如：#brower = webdriver.Chrome(executable_path="G:/Python/爬虫/scrapy/chromedriver.exe")
    
    brower.get("http://www.baidu.com")
    text=brower.get_source #返回加载好后的网页代码
    t_selector=Selector(text=text)  #用scrapy的Selector选择器来加载网页代码  方便以后用xpath和css选择信息
    例如：t_selector.xpath('')
         t_selector.css('')
    
"""
#设置Chromedriver不加载图片
chrome_opt=webdriver.ChromeOptions()
prefs={"profile.managed_default_content_settings.images":2}
chrome_opt.add_experimental_option("prefs",prefs)
brower = webdriver.Chrome(executable_path="G:/Python/爬虫/scrapy/chromedriver.exe",chrome_options=chrome_opt)
brower.get("https://www.taobao.com")


#phantomjs 无界面的浏览器
#多线程的情况下 phantomjs性能会下降很严重
#在Linux下比较有用

# phantomjs_path="你的phantomjs路径"
# web=webdriver.PhantomJS(executable_path=phantomjs_path)
# text=web.page_source
# web.quit()





















# print(brower.page_source)
