import os
import requests
import threading
import time, sys


class ImageDownloader(threading.Thread):
    def __init__(self, chDownloader, st):
        threading.Thread.__init__(self)
        self.chDlder = chDownloader
        self.sleepTime = st
        return

    def run(self):
        while True:
            if not self.chDlder.GetImgQueue().empty():
                work = self.chDlder.GetImgQueue().get()
                imgUrl, page = work[0], work[1]
                try:
                    r = requests.get(imgUrl, headers=self.chDlder.GetHeaders(), proxies=self.chDlder.GetProxy())
                    # imgPath = self.chDlder.GetDownloadDir() + "\\" + str(page) + ".png"
                    imgPath = os.path.join(self.chDlder.GetDownloadDir(), str(page)+".png")
                    with open(imgPath, "wb") as f:
                        f.write(r.content)
                    sys.stdout.write(time.asctime(time.localtime(time.time())) + " : " + "Page " + str(
                        page) + " of chapter " + self.chDlder.GetChapterName() + " has been downloaded!\n")
                    self.chDlder.GetImgQueue().task_done()
                    time.sleep(self.sleepTime)
                except:
                    sys.stdout.write(
                        time.asctime(time.localtime(time.time())) + " : thread failed downloading " + imgUrl + "\n")
                    self.chDlder.GetImgQueue().put(work)
                    continue
            else:
                time.sleep(1)
