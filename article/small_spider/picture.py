# _*_ coding:utf8 _*_

from selenium import webdriver
from scrapy.selector import Selector
import urllib
import re, random, os,requests

session=requests.session()
brower = webdriver.Chrome(executable_path="G:/Python/爬虫/scrapy/chromedriver.exe")
image_path = "E:/Picture"
import time

brower.get("http://www.polayoutu.com/collections")
for i in range(20):
    brower.execute_script(
        "window.scrollTo(0,document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage")
    time.sleep(3)
t_selector = Selector(text=brower.page_source)
print(t_selector)
image_url = t_selector.css(".download_original::attr(href)").extract()
for url in image_url:
    image_count = random.randint(10000, 20000)
    image_name=image_path+"/"+str(image_count)+".jpg"
    t = session.get(url)
    with open(image_name, 'wb') as f:
        f.write(t.content)
        f.close()



# print(image_url)

# print(brower.page_source)
