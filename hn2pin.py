#!/usr/bin/env python
"""Python-Pinboard

Python script for syncronizing Hacker News <http://news.ycombinator.com> saved stories to Pinboard <http://pinboard.in/> via its API.

Originally written on Pythonista on iPad
"""

__version__ = "1.1"
__license__ = "BSD"
__copyright__ = "Copyright 2013-2014, Luciano Fiandesio"
__author__ = "Luciano Fiandesio <http://fiandes.io/>"

import argparse
import re
import sys
import urllib
import urllib.parse as urlparse
from bs4 import BeautifulSoup
import requests
from types import *
import xml.etree.ElementTree as xml

HACKERNEWS = 'https://news.ycombinator.com'

parser = argparse.ArgumentParser()

parser.add_argument("username", help="The Hacker News username to grab the stories from.")
parser.add_argument("password", help="The password to login with using the username.")
parser.add_argument("filename", help="Filepath to store the JSON document at.")
arguments = parser.parse_args()

def getSavedStories(session, hnuser):
    print("...get saved stories...")
    savedStories = {}
    saved = session.get(HACKERNEWS + '/saved?id=' + hnuser)

    soup = BeautifulSoup(saved.content)

    for tag in soup.findAll('td',attrs={'class':'title'}):

        if type(tag.a) is not type(None):
            try:
                _href = tag.a['href']
                if not str.startswith(str(_href), '/x?fnid'): # skip the 'More' link
                    _href = HACKERNEWS+_href if str.startswith(str(_href), 'item?') else _href
                    savedStories[_href] = tag.a.text
            except:
                print("The saved story has no link, skipping")
    return savedStories

def loginToHackerNews(username, password):
    s = requests.Session() # init a session (use cookies across requests)

    headers = { # we need to specify an header to get the right cookie
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:25.0) Gecko/20100101 Firefox/25.0',
        'Accept' : "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }

    # Build the login POST data and make the login request.
    payload = {
        'whence': 'news',
        'acct': username,
        'pw': password
    }
    auth = s.post(HACKERNEWS+'/login', data=payload, headers=headers )
    if 'Bad login' in str(auth.content):
        raise Exception("Hacker News authentication failed!")
    if not username in str(auth.content):
        raise Exception("Hacker News didn't succeed, username not displayed.")

    return s # return the http session

def main():
    links = getSavedStories( loginToHackerNews(arguments.username,
                                               arguments.password ),
                             arguments.username)
    for key, value in links.items():
        print(key, value)

if __name__ == "__main__":
    main()
