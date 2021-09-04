#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 _     _
# | |__ (_)_ __   __ _ _ __   ___  _ __ _ __
# | '_ \| | '_ \ / _` | '_ \ / _ \| '__| '_ \
# | |_) | | | | | (_| | |_) | (_) | |  | | | |
# |_.__/|_|_| |_|\__, | .__/ \___/|_|  |_| |_|
#                |___/|_|
ay@no-ma..me 20201125 073526 -0800 PST 1606318526 d(-_- )b...

"""
from contextlib import closing
import sys
import random
import json
import time
import youtube_dl

from cachetools import cached, LRUCache
from requests import post
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from logzero import logger as log
import logzero

ytdllog = logzero.setup_logger(
    name="ytdllog", level=logzero.INFO, disableStderrLogger=True
)


# Blacklisted sites, these sites "work" with youtube_dl, but don't work for us
blacklist = [
    "porndig.com",
    "dailymotion.com",
    "facebook.com",
    "rexxx.org",
    "xxxbunker.com",
    "tukif.com",
    "txxx.com",
    "instagram.com",
    "spankbang.com",
    "tiktok.com",
    "vimeo.com",
    "youtube.com",
]


class MyLogger(object):
    def debug(self, msg):
        ytdllog.debug(msg)

    def warning(self, msg):
        ytdllog.warning(msg)

    def error(self, msg):
        log.error(msg)


# initialize ydl
ydl = youtube_dl.YoutubeDL(
    {
        "format": "([protocol=https]/[protocol=http])[ext=mp4]",
        "ignoreerrors": True,
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True,
        "sleep-interval": 1,
        "max-sleeo-interval": 5,
        "user-agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36,gzip(gfe)",
        "logger": MyLogger(),
    }
)


class PornException(Exception):
    """shit! no porn!"""

    ...


def url_generator(linklist):
    """
    Generator object thatWill spit out valid urls on stdout that you
    can have mpd or vlc swallow

    Args:
        linklist (List): Its a list. of links. what did you expect?
    Yields:
        stream (Generator) A generator for spewing filthy urls all over
    """
    for link in linklist:
        try:
            stream = getstream(link)
            if stream:
                yield stream
            else:
                continue
        except PornException:
            ...
        #  sys.stderr.writeline(err)


def get_direct_link(search, results=105, length=0):
    """See pore porn, see no ads, usin the best search porn enine, Bing!"""

    length_param = ""

    if length and int(length) >= 20:
        length_param = "+filterui:duration-long"

    srch = "https://www.bing.com/videos/asyncv2"
    srch += '?q="{}" AND NOT (site:{})'
    srch += "&async=content"
    srch += "&first=0&count={}&qft={}"
    blklst = " OR site:".join(blacklist)

    search_url = srch.format(search.lower(), blklst, results, length_param)

    # get request for search page, create parser
    html = BeautifulSoup(simple_get(search_url), "html.parser")

    # Extract links to video pages from search results
    narrowed_html = html.find_all(class_="vrhdata")
    link_list = []
    for n_html in narrowed_html:
        link_list.append(json.loads(n_html["vrhm"])["pgurl"])

    random.shuffle(link_list)
    #    log.info("link_list: %s ", link_list)

    return url_generator(link_list[0:5])


# Boilerplate requests stuff
def simple_get(url):
    cookiecontent = "ADLT=OFF&CW=1117&CH=1771&DPR=2&UTC=-360&HV={}"
    cookie = {"SRCHHPGUSR": cookiecontent.format(str(int(time.time())))}

    try:
        with closing(post(url, cookies=cookie)) as resp:
            if resp.ok and "html" in resp.headers["Content-Type"]:
                return resp.content
            return None
    except RequestException as err:
        return None


@cached(cache=LRUCache(maxsize=1024))
def getstream(link):
    try:
        log.info("sleeping 5")
        time.sleep(5)
        return ydl.extract_info(link, download=False).get("url", None)
    except AttributeError:
        ...


if __name__ == "__main__":
    ...
