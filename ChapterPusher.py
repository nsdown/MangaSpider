from email.header import Header
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
import smtplib
import os

class ChapterPusher:
    def __init__(self, TQ, stmpServer, fromAddr, toAddr, un, pw):
        self.__stmp = stmpServer
        self.tasker = TQ
        self.__from = fromAddr
        self.__to = toAddr
        self.__un = un
        self.__pw = pw
        self.__chWork = None
        return

    def GetWork(self):
        self.__chWork = self.tasker.GetPusherWork()

    def Work(self):
        filename = self.__chWork.chName+".pdf"
        # filepath = os.path.abspath(os.path.join(self.__chWork.downloadDir, os.pardir))+"\\"+filename
        msg = MIMEMultipart()
        att = MIMEBase('application', "pdf")
        att.set_payload(open(filename, 'rb').read())
        att_header = Header(filename, "utf-8")
        att.add_header('Content-Disposition', 'attachment; filename="%s"' % att_header)
        msg.attach(att)
        msg['to'] = self.__to
        msg['from'] = self.__from
        msg['subject'] = 'manga from mangaspider'
        try:
            server = smtplib.SMTP()
            server.connect(self.__stmp)
            server.login(self.__un,self.__pw)
            server.sendmail(msg['from'], msg['to'],msg.as_string())
            # server.sendmail(msg['from'], msg['to'], 'manga from mangaspider')
            server.quit()
            print "success pushing"
        except Exception, e:
            print str(e)
