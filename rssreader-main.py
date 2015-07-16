import sys
from PyQt4 import uic
from PyQt4.QtGui import *
from PyQt4.QtCore import QUrl,SIGNAL,QThread
from PyQt4.QtWebKit import QWebView
import logging
from threading import Thread
import time
from queue import *
import feedparser
from rssreaderparser import *

#Declaracion de variables

#Call interface
rssreader_main = uic.loadUiType('./rssreader-main.ui')[0]
#Pool of data RSS
pool = Queue()
#List of url RSS
links = []

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s (%(threadName)-2s) %(message)s',
                    )

#Read file and put in list links
def load():
    import csv
    #open file
    with open('rss.csv', newline='') as csvfile:
        #get buffer
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        #get items "url"
        for row in spamreader:
            #put in list "links"
            links.append(row)


'''
    PRODUCERS
'''
#create function worker for get rss
def getRSS(self,link):
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
                    self.cmb_rss.addItem('rssentry')
                    
                    pubdate = entry.published_parsed
            else:
                pool.put(rssentry)
                self.cmb_rss.addItem('rssentry')
                pubdate = entry.published_parsed

# create threads with object
def producers(self,links):
    for link in links:
        worker = Thread(target=getRSS, args=(self,link))
 #       worker.setDaemon(True)
        worker.start()

#Interface Graphics
class RssReaderMain(QMainWindow, rssreader_main):
    d = 0
    def __init__(self,parent=None):
        QMainWindow.__init__(self,parent)
        self.setupUi(self)
        self.process_getrss = ConsumerRSS(self)
        self.initialize_()

    #Initialize Element of GUI
    def initialize_(self):

        self.btn_add.clicked.connect(self.saveLink)

        self.cmb_rss.setCurrentIndex(-1)
        self.cmb_rss.currentIndexChanged['int'].connect(self.chargeHtmlRSS)
        self.connect(self.process_getrss, SIGNAL("event"), self.start_process)

        #Create to WebView
        self.rssweb = QWebView(loadProgress = self.rssweb_progress.setValue, \
                               loadFinished = self.rssweb_progress.hide, \
                               loadStarted = self.rssweb_progress.show, \
                               titleChanged = self.setWindowTitle)
        self.rssweb_progress.hide()
        self.rssweb_container.addWidget(self.rssweb)

        
        self.process_getrss.start()
        load()
        producers(self,links)


    def start_process(self,event):
        print (event)
        self.rss_terminal.append('[Thread' + str(self.d) + ']:' + str(event))
        self.d = self.d + 1
        print(self.d)

    #Save url RSS in file "rss.csv"
    def saveLink(self):
        if str(self.txt_url.text()) is not None:
            with open('rss.csv','a') as csvfile:
                 csvfile.write(str(self.txt_url.text()))
            self.txt_url.setText('')
                
    #Charge Entries of RSS
    def chargeHtmlRSS(self,text):
        print( str(text) )
        self.rssweb.load(QUrl('http://www.google.com'))


'''
    CONSUMERS
'''
class ConsumerRSS(QThread):

    def __init__(self,parent=None):
        QThread.__init__(self,parent)

    #Get Rss of Pool for parcer and show
    def run(self):
        while True:
            if not pool.empty():
               tmp = pool.get()
               self.emit(SIGNAL("event"), tmp) #Emit signal event


if __name__ == '__main__':
    app = QApplication(sys.argv)
    rssreader_main = RssReaderMain()
    rssreader_main.show()
    sys.exit(app.exec_())
