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
import json
import time
import youtube_dl
import fire

from cachetools import cached, LRUCache
from requests import post
from requests.exceptions import RequestException
from bs4 import BeautifulSoup


# Blacklisted sites, these sites "work" with youtube_dl, but don't work for us
blacklist = ["spankbang.com", "youtube.com", "xhamster.com"]

# initialize ydl
ydl = youtube_dl.YoutubeDL(
    {
        "format": "([protocol=https]/[protocol=http])[ext=mp4]",
        "ignoreerrors": True,
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True,
    }
)


class PornException(Exception):
    """shit! no porn!"""

    ...


def url_generator(linklist):
    """
    Will spit out valid urls on stdout that you can have mpd or vlc swallow
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
        except PornException as err:
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

    return url_generator(link_list)


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
        ydl.extract_info(link, download=False).get("url", None)
    except AttributeError:
        ...


def direct_vid_link(query, results=105, length=20):
    """So you want to see some porn eh?-

    Args:
        query (String): Your guilty pleasure, quoted e.g: "Emma Mae"
        results (TYPE, optional): DESCRIPTION. Defaults to 105.
        length (TYPE, optional): DESCRIPTION. Defaults to 20.

    Returns:
        None.

    this function is tied
    to fire.,Fire() which makes this function it's bitch and
    turns its arguments into positional. mandatory arguments for
    the bingporn command. keyword arguments are treated as option
    flags, since they are, well, optional. (havin a default value
    does that to ya. Also: when the docstring of a function is 6
    times longer than the function itself, do you really need that
    function? turns out most of the times, no. but in this case what
    i need to do is stop smoking that shit and watch some porn."""

    for link in get_direct_link(query, results=results, length=length):
        print(link)


if __name__ == "__main__":
    fire.Fire(direct_vid_link)
