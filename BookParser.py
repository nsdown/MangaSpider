import requests
from bs4 import BeautifulSoup
import re
from ChapterWork import ChapterWork
import sys


class BookParser:
    def __init__(self, taskQueue, proxy=None):
        self.__url = None
        self.tasker = taskQueue
        self.__proxy = proxy
        return

    def GetWork(self, mangaUrl):
        self.__url = mangaUrl

    def Work(self):
        resp = requests.get(self.__url, proxies = self.__proxy)
        soup = BeautifulSoup(resp.content, "html.parser")
        chListCols = soup.find_all("ul", attrs={"class": "nr6 lan2", "id": re.compile("^cbc_\d$")})
        no = 0
        for col in chListCols:
            oneCol = col.find_all("a", attrs={"class": "tg"})
            for ch in oneCol:
                sys.stdout.write(str(no)+" "+ch.get("href")+" "+ch.get("title")+"\n")
                self.tasker.PutIntoChapterQueue(ChapterWork(no, ch.get("title"), ch.get("href").rstrip("/")))
                no += 1
