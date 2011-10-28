import os

sites = {
    'cnn' : {
        'feed_prefix' : 'http://rss.cnn.com/rss/',
        'feeds' : (
            'cnn_topstories.rss',
            'cnn_world.rss',
            'cnn_us.rss',
            'money_latest.rss',
            'cnn_allpolitics.rss',
            'cnn_crime.rss',
            'cnn_tech.rss',
            'cnn_health.rss',
            'cnn_showbiz.rss',
            'cnn_travel.rss',
            'cnn_living.rss',
            'cnn_studentnews.rss',
            'cnn_mostpopular.rss',
            )
        }, # cnn

    'fox' : {
        'feed_prefix' : 'http://feeds.foxnews.com/foxnews/',
        'feeds' : (
            'latest',
            'national',
            'world',
            'politics',
            'business',
            'scitech',
            'health',
            'entertainment',
            )
        }, # fox

    'msnbc' : {
        'feed_prefix' : 'http://rss.msnbc.msn.com/id/',
        'feeds' : (
            '3032091/device/rss/rss.xml', # Headlines
            '3032524/device/rss/rss.xml', # US news
            '3032506/device/rss/rss.xml', # World news
            '3032552/device/rss/rss.xml', # Politics
            '3032071/device/rss/rss.xml', # Business
            '3032083/device/rss/rss.xml', # Entertainment
            '3088327/device/rss/rss.xml', # Health
            '3032117/device/rss/rss.xml', # Tech & Science
            )
        }, # msnbc
    'reuters' : {
        'feed_prefix' : 'http://feeds.reuters.com/reuters/',
        'feeds' : (
            'artNews',
            'companyNews',
            'entertainment',
            'environment',
            'healthNews',
            'worldNews',
            'InternetNews',
            'lifestyle',
            'mediaNews',
            'MostRead',
            'musicNews',
            'oddlyEnoughNews',
            'politicsNews',
            'scienceNews',
            'technologyNews',
            'topNews',
            'domesticNews',
            )
        }, # reuters

    } # sites  

#- Start Misc Settings -#
MAX_FETCH_RETRIES = 5
FETCH_TIMEOUT = 10 # seconds
DATA_PATH = '/home/hhicks/Desktop/chomsky/data/'

#- End Misc Settings -#


#- Start Database Conf -#

# Path for sqlite
DATABASE_NAME = os.path.join(DATA_PATH, 'lexikon.db') 
DATABASE_BACKEND = 'sqlite'   # sqlite, mysql, etc. 
DATABASE_HOST = ''           # Empty string means localhost
DATABASE_USER = ''           # Notused for sqlite
DATABASE_PASSWORD = ''       # Not used for sqlite

#- End  Database Conf -#
