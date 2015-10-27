import requests
import jsbeautifier
import re
import os
from ImageDownloader import ImageDownloader
import sys, time


class ChapterDownloader:
    def __init__(self, taskQueue, proxy=None):
        # threading.Thread.__init__(self)
        self.__chWork = None
        self.__baseURL = "http://www.dm5.com"
        self.__lang = None
        self.__gtk = None
        self.__cid = None
        self.__headers = None
        self.__proxy = proxy
        self.tasker = taskQueue
        self.__workerAmount = 30
        self.__workerPool = []
        self.WorkersLineup()
        return

    def GetChapterName(self):
        return self.__chWork.chName

    def GetDownloadDir(self):
        return self.__chWork.downloadDir

    def GetImgQueue(self):
        return self.__chWork.imgQueue

    def GetProxy(self):
        return self.__proxy

    def GetHeaders(self):
        return self.__headers

    def GetWork(self):
        self.__chWork = self.tasker.GetChapterWork()
        self.__lang = "1"
        self.__gtk = "6"
        self.__cid = self.__chWork.chPath.split('m')[-1]
        self.__headers = {
            "Referer": self.__baseURL + self.__chWork.chPath
        }
        if not os.path.exists(self.__chWork.downloadDir):
            os.makedirs(self.__chWork.downloadDir)
        sys.stdout.write(time.asctime(time.localtime(time.time()))+" : "+"Retrieving image urls......\n")
        self.PutWorkIntoQueue()
        sys.stdout.write(time.asctime(time.localtime(time.time()))+" : "+"Downloading images of chapter "+self.GetChapterName()+"\n")
        return

    def EchoFromChfun(self, page):
        chfunUrl = self.__baseURL + self.__chWork.chPath + "/chapterfun.ashx" + "?cid=" + self.__cid + "&page=" + str(
            page) + "&key=&language=" + self.__lang + "&gtk=" + self.__gtk
        rawResp = requests.get(chfunUrl, headers=self.__headers, proxies=self.__proxy)
        niceResp = jsbeautifier.beautify(rawResp.content)
        key = re.sub('[^a-zA-Z\d]', '', niceResp[niceResp.find("key") + 3:niceResp.find("var", niceResp.find("key"))])
        pix = niceResp[niceResp.find("pix") + 3:niceResp.find("var", niceResp.find("pix"))].split("\"")[-2]
        pvalue = [niceResp[niceResp.find("pvalue") + 5:niceResp.find("var", niceResp.find("pvalue"))].split("\"")[i] for
                  i in [1, -2]]
        imgUrl = pix + pvalue[0] + "?cid=" + self.__cid + "&key=" + key
        return imgUrl, page, pvalue[0] == pvalue[1]

    def PutWorkIntoQueue(self):
        page = 1
        while True:
            try:
                imgUrl, page, isLastpage = self.EchoFromChfun(page)
                self.__chWork.PutIntoImgQueue((imgUrl, page))
                if isLastpage:
                    break
                else:
                    page += 1
            except:
                sys.stdout.write(time.asctime(time.localtime(time.time()))+" : "+"Failed retrieving img url of page: "+str(page)+"\n")
                continue

    def WorkersLineup(self):
        for i in range(self.__workerAmount):
            # you can set sleep time to 0 if u want
            self.__workerPool.append(ImageDownloader(self, 0))
        return

    def Work(self):
        for worker in self.__workerPool:
            if not worker.isDaemon():
                worker.setDaemon(True)
                worker.start()
        # TODO kill all threads at last
        self.GetImgQueue().join()
        sys.stdout.write(time.asctime(time.localtime(time.time()))+" : "+"All images of chapter "+self.GetChapterName()+ " has been downloaded\n")
        self.tasker.PutIntoMergerQueue(self.__chWork)
        return
