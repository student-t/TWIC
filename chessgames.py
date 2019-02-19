import os
import sys
import urllib
from lxml import html
from urllib.parse import urlsplit
from urllib.parse import parse_qsl
from urllib.request import urlopen
from multiprocessing.dummy import Pool as ThreadPool 

def readGameLinks(url, cur=1):
    links = []
    page = html.fromstring(urlopen(url).read())
    hasNext = False    
    nextURL = None
    for link in page.xpath("//a"):
        if link.get("href") != None:
            if 'chessgame?gid' in link.get("href"):
                parsed = dict(parse_qsl(urlsplit(link.get("href")).query))
                links.append(parsed['gid'])
            elif 'page=' in link.get("href") and hasNext == False:
                page = int(link.get('href').split('page=')[1].split('&')[0])
                if page == cur + 1:
                    hasNext = True
                    nextURL = 'http://www.chessgames.com/' + link.get("href")
    if nextURL is not None:
        links = links + readGameLinks(nextURL, cur=cur+1)    
    return links

def readPGN(url):
    return urlopen(url).read().decode("utf-8")

def readGame(game):
    url = 'http://www.chessgames.com/perl/nph-chesspgn?gid={0}&text=1'.format(game)
    return readPGN(url) + '\n'

# http://www.chessgames.com/perl/chessplayer?pid=24694
toks = sys.argv[1].split('?')

# http://www.chessgames.com/perl/chess.pl?page=1&pid=24694
url = 'http://www.chessgames.com/perl/chess.pl?page=1&' + toks[1]

# Parse all games for the player
games = list(reversed(readGameLinks(url)))

print(''.join([readGame(i) for i in games]))