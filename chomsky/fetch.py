#!/usr/bin/env python
"""
TODOS
------

- Finish the specifications for the database in db.py. Probably just
  sqlite3 rigtht now... unless it gets hugemongous (possible).

- Check if url has already been fetched in the DB so we can check
  multiple times per day and not have dupes. Also this will prevent
  dupes in the case of interrupted fetching.

"""

from pprint import pprint
import sys
import os
import urllib2 as urllib
from datetime import datetime
import tarfile

import feedparser

from chomsky import conf
from chomsky import db

db_query = db.session.query(db.Article)


def make_rss_urls(sites):
    for site, data in sites.items():
        print 'Site:', site
        print
        prefix = data['feed_prefix']
        for feed in data['feeds']:
            url = prefix + feed
            yield (site, url)

def make_article_urls(urls):
    for site, url in urls:
        feeds = feedparser.parse(url)
        for article in feeds['entries']:
            yield (site, article['link'])
            
def fetch_html(urls):
    for (site, url) in urls:
        tries = 0
        while tries <= conf.MAX_FETCH_RETRIES:
            tries += 1
            try:
                connection = urllib.urlopen(url, timeout=conf.FETCH_TIMEOUT)
            except urllib.URLError:
                print 'Connection Timeout(%s): %s' % (tries, url)
                print
                continue # while ties 
            
            break # out of while tries
        else:
            print 'Error: MAX_FETCH_RETRIES exceeded, skipping', url
            print
            continue # for (site, url)

        redirected_url = connection.geturl() 
        
        query_result = db_query.filter_by(url=unicode(redirected_url))

        if query_result.count():
            print 'Skipped:', redirected_url
            print 'Reason: In Database'
            print
            connection.close()
            continue

        print 'Fetching:', redirected_url
        print            
            
        html = connection.read()
        connection.close()
        # TODO: Check redirected_url against urls of articles in DB.
        # if exists skip via "continue"
        
        yield site, redirected_url, html

def save_articles(articles):
    for i, (site, url, article) in enumerate(articles, 1):
        filename = os.path.join(
            conf.DATA_PATH, '%s_article_%d.html' % (site, i))
        with open(filename, 'w') as htmlfile:
            print >> htmlfile, url
            print >> htmlfile, article
        yield filename

def tar_saved_files(filepaths):
    now = datetime.now()
    
    tarball = os.path.join(
        conf.DATA_PATH, 
        '%s-%s_articles.tar' % (now.date(), now.time()))
    
    original_dir = os.getcwd()
    os.chdir(conf.DATA_PATH)

    tf = tarfile.open(tarball, 'w')
    for i, filepath in enumerate(filepaths, 1):
        path, filename = os.path.split(filepath)
        print filename, '>>', tarball
        print 
        tf.add(filename)
        yield filepath
    tf.close()
    os.chdir(original_dir)

def cleanup_uncompressed_files(filenames):
    for filename in filenames:
        os.remove(filename)
        

