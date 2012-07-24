from util import BatchDownloader
from crawler import get_rids


if __name__ == "__main__":
    url = 'http://www.kuwo.cn/zhuanji/833277/#@'
    rids = get_rids(url)

    bd = BatchDownloader(rids,url,'mozart')
    bd.start()
