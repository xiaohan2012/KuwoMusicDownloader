from urllib2 import *
from simplejson import loads
from threading import Thread
from Queue import Queue
import os

class MusicDownloadRequest(Request):
    def __init__(self,rid,referer):
        headers =  {}
        headers["Cookie"] = 'JSESSIONID=F66E7D2DBFC2D163CECFF6074260A455.worker1; mbox=MUSIC_2.0.2.2; rec_usr=1339604827413x852_0_1343046767042; searchHistory=%u83AB%u624E%u7279; Hm_lvt_cdb524f42f0ce19b169a8071123a4797=1343047346116; Hm_lpvt_cdb524f42f0ce19b169a8071123a4797=1343047346116; ad_dist=%25BA%25FE%25B1%25B1'
        headers['Referer'] = referer 

        Request.__init__(self,'http://www.kuwo.cn/yy/st/DownPath?rid=%s' %rid , headers = headers)

class MusicDownloader():
    @staticmethod
    def download(req,save_path):
        res_str = urlopen(req).read()
        res_str = res_str.replace("\'","\"")
        res_obj = loads(res_str)
        down_url = "http://%s%s" %(res_obj['server'],res_obj['path'])
        
        fp = '%s/%s.acc' %(save_path , res_obj['name'])
        with open(fp,'w') as f:
            f.write(urlopen(down_url).read())
        print "%s  saved" %fp
        return True

class DownloadThread(Thread):
    def __init__(self,queue):
        Thread.__init__(self)
        self.q = queue
    
    def run(self):
        while True:
            rid , referer , save_path = self.q.get()
            req = MusicDownloadRequest(rid,referer)
            dl = MusicDownloader
            dl.download(req , save_path)
            self.q.task_done()
        
class BatchDownloader(object):
    def __init__(self , rids , referer , save_path):
        if not os.path.exists(save_path):
            os.mkdir(save_path)

        self.q = Queue()
        for rid in rids:
            self.q.put((rid,referer,save_path))

    def start(self):
        for i in xrange(4):
             t = DownloadThread(self.q)
             t.setDaemon(True)
             t.start()
        self.q.join()
        print "download done"

if __name__ == "__main__":
    rid = 'MUSIC_575016'
    referer = 'http://www.kuwo.cn/zhuanji/833277/'
    save_path = '.'

    req = MusicDownloadRequest(rid,referer)
    dl = MusicDownloader
    dl.download(req , save_path)
