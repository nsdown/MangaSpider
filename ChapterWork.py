from Queue import Queue
import os


class ChapterWork:
    def __init__(self, no, chName, chPath):
        self.chName = chName
        self.chPath = chPath
        self.no = no
        self.imgQueue = Queue()
        cwd = os.getcwd()
        self.downloadDir = cwd + "\\" + self.chPath.split('m')[-1]
        self.outputDir = os.path.abspath(os.path.join(self.downloadDir, os.pardir))

    def PutIntoImgQueue(self, imgWork):
        # imgwork structure: (imgurl, page)
        self.imgQueue.put(imgWork)
        return