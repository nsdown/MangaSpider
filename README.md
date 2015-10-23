# MangaSpider
Scrape manga from dm5.com and print downloaded images into PDF file so you can read on kindle

## How to use
here's an example:

import DM5ChapterDLDer as ChDLDer
import ImageMerger as IMGer
reqProxy = {
    "http": "http://127.0.0.1:1234",
    "https": "http://127.0.0.1:1234"
}
ChapterPath = "/m224188"
sleeptimeBetweenDownloading = 0
dlder = ChDLDer.DM5ChapterDLDer(ChapterPath)
dlder.EchoFromChfun(sleeptimeBetweenDownloading)
# if u need to use proxy
# ins.EchoFromChfun(sleeptimeBetweenDownloading, reqProxy)
im = IMGer.ImageMerger(dlder)
im.Merge()
