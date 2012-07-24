from urllib2 import *
from pyquery import PyQuery as pq
import re

def get_rids(url):
    doc = pq(url)
    for song in doc(".listCont .itemUl"):
        func_ = pq(pq(song).find(".iNum a")[2])
        yield re.findall('\w+_\d+' , func_.attr("onclick"))[0]

if __name__ == "__main__":
    url = 'http://www.kuwo.cn/zhuanji/833277/#@'
    for rid in get_rids(url):
        print rid

