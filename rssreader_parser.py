import feedparser
url = 'http://rss.cnn.com/rss/edition.rss'
#feedparser http://pythonhosted.org/feedparser/common-rss-elements.html
#https://github.com/kurtmckee/feedparser

class RssObject():
    url = ''
    rss = ''
    isUpdate = False
    entries = []

    def __init__(self,*args,**Kwargs):
        if not args[0] is None:
            self.url = args[0]
            self.updateRss()

    def updateRss(self):
        self.rss = feedparser.parse( self.url )
        self.isUpdate = True

    def getFeed(self):
        if self.isUpdate:
            title = self.rss.feed.title
            link = self.rss.feed.link
            description = self.rss.feed.description
            published = self.rss.feed.published
            published_parsed = self.rss.feed.published_parsed

            feed = 'title: ' + title + '\nlink: ' + link + '\ndescription: ' + \
                   description + '\npublished: ' + published

            print(feed)
            return self.rss

    def getEntries(self):
        for entrie in self.rss.entries:
            rssentrie = RssEntrie(entrie)
            self.entries.append(rssentrie)



class RssEntrie():
    entrie = ''

    def __init__(self, entrie):
        self.entrie = entrie

    def getData(self):
        self.title = self.entrie.title
        self.link = self.entrie.link
        self.links = self.entrie.links
        self.href = self.entrie.href
        self.media_content = self.entrie.media_content
        self.description = self.entrie.description
        self.id = self.entrie.id

#cnn = RssObject(url)
#cnn.getFeed()

