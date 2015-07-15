import sys
from PyQt4 import uic
from PyQt4.QtGui import *
from PyQt4.QtCore import QUrl,SIGNAL,QThread
from PyQt4.QtWebKit import QWebView
from rssreader_parser import * 

rssreader_main = uic.loadUiType('./rssreader-main.ui')[0]
import Queue
pool = Queue.Queue()
class RssReaderMain(QMainWindow, rssreader_main):
    
    def __init__(self,parent=None):
        QMainWindow.__init__(self,parent)
        self.setupUi(self)
        self.process_getrss = ProcessGetRss(self)
        self.initialize_()
        
    #Initialize Element of GUI
    def initialize_(self):

        #Temporally Put 'Manual' in pool(queue) rss object
        self.rss = RssObject(url)
        self.rss = self.rss.getFeed
        pool.put(self.rss)



        self.rssweb = QWebView(loadProgress = self.rssweb_progress.setValue, \
                               loadFinished = self.rssweb_progress.hide, \
                               loadStarted = self.rssweb_progress.show, \
                               titleChanged = self.setWindowTitle)

        self.rssweb_container.addWidget(self.rssweb)
        self.rssweb.load(QUrl('http://www.google.com'))
              
        self.connect(self.process_getrss, SIGNAL("event"), self.start_process)
        self.process_getrss.start()


    def start_process(self,event):
        print event
        self.rss_terminal.append('[Thread1]:' + str(event))
        
#Get Rss of Pool for parcer and show
class ProcessGetRss(QThread):

    def __init__(self,parent=None):
        QThread.__init__(self,parent)

    def run(self):
        #for i in range(5):
        #    self.emit(SIGNAL("event"), str(i)) #Emit signal event
        #    self.sleep(2) #Simulation temporally
        while True:
            if not pool.empty():
               tmp = pool.get()
               self.emit(SIGNAL("event"), tmp) #Emit signal event
   


if __name__ == '__main__':
    app = QApplication(sys.argv)
    rssreader_main = RssReaderMain()
    rssreader_main.show()
    sys.exit(app.exec_())
