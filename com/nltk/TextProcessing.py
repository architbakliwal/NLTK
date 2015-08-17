'''
Created on Aug 12, 2015

@author: n553721
'''

from urllib import request

from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import feedparser
from nltk import word_tokenize
import nltk, re , pprint


llog = feedparser.parse("http://www.moneycontrol.com/rss/marketreports.xml")
# print(len(llog.entries))
post_titles = []
post_link = []
for post in llog.entries:
#     print(post.title)
    post_titles.append(post.title)
    post_link.append(post.id)

only_body_tags = SoupStrainer("body")
html_doc = request.urlopen(post_link[0]).read()
soup = BeautifulSoup(html_doc, 'html.parser', parse_only=only_body_tags)
print(soup.prettify())
