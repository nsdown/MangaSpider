import os
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import sys
import time


class ImageMerger:
    def __init__(self, TQ):
        self.__chWork = None
        self.__outputDir = None
        self.outputPath = None
        self.tasker = TQ
        return

    def GetWork(self):
        self.__chWork = self.tasker.GetMergerWork()
        self.__outputDir = os.path.abspath(os.path.join(self.__chWork.downloadDir, os.pardir))
        # self.outputPath = self.__outputDir+"\\"+self.__chWork.chName+".pdf"
        self.outputPath = os.path.join(self.__outputDir, self.__chWork.chName+".pdf")

    def Merge(self):
        c = canvas.Canvas(self.outputPath)
        for pn in range(1, len(os.listdir(self.__chWork.downloadDir)) + 1):
            try:
                fn = os.path.join(self.__chWork.downloadDir, str(pn)+".png")
                # fn = self.__chWork.downloadDir+"\\"+str(pn)+".png"
                im = ImageReader(fn)
                imageSize = im.getSize()
                c.setPageSize(imageSize)
                c.drawImage(fn, 0, 0)
                c.showPage()
                sys.stdout.write(time.asctime(time.localtime(time.time()))+" : "+fn+"has been merged into PDF: "+self.outputPath+"\n")
            except:
                # TODO excetion handling
                sys.stdout.write(time.asctime(time.localtime(time.time()))+" : "+"merge failure!\n")
        c.save()
        sys.stdout.write(time.asctime(time.localtime(time.time()))+" : "+self.outputPath+" is done.\n")
        self.tasker.PutIntoPusherQueue(self.__chWork)
        return
