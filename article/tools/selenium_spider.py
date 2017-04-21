# _*_ coding:utf8 _*_

from selenium import webdriver
from scrapy.selector import Selector
from urllib.request import urlopen
import re,random,os
brower = webdriver.Chrome(executable_path="G:/Python/爬虫/scrapy/chromedriver.exe")
image_path="E:/Picture"
import time
brower.get("http://www.polayoutu.com/collections")
for i in range(3):
    brower.execute_script("window.scrollTo(0,document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage")
    time.sleep(3)
t_selector=Selector(text=brower.page_source)
image_url=t_selector.css(".download_original::attr(href)").extract()
if image_url:
    image_name = random.randint(10000, 20000)
    res=urlopen(image_url)
    if res.getcode()!=200:
        pass
    else:
        data=res.read()
        




print(image_url)

# print(brower.page_source)
