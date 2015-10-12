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
import json
from bs4 import BeautifulSoup
import requests
from types import *
import xml.etree.ElementTree as xml

HACKERNEWS = 'https://news.ycombinator.com'

parser = argparse.ArgumentParser()

parser.add_argument("username", help="The Hacker News username to grab the stories from.")
parser.add_argument("password", help="The password to login with using the username.")
parser.add_argument("-f", "--file", help="Filepath to store the JSON document at.")
parser.add_argument("-n", "--number", default=1, type=int, help="Number of pages to grab, default 1.")

arguments = parser.parse_args()

def getSavedStories(session, hnuser, page_range):
    story_ids = []
    for page_index in page_range:
        saved = session.get(HACKERNEWS + '/saved?id=' + 
                            hnuser + "&p=" + str(page_index))
        soup = BeautifulSoup(saved.content)
        for tag in soup.findAll('td',attrs={'class':'subtext'}):
            if tag.a is not type(None):
                a_tags = tag.find_all('a')
                for a_tag in a_tags:
                    if a_tag['href'][:5] == 'item?':
                        story_id = a_tag['href'].split('id=')[1]
                        story_ids.append(story_id)
                        break
    return story_ids

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

def getHackerNewsItem(item_id):
    """Get an 'item' as specified in the HackerNews v0 API."""
    item_json_link = "https://hacker-news.firebaseio.com/v0/item/" + item_id + ".json"
    try:
        with urllib.request.urlopen(item_json_link) as item_json:
            return json.loads(item_json.read().decode('utf-8'))
    except urllib.error.URLError:
        return {"title":"Item " + item_id + " could not be retrieved",
                "id":item_id}

def main():
    json_items = {"saved_stories":list(), "saved_comments":list()}
    story_ids = getSavedStories( loginToHackerNews(arguments.username,
                                               arguments.password ),
                             arguments.username, range(1, arguments.number + 1))
    for story_id in story_ids:
        json_items["saved_stories"].append(getHackerNewsItem(story_id))
        sys.stderr.write("Got item " + story_id + ".\n")
    if arguments.file:
        with open(arguments.file, 'w') as outfile:
            json.dump(json_items, outfile)
    else:
        print(json.dumps(json_items))

if __name__ == "__main__":
    main()
