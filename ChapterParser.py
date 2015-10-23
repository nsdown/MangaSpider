import requests
from bs4 import BeautifulSoup
import re

class ChapterParser:
    def __init__(self, mangaurl):
        self.url = mangaurl
        self.chDict = {}
        return

    def GetChapterList(self):
        resp = requests.get(self.url)
        soup = BeautifulSoup(resp.content, "html.parser")
        chListCols = soup.find_all("ul", attrs={"class":"nr6 lan2", "id":re.compile("^cbc_\d$")})
        for col in chListCols:
            oneCol = col.find_all("a", attrs={"class":"tg"})
            for ch in oneCol:
                self.chDict[ch.get("href")] = ch.get("title")

    def PrintAllHref(self):
        for a in self.chDict:
            print a, self.chDict[a]