import sys
from PyQt4 import uic
from PyQt4.QtGui import *
from PyQt4.QtCore import QUrl
from PyQt4.QtWebKit import QWebView

rssreader_main = uic.loadUiType('./rssreader-main.ui')[0]
class RssReaderMain(QMainWindow, rssreader_main):
    
    def __init__(self,parent=None):
        QMainWindow.__init__(self,parent)
        self.setupUi(self)
        self.initialize_()

    def initialize_(self):
        self.rssweb = QWebView(loadProgress = self.rssweb_progress.setValue, \
                                              loadFinished = self.rssweb_progress.hide, \
                                              loadStarted = self.rssweb_progress.show, \
                                              titleChanged = self.setWindowTitle)
        #self
        self.rssweb_container.addWidget(self.rssweb)
        self.rssweb.load(QUrl('http://www.google.com'))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    rssreader_main = RssReaderMain()
    rssreader_main.show()
    sys.exit(app.exec_())
