import requests
import threading


class ImageDownloader(threading.Thread):

    def __init__(self, chDownloader):
        threading.Thread.__init__(self)
        self.chDlder = chDownloader
        return

    def run(self):
        while True:
            work = self.chDlder.tasker.GetImageWork(self.chDlder.GetCid())
            imgUrl = work[0]
            page = work[1]
            try:
                r = requests.get(imgUrl, headers=self.chDlder.GetHeaders(), proxies=self.chDlder.GetProxy())
                imgPath = self.chDlder.GetDownloadDir() + "\\" + str(page) + ".png"
                with open(imgPath, "wb") as f:
                    f.write(r.content)
                print "Page " + str(page) + " of chapter " + self.chDlder.GetCid() + " has been downloaded! "
                self.chDlder.GetQueue().task_done()
            except:
                # TODO failed downloading
                return
