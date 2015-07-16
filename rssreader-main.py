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
#Pool of data producer-consumer RSS
pool = Queue()
#Poll of data for show. Use only in consumer
pool_cmb = []
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
def getRSS(self,link,position):
    pubdate = None
    while True:
        rss = feedparser.parse(link[0]) #Get data and parse
        entries = rss.entries #Get Entries from RSS
        father = RssObject(rss) #Create a RssObject

        for entry in entries:
            rssentry = RssEntrie(entry, father) #Create RssEntrie
            
            #Only Put in queue feeds News
            if pubdate is not None:
                if pubdate > entry.published_parsed:
                    pool.put(rssentry)
                     
                    pubdate = entry.published_parsed
            else:
                pool.put(rssentry)
                pubdate = entry.published_parsed

        self.printprocess(position,'Finished')

#Create threads with object
def producers(self,links):
    #Get url from links
    i=1
    self.cmb_rss.clear()
    pool_cmb=[]

    for link in links:
        
        worker = Thread(target=getRSS, args=(self,link,i)) #Create a Thread for each url
        #worker.setDaemon(True)
        worker.start() #Start Thread
        self.printprocess(i,'Start')
        i +=1

'''
    CONSUMERS
'''
#Interface Graphics
class RssReaderMain(QMainWindow, rssreader_main):
    div = ''
    html = ''
    div_end = '</ul></div></div></div><script\
            type="text/javascript"></script></body></html>'
    with open('style.html','r') as style:
        div = style.read()
    html = div

    def __init__(self,parent=None):
        QMainWindow.__init__(self,parent)
        self.setupUi(self)
        self.process_getrss = ConsumerRSS(self)
        self.initialize_()


    #Initialize Element of GUI
    def initialize_(self):
        
        #Fill combobox with rss links (links list)
        i = 0
        
        '''
        for link in links:
            i = i + 1
            self.cmb_rss.addItem(link[0],i)
        '''

        #Button Add: call function saveLink()
        self.btn_add.clicked.connect(self.saveLink)
        #Set ComboBox Index to' -1'
        self.cmb_rss.setCurrentIndex(-1)
        #Put signal to ComboBox Changed Index
        self.cmb_rss.currentIndexChanged['int'].connect(self.chargeHtmlRSS)
        #Put signal for add item in ComboBox
        self.connect(self.process_getrss, SIGNAL("event"), self.addItem)

        #Create to WebView
        self.rssweb = QWebView(loadProgress = self.rssweb_progress.setValue, \
                               loadFinished = self.rssweb_progress.hide, \
                               loadStarted = self.rssweb_progress.show, \
                               titleChanged = self.setWindowTitle)
        self.rssweb_progress.hide()
        #Add WebView to Widget container
        self.rssweb_container.addWidget(self.rssweb)

        
        producers(self,links) #Start Producer
        self.process_getrss.start() #Start Comsumer


    #Print process. How start and finish a Thread Producer
    def printprocess(self,thread,status):
        self.rss_terminal.append('[Thread' + str(thread) + ']:' + str(status))
        #a = logging.debug('[Thread' + str(thread) + ']:' + str(status))
        #print(a)
        #self.rssweb.setHtml(event.getHtml())

    def addItem(self,title):
        self.cmb_rss.addItem(str(title))

    #Save url RSS in file "rss.csv"
    def saveLink(self):
        if str(self.txt_url.text()) is not None:
            with open('rss.csv','a') as csvfile:
                 csvfile.write(str(self.txt_url.text()))
            self.txt_url.setText('')
            load()
            producers(self,links)
                
    #Charge Entries of RSS
    def chargeHtmlRSS(self,position):
        html_feed = ''
        html_feed = pool_cmb[position].getHtml()
       
        #url = self.cmb_rss.itemData(int(text))

        self.rssweb.setHtml(html_feed)


'''
    CONSUMERS
'''
#Get Rss of Pool for parser and show
class ConsumerRSS(QThread):

    def __init__(self,parent=None):
        QThread.__init__(self,parent)

    #Get Rss of Pool for parcer and show
    def run(self):
        while True:
            #Get object only when a queue not empty
            if not pool.empty():
               tmp = pool.get()
               pool_cmb.append(tmp)
               #print(len(pool_cmb))
               self.emit(SIGNAL("event"), tmp.title) #Emit signal event


if __name__ == '__main__':
    load() #Start read file
    app = QApplication(sys.argv) #Create application
    rssreader_main = RssReaderMain() #Create GUI
    rssreader_main.show() #Show GUI
    sys.exit(app.exec_()) #Destroy all to finish
