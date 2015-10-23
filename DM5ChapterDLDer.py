import requests
import jsbeautifier
import re
import os
import time


class DM5ChapterDLDer:
    def __init__(self, chpath):
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
        self.currentPage = 1
        return

    def GetChfunURL(self, page):
        return self.__chfunBaseURL + "?cid=" + self.cid + "&page=" + str(
            page) + "&key=&language=" + self.__lang + "&gtk=" + self.__gtk

    def EchoFromChfun(self, sleepTime, proxy=None):
        self.currentPage = 1
        while True:
            req = requests.get(self.GetChfunURL(self.currentPage), headers=self.__headers, proxies=proxy)
            resp = jsbeautifier.beautify(req.content)
            key = re.sub('[^a-zA-Z\d]', '', resp[resp.find("key") + 3:resp.find("var", resp.find("key"))])
            pix = resp[resp.find("pix") + 3:resp.find("var", resp.find("pix"))].split("\"")[-2]
            pvalue = [resp[resp.find("pvalue") + 5:resp.find("var", resp.find("pvalue"))].split("\"")[i] for i in
                      [1, -2]]
            imgUrl = pix + pvalue[0] + "?cid=" + self.cid + "&key=" + key
            r = requests.get(imgUrl, headers=self.__headers, proxies=proxy)
            imgPath = self.downloadDir + "\\" + str(self.currentPage) + ".png"
            imgDir = os.path.dirname(imgPath)
            if not os.path.exists(imgDir):
                os.makedirs(imgDir)
            with open(imgPath, "wb") as f:
                f.write(r.content)
                print "Page " + str(self.currentPage) + " of chapter " + self.cid + " has been downloaded! "
            if pvalue[0] == pvalue[1]:
                break
            else:
                self.currentPage += 1
                time.sleep(sleepTime)