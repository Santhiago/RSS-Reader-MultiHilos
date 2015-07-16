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
            self.rss = args[0]

    def getFeed(self):
        title = self.rss.feed.title
        link = self.rss.feed.link
        description = self.rss.feed.description
        published = self.rss.feed.published
        published_parsed = self.rss.feed.published_parsed
        feed = 'title: ' + title + '\nlink: ' + link + '\ndescription: ' + \
                description + '\npublished: ' + published
        return feed


class RssEntrie():
    entry = ''
    father = ''

    def __init__(self, entry, father):
        self.entry = entry
        self.father = father
        self.getData()

    def getData(self):
        self.title = self.entry.title
        self.link = self.entry.link
        self.links = self.entry.links
        self.href = self.entry.href
        self.media_content = self.entry.media_content
        self.description = self.entry.description
        self.id = self.entry.id

    def getHtml(self):
        style = ''
        print(self.media_content)
        print(self.media_content[0]['url'])
        div = '<li><div class="timeline-image">\
                <img class="img-circle img-responsive"\
                src="' + self.media_content[0]['url'] + '"></div>'
        div = div +'<div class="timeline-panel"><div class="timeline-heading">\
                ' + self.title + '</div>'
        div = div + '<div class="timeline-body"><p class="text-muted">\
                ' + self.description
        div = div + '<br/><a href="'+ self.href+'"></p></div></div>'
        div = div + '</li>'
        return div



