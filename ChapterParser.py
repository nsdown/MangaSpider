import requests
from bs4 import BeautifulSoup
import re

class ChapterParser:
    def __init__(self, mangaurl):
        self.__url = mangaurl
        self.chList = []
        return

    def GetChapterList(self):
        resp = requests.get(self.__url)
        soup = BeautifulSoup(resp.content, "html.parser")
        chListCols = soup.find_all("ul", attrs={"class":"nr6 lan2", "id":re.compile("^cbc_\d$")})
        no = 0
        for col in chListCols:
            oneCol = col.find_all("a", attrs={"class":"tg"})
            for ch in oneCol:
                self.chList.append((no, ch.get("href"), ch.get("title")))
                no+=1

    def PrintAllHref(self):
        for a in self.chList:
            print a[0], a[1], a[2]