"""
"""
import sys
import re
from glob import glob

import yaml

from chomsky import db
from chomsky.db import Article

article_rx = re.compile(
    r"""
    <!--startclickprintinclude-->(.+)<!--endclickprintinclude-->
    """, re.VERBOSE | re.DOTALL)

# Group number of the title_rx where the actual title text is found
# wihtout the stupid html tags.
TITLE_GROUP = 2
title_rx = re.compile(r'<h1( .*?)?>(.+)</h1>')

clean_rx = re.compile(
    r"""
    (<!--startclickprintexclude-->(.+)<!--endclickprintexclude-->) |
    (<[/]?.+?>)
    """,
    re.DOTALL | re.VERBOSE)

quote_rx = re.compile(r'[&]quot[;]')

PUB_GROUP = 1
pub_rx = re.compile(r"var cnnFirstPub = new Date[(]'([A-Za-z0-9: ]+)'[)];")

AUTHOR_GROUP = 1
author_rx = re.compile(r"name=\"AUTHOR\" content=\"(.*?)\"", re.IGNORECASE)

def _parse_url(html):
    first_line, _ = html.split('\n', 1)
    if first_line.startswith('http://'):
        url = first_line
    else:
        url = ''
    return url

def _parse_published(html):
    match = pub_rx.search(html)
    published = match.group(PUB_GROUP) if match else ''
    return published

def _parse_author(html):
    match = author_rx.search(html)
    author = match.group(AUTHOR_GROUP) if match else ''

    if author.lower().startswith('by'):
        author = author[3:].strip()
    elif author.lower().startswith('from'):
        author = author[4:].strip()
    
    if ',' in author:
        author, affiliation = author.rsplit(',', 1)
    else:
        affiliation = ''    
    return author, affiliation

def _parse_text(html):
    title = ''
    text = ''
    result = article_rx.search(html)    
    if result:
        raw_article = result.group()
        title_match = title_rx.search(raw_article)
        title = title_match.group(TITLE_GROUP)
        raw_article = title_rx.sub('', raw_article)
        clean_text = clean_rx.sub('', raw_article)
        text = quote_rx.sub('\"', clean_text).strip()
    return title, text

def parse_articles(html_files):

    for html_file in html_files:

        print 'Parsing:', html_file
        print 

        with open(html_file, 'r') as infile: 
            html = infile.read()

        url = _parse_url(html)

        published = _parse_published(html)
        
        author, affiliation = _parse_author(html)

        title, text = _parse_text(html)
 
        article = Article(author=author, title=title, pub=published,
                     affiliation=affiliation, text=text, url=url)
     
        yield article

