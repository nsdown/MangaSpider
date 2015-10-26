import os
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader


class ImageMerger:
    def __init__(self, TQ):
        self.__imageDir = None
        self.__outputDir = None
        self.__outputFilename = None
        self.__totalPages = None
        self.outputPath = None
        self.tasker = TQ
        return

    def GetWork(self):
        imgDir, outputFn = self.tasker.GetMergerWork()
        self.__imageDir = imgDir
        self.__outputDir = os.path.abspath(os.path.join(self.__imageDir, os.pardir))
        self.__outputFilename = outputFn
        self.__totalPages = len(os.listdir(imgDir))
        self.outputPath = self.__outputDir+"\\"+self.__outputFilename+".pdf"

    def Merge(self):
        c = canvas.Canvas(self.outputPath)
        for pn in range(1, self.__totalPages+1):
            try:
                fn = self.__imageDir+"\\"+str(pn)+".png"
                im = ImageReader(fn)
                imageSize = im.getSize()
                c.setPageSize(imageSize)
                c.drawImage(fn, 0, 0)
                c.showPage()
                print fn, " has been merged into PDF: ", self.outputPath
            except:
                print "merge failure!"
        c.save()
        print self.outputPath, " has been finished! "
        return
