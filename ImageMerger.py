import os
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader


class ImageMerger:
    def __init__(self, DLDer):
        self.__imageDir = DLDer.downloadDir
        self.__outputDir = os.path.abspath(os.path.join(self.__imageDir, os.pardir))
        self.__outputFilename = DLDer.cid+'.pdf'
        self.__totalPages = DLDer.currentPage
        self.outputPath = self.__outputDir+"\\"+self.__outputFilename
        return

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
        print self.outputPath, " has is finished! "
        return
