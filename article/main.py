# -*- coding: utf-8 -*-
# 用于方便调试 scrapy
from scrapy.cmdline import execute

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
#print(sys.path)
#execute(["scrapy","crawl","Jobbole"])

if __name__ == '__main__':
    #print(os.path.dirname(os.path.abspath(__file__)))
    execute(["scrapy", "crawl", "movie"])