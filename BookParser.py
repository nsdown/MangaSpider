import requests
from bs4 import BeautifulSoup
import re


class BookParser:
    def __init__(self):
        self.__url = None
        self.__chList = []
        return

    def GetWork(self, mangaUrl):
        self.__url = mangaUrl

    def GetChapterList(self):
        resp = requests.get(self.__url)
        soup = BeautifulSoup(resp.content, "html.parser")
        chListCols = soup.find_all("ul", attrs={"class": "nr6 lan2", "id": re.compile("^cbc_\d$")})
        no = 0
        for col in chListCols:
            oneCol = col.find_all("a", attrs={"class": "tg"})
            for ch in oneCol:
                self.__chList.append((no, ch.get("href"), ch.get("title")))
                no += 1
        return self.__chList

    def PrintAllHref(self):
        for a in self.__chList:
            print a[0], a[1], a[2]
