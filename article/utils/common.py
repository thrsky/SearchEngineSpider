# -*- coding: utf-8 -*-

import hashlib,re

def get_md5(url):
    if isinstance(url,str):
        url=url.encode("utf-8")
    m=hashlib.md5()
    m.update(url)
    return m.hexdigest()

def get_salary(value):
    if value:
        min_re=re.match('(\d+?)k-(\d+?)k',value)
        if min_re:
            min=(int(min_re.group(1))*1000)
            max=(int(min_re.group(2))*1000)
        else:
            min=0
            max=0
        return min,max
    else:
        return 0,0

def get_year(value):
    if value:
        year=re.match('经验(\d+?)-(\d+?)年',value)
        if year:
            min=int(year.group(1))
            max=int(year.group(2))
        else:
            min=0
            max=0
        return min,max
    else:
        return 0,0


def getJob_addr(value):
    li=re.findall(r'#filterBox">(.*?)</a>',value)
    return (" - ").join(li)


def extract_num(text):
    #从字符串中提取出数字
    match_re = re.match(".*?(\d+).*", text)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0

    return nums