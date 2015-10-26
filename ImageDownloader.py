import requests
import threading
import time


class ImageDownloader(threading.Thread):

    def __init__(self, chDownloader, st):
        threading.Thread.__init__(self)
        self.chDlder = chDownloader
        self.sleepTime = st
        return

    def run(self):
        while True:
            try:
                work = self.chDlder.GetImgQueue().get()
                imgUrl, page = work[0], work[1]
                r = requests.get(imgUrl, headers=self.chDlder.GetHeaders(), proxies=self.chDlder.GetProxy())
                imgPath = self.chDlder.GetDownloadDir() + "\\" + str(page) + ".png"
                with open(imgPath, "wb") as f:
                    f.write(r.content)
                print "Page " , str(page) , " of chapter " , self.chDlder.GetChapterName() , " has been downloaded! "
                self.chDlder.GetImgQueue().task_done()
                time.sleep(self.sleepTime)
            except:
                # TODO failed downloading
                return
