import requests
import jsbeautifier
import re
import os
from ImageDownloader import ImageDownloader


class ChapterDownloader():
    def __init__(self, taskQueue, proxy=None):
        # threading.Thread.__init__(self)
        self.__baseURL = "http://www.dm5.com"
        self.__chPath = None
        self.__chURL = None
        self.__chfunBasePath = None
        self.__chfunBaseURL = None
        self.__lang = None
        self.__gtk = None
        self.__cid = None
        self.__headers = None
        self.__downloadDir = None
        self.__proxy = proxy
        self.tasker = taskQueue
        self.__workerAmount = 10
        self.__workerPool = []
        return

    def GetQueue(self):
        return self.tasker.workPool[self.__cid]

    def GetCid(self):
        return self.__cid

    def GetDownloadDir(self):
        return self.__downloadDir

    def GetProxy(self):
        return self.__proxy

    def GetHeaders(self):
        return self.__headers

    def GetWork(self, chpath):
        self.__chPath = chpath
        self.__chURL = self.__baseURL + self.__chPath
        self.__chfunBasePath = chpath + "/chapterfun.ashx"
        self.__chfunBaseURL = self.__baseURL + self.__chfunBasePath
        self.__lang = "1"
        self.__gtk = "6"
        self.__cid = chpath.split('m')[-1]
        self.tasker.PutIntoChapterQueue(self.__cid)
        self.__headers = {
            "Referer": self.__chURL
        }
        cwd = os.getcwd()
        self.__downloadDir = cwd + "\\" + self.__cid
        if not os.path.exists(self.__downloadDir):
            os.makedirs(self.__downloadDir)
        self.PutWorkIntoQueue()
        return

    def EchoFromChfun(self, page):
        chfunUrl = self.__chfunBaseURL + "?cid=" + self.__cid + "&page=" + str(
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
                self.tasker.PutIntoImageWorkQueue(self.__cid, (imgUrl, page))
                if isLastpage:
                    break
                else:
                    page += 1
            except:
                # TODO hear echo failed
                return

    def WorkersLineup(self):
        for i in range(self.__workerAmount):
            self.__workerPool.append(ImageDownloader(self))
        return

    def Work(self):
        self.WorkersLineup()
        for worker in self.__workerPool:
            worker.setDaemon(True)
            worker.start()
        print "Downloading images of chapter ", self.__cid
        self.GetQueue().join()
        print "All images of chapter ", self.__cid, " has been downloaded"
        return

