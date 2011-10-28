"""
.. moduleauthor:: Dillon Hicks <harold.hicks@gmail.com>
"""
# Standard Python Library Imports
from datetime import datetime

# 3rd Party Imports
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, DateTime, Column, Integer, \
    String, MetaData, ForeignKey, Unicode, UnicodeText
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# My imports
from chomsky.conf import DATABASE_NAME, DATABASE_HOST, DATABASE_BACKEND

db_connection = '%s:/%s//%s' % \
    (DATABASE_BACKEND, DATABASE_HOST, DATABASE_NAME)

Session = sessionmaker()
engine = create_engine(db_connection)
Session.configure(bind=engine)
session = Session()

# This is kinda funky that a function returns a class but w/e.  To
# future Dillon: Documentation is your friend.
Base = declarative_base()

class Article(Base):
    # Table name in teh database, used by the Base class.
    __tablename__ = 'articles'

    #- Start Article Column Declarations -#
    id = Column(Integer, primary_key=True)
    author = Column(Unicode)
    title = Column(Unicode)
    text = Column(UnicodeText)
    site = Column(Unicode)
    url = Column(Unicode)
    pub = Column(Unicode)
    affiliation = Column(Unicode)
    added = Column(DateTime)
    #- End Article Column Declarations -#

    def __init__(self, author='', title='', text='', 
                 pub='', url='', site='', affiliation=''):

        #- Start Article Auto-Mapping Attributes -# The auto-mapped
        # Attributes should be 1:1 with the column definitions in
        # order for the magic (alchemy) to work.
        self.author = unicode(author, errors='replace')
        self.title = unicode(title, errors='replace')
        self.text = unicode(text, errors='replace')
        # Couldn't bring myself to type published everytime.
        self.pub = unicode(pub, errors='replace')
        self.site = unicode(site, errors='replace')
        self.url = unicode(url, errors='replace')
        # Shorten affiliation, it hurts my eyes.
        self.affiliation = unicode(affiliation, errors='replace')
        self.added = datetime.now()
        #- End Article Auto-Mapping Attributes -#

    def __repr__(self):
        return "<Article('%s', '%s')>" % (self.author, self.title)

    def as_dict(self):
        return {
            'title' : self.title,
            'author' : self.author,
            'affiliation' : self.affiliation,
            'pub' : self.pub,
            'text' : self.text,
            'site' : self.site,
            'url' : self.url,
            'added' : self.added,
            }


def dump(articles, commit_size=10):

    for i, article in enumerate(articles, 1):
        session.add(article)
        # Commit only evey commit_size articles.
        if i % commit_size == 0:
            print 'Commit(%d)' % commit_size
            print
            session.commit()

        yield article
    else:
        # Also commit at the exit of the for loop
        print 'Commit(%d)' % len(session.new)
        session.commit()

# Strange Thing #87453: This needs to be near the bottom of the file
# so that it is called after the Table classes are created. The 'Base'
# class keeps track of all inhertied classes and uses its crazy magic
# to setup the database using the tracked subclasses. KTHXBYE!
Base.metadata.create_all(engine) # Keep me at bottom of declarative code!
