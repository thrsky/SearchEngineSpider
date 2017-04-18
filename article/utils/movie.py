# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen
import re
import lxml

def getScore():
    html=urlopen('http://www.ygdy8.com/html/gndy/dyzz/20170413/53729.html')
    soup=BeautifulSoup(html.read(),"lxml")
    #print(soup)
    score_re=re.match('◎豆瓣评分　(.*?)/10 from',soup.text,re.DOTALL)
    if score_re:
        score_re=score_re.group(1)
        print(score_re)
    else:
        print("no score")


getScore()