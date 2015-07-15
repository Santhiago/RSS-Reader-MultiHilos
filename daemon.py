import logging
from threading import Thread
import time
from queue import *
import feedparser
from rssreaderparser import *

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s (%(threadName)-2s) %(message)s',
                    )
pool  = Queue()
links = []

#load all rss links
def load():
    import csv
    with open('rss.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            links.append(row)
load()

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
                print(pubdate > entry.published_parsed)
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

producers(links)
