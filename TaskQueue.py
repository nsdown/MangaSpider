from Queue import Queue
from ChapterWork import ChapterWork

class TaskQueue:
    def __init__(self):
        self.__chapterQueue = Queue()
        self.__mergerQueue = Queue()
        return

    def PutIntoMergerQueue(self, chWork):
        self.__mergerQueue.put(chWork)

    def GetMergerWork(self):
        return self.__mergerQueue.get()

    def IsEmpty(self):
        return self.__chapterQueue.empty()

    def PutIntoChapterQueue(self, chwork):
        self.__chapterQueue.put(chwork)
        return

    def GetImageWork(self, chPath):
        return self.__chapterQueue[chPath].get()

    def GetChapterWork(self):
        # TODO this is not the first item, make workPool into workQueue
        return self.__chapterQueue.get()
