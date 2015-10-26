from Queue import Queue

class TaskQueue:
    def __init__(self):
        self.workPool = {}
        return

    def PutIntoChapterQueue(self, chCid):
        self.workPool[chCid] = Queue()
        return

    def PutIntoImageWorkQueue(self,chCid, imgWork):
        # imgwork structure: (imgurl, page)
        self.workPool[chCid].put(imgWork)
        return

    def GetImageWork(self, chCid):
        return self.workPool[chCid].get()