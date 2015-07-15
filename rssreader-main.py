import sys
from PyQt4 import uic
from PyQt4.QtGui import *
from PyQt4.QtCore import QUrl,SIGNAL,QThread
from PyQt4.QtWebKit import QWebView
from rssreader_parser import *
import logging
from threading import Thread
import time
from queue import *
import feedparser
from rssreaderparser import *

#Declaracion de variables
rssreader_main = uic.loadUiType('./rssreader-main.ui')[0]
pool = Queue()
links = []
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s (%(threadName)-2s) %(message)s',
                    )

#load all rss links
def load():
    import csv
    with open('rss.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            links.append(row)


'''
    PRODUCERS
'''
#create function worker for get rss
def getRSS( link):
    pubdate = None
    while True:
        rss = feedparser.parse(link[0])
        entries = rss.entries
        father = RssObject(rss)
        for entry in entries:
            rssentry = RssEntrie(entry, father)
            if pubdate is not None:
                if pubdate > entry.published_parsed:
                    pool.put(rssentry)
                    pubdate = entry.published_parsed
            else:
                pool.put(rssentry)
                pubdate = entry.published_parsed
        print(pool.qsize())

# create threads with object
def producers(links):
    for link in links:
        worker = Thread(target=getRSS, args=(link,))
 #       worker.setDaemon(True)
        worker.start()

'''
    CONSUMERS
'''

class RssReaderMain(QMainWindow, rssreader_main):
    d = 0
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
        print (event)
        self.rss_terminal.append('[Thread1]:' + str(event))
        self.d = self.d + 1
        print(self.d)

#Get Rss of Pool for parcer and show
class ProcessGetRss(QThread):

    def __init__(self,parent=None):
        QThread.__init__(self,parent)

    def run(self):
        while True:
            if not pool.empty():
               tmp = pool.get()
               self.emit(SIGNAL("event"), tmp) #Emit signal event


if __name__ == '__main__':
    app = QApplication(sys.argv)
    rssreader_main = RssReaderMain()
    rssreader_main.show()
    load()
    producers(links)
    sys.exit(app.exec_())
