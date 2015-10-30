from Queue import Queue


class TaskQueue:
    def __init__(self):
        self.__chapterQueue = Queue()
        self.__mergerQueue = Queue()
        self.__pusherQueue = Queue()
        return

    def PutIntoPusherQueue(self, chWork):
        self.__pusherQueue.put(chWork)

    def GetPusherWork(self):
        return self.__pusherQueue.get()

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
