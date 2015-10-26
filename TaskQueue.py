from Queue import Queue


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

    def GetChapterWork(self):
        return self.__chapterQueue.get()
