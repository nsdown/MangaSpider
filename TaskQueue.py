from Queue import Queue


class TaskQueue:
    def __init__(self):
        self.__workPool = {}
        return

    def IsEmpty(self):
        return len(self.__workPool) == 0

    def GetQueueOfChapter(self, chPath):
        return self.__workPool[chPath]

    def PutIntoChapterQueue(self, chPath):
        self.__workPool[chPath] = Queue()
        return

    def PutIntoImageWorkQueue(self, chPath, imgWork):
        # imgwork structure: (imgurl, page)
        self.__workPool[chPath].put(imgWork)
        return

    def GetImageWork(self, chPath):
        return self.__workPool[chPath].get()

    def PopOutChapter(self, chPath):
        del self.__workPool[chPath]
        return

    def GetFirstChapter(self):
        # TODO this is not the first item, make workPool into workQueue
        return self.__workPool.items()[0]
