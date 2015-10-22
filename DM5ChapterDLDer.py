import requests
import jsbeautifier
import re
import os
import time


class DM5ChapterDLDer:
    def __init__(self, chpath):
        self.baseURL = "http://www.dm5.com"
        self.chPath = chpath
        self.chURL = self.baseURL + self.chPath
        self.chfunBasePath = chpath + "/chapterfun.ashx"
        self.chfunBaseURL = self.chURL + self.chfunBasePath
        self.lang = "1"
        self.gtk = "6"
        self.cid = chpath.split('m')[-1]
        self.headers = {
            "Referer": self.chURL
        }
        return

    def GetChfunURL(self, page):
        return self.chfunBaseURL + "?cid=" + self.cid + "&page=" + str(
            page) + "&key=&language=" + self.lang + "&gtk=" + self.gtk

    def EchoFromChfun(self, sleepTime, proxy=None):
        page = 1
        while True:
            req = requests.get(self.GetChfunURL(page), headers=self.headers, proxies=proxy)
            resp = jsbeautifier.beautify(req.content)
            key = re.sub('[^a-zA-Z\d]', '', resp[resp.find("key") + 3:resp.find("var", resp.find("key"))])
            pix = resp[resp.find("pix") + 3:resp.find("var", resp.find("pix"))].split("\"")[-2]
            pvalue = [resp[resp.find("pvalue") + 5:resp.find("var", resp.find("pvalue"))].split("\"")[i] for i in
                      [1, -2]]
            imgUrl = pix + pvalue[0] + "?cid=" + self.cid + "&key=" + key
            r = requests.get(imgUrl, headers=self.headers, proxies=proxy)
            cwd = os.getcwd()
            imgPath = cwd + "\\" + self.cid + "\\" + str(page) + ".png"
            imgDir = os.path.dirname(imgPath)
            if not os.path.exists(imgDir):
                os.makedirs(imgDir)
            with open(imgPath, "wb") as f:
                f.write(r.content)
                print "Page " + str(page) + " of chapter " + self.cid + " has been downloaded! "
            if pvalue[0] == pvalue[1]:
                break
            else:
                page += 1
                time.sleep(sleepTime)
                