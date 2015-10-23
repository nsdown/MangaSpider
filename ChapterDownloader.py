import requests
import jsbeautifier
import re
import os
import time
import threading


class ChapterDownloader(threading.Thread):
    def __init__(self, proxy=None):
        threading.Thread.__init__(self)
        self.__baseURL = None
        self.__chPath = None
        self.__chURL = None
        self.__chfunBasePath = None
        self.__chfunBaseURL = None
        self.__lang = None
        self.__gtk = None
        self.cid = None
        self.__headers = None
        self.downloadDir = None
        self.__proxy = proxy
        return

    def GetWork(self, chpath):
        self.__baseURL = "http://www.dm5.com"
        self.__chPath = chpath
        self.__chURL = self.__baseURL + self.__chPath
        self.__chfunBasePath = chpath + "/chapterfun.ashx"
        self.__chfunBaseURL = self.__baseURL + self.__chfunBasePath
        self.__lang = "1"
        self.__gtk = "6"
        self.cid = chpath.split('m')[-1]
        self.__headers = {
            "Referer": self.__chURL
        }
        cwd = os.getcwd()
        self.downloadDir = cwd + "\\" + self.cid
        return

    def EchoFromChfun(self, page):
        chfunUrl = self.__chfunBaseURL + "?cid=" + self.cid + "&page=" + str(
            page) + "&key=&language=" + self.__lang + "&gtk=" + self.__gtk
        rawResp = requests.get(chfunUrl, headers=self.__headers, proxies=self.__proxy)
        niceResp = jsbeautifier.beautify(rawResp.content)
        key = re.sub('[^a-zA-Z\d]', '', niceResp[niceResp.find("key") + 3:niceResp.find("var", niceResp.find("key"))])
        pix = niceResp[niceResp.find("pix") + 3:niceResp.find("var", niceResp.find("pix"))].split("\"")[-2]
        pvalue = [niceResp[niceResp.find("pvalue") + 5:niceResp.find("var", niceResp.find("pvalue"))].split("\"")[i] for
                  i in [1, -2]]
        imgUrl = pix + pvalue[0] + "?cid=" + self.cid + "&key=" + key
        return imgUrl, pvalue[0] != pvalue[1]

    def DownloadOneImg(self, page):
        echo = self.EchoFromChfun(page)
        r = requests.get(echo[0], headers=self.__headers, proxies=self.__proxy)
        imgPath = self.downloadDir + "\\" + str(page) + ".png"
        imgDir = os.path.dirname(imgPath)
        if not os.path.exists(imgDir):
            os.makedirs(imgDir)
        with open(imgPath, "wb") as f:
            f.write(r.content)
        print "Page " + str(page) + " of chapter " + self.cid + " has been downloaded! "
        if echo[1]:
            return True
        else:
            print "Whole chapter " + self.cid + " has been downloaded! "
            return False

    def Work(self, sleepTime):
        page = 1
        while True:
            undone = self.DownloadOneImg(page)
            if undone:
                page += 1
                time.sleep(sleepTime)
            else:
                break
