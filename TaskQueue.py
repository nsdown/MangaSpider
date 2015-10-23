from Queue import Queue

class TaskQueue:
    def __init__(self):
        # storing images to download
        self.WorkQueue = Queue()
        # storing images downloaded & wait to be merged
        self.DoneQueue = Queue()
        # storing images failed downloading
        self.ExceptionQueue = Queue()
        return

    def putIntoWorkQueue(self, workList):
        for work in workList:
            self.WorkQueue.put(work)
        return

    def putIntoDoneQueue(self, doneWorkList):
        for doneWork in doneWorkList:
            self.DoneQueue.put(doneWork)
        return

    def putIntoExceptionQueue(self, undoneWorkList):
        for undoneWork in undoneWorkList:
            self.ExceptionQueue.put(undoneWork)
        return

    def getWork(self):
        return self.WorkQueue.get()

    def getUndoneWork(self):
        return self.ExceptionQueue.get()