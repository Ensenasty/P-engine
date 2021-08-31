#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
#  _     _
# | |__ (_)_ __   __ _ _ __   ___  _ __ _ __
# | '_ \| | '_ \ / _` | '_ \ / _ \| '__| '_
# | |_) | | | | | (_| | |_) | (_) | |  | | | |
# |_.__/|_|_| |_|\__, | .__/ \___/|_|  |_| |_|
#                |___/|_|
ay@no-ma..me 20201125 073526 -0800 PST 1606318526 d(-_- )b...

"""
from contextlib import closing

import os.path
import sys
import json
import time
import youtube_dl
import fire

from requests import post
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from logzero import logger as log


class PornError(Exception):
    """shit! no porn!"""

    ...


class BingPorn:
    """Get your porn from the best porn search engine on the internet: bing"""

    def __init__(self, verbose=False):
        self._verbose = verbose
        self._blacklist = [
            "archive.org",
            "dailymotion.com",
            "facebook.com",
            "instagram.com",
            "spankbang.com",
            "tiktok.com",
            "vimeo.com",
            "xhamster.com",
            "youtube.com",
        ]  # no good porn here
        self._ydl = youtube_dl.YoutubeDL(
            {
                "format": "([protocol=https]/[protocol=http])[ext=mp4]",
                "ignoreerrors": True,
                "quiet": True,
                "no_warnings": True,
                "noplaylist": True,
                "call_home": False,
            }
        )
        self._link = ""
        self._link_list = ""
        self._url = ""

    def _url_generator(self):
        """
        Will spit out valid urls on stdout that you can have mpd or vlc swallow

        Yields:
            stream (Generator) A generator for spewing filthy urls all over
        """
        for self._link in self._link_list:
            try:
                stream = self._ydl.extract_info(self._link, download=False).get(
                    "url", None
                )
            except PornError as err:
                if self._verbose:
                    log.error("error %s" % err)
                stream = None
            except AttributeError as err:
                if self._verbose:
                    log.error("error %s" % err)
                stream = None
            if stream:
                yield stream

    def _get_search_results(self):
        """Generator, will return the next porn-spewing directly streamable
        link available after performing an async bing search

        Args:
            self: the instance data
            search: a query string
            count: desired result count 105 is optimal
            duration: porn minutes to watch per video
        """

        if self._verbose:
            log.debug("-----")
            log.debug("get_direct_link(self, search):")
            log.debug('query="%s"', self.query)
            log.debug('count="%s"', self.count)
            log.debug('duration="%s"', self.duration)
            log.debug('self._blacklist="%s"', self._blacklist)
            log.debug('self._url="%s"', self._url)

        if int(self.duration) >= 20:
            dur = "+filterui:duration-long"
        else:
            dur = ""

        blklst = " OR site:".join(self._blacklist)
        srch = "https://www.bing.com/videos/asyncv2"
        srch += f'?q="{self.query}" AND NOT (site:{blklst})'
        srch += "&async=content"
        srch += f"&first=0&count={self.count}&qft={dur}"

        html = BeautifulSoup(self._simple_get(srch), "html.parser")

        narrowed_html = html.find_all(class_="vrhdata")
        for n_html in narrowed_html:
            if self._verbose:
                log.debug(json.loads(n_html["vrhm"])["pgurl"])
            yield json.loads(n_html["vrhm"])["pgurl"]

    def _get_direct_link(self):
        for link in self._get_search_results():
            start = time.time()

            if self._verbose:
                log.info("TRYING:{}".format(link))

            try:

                stream = self._ydl.extract_info(link, download=False).get("url", None)
                if stream:
                    if self._verbose:
                        log.info(
                            "MP4 URL:{} {:0.2f} seconds".format(
                                stream, time.time() - start
                            )
                        )
                    yield stream
                else:
                    if self._verbose:
                        log.info("discarded %s", link)
                    ...
            except AttributeError as e:
                if self._verbose:
                    log.error("no mp4 at addr {}".format(link))
                ...

    def _simple_get(self, bingurl):
        if self._verbose:
            log.debug("_simple_get(self,bingurl)")
            log.debug('bingurl="%s"', bingurl)
        cookiecontent = "ADLT=OFF&CW=1117&CH=1771&DPR=2&UTC=-360&HV={}"
        cookie = {"SRCHHPGUSR": cookiecontent.format(str(int(time.time())))}

        try:
            with closing(post(bingurl, cookies=cookie)) as resp:
                if resp.ok and "html" in resp.headers["Content-Type"]:
                    return resp.content
                return None
        except RequestException as err:
            sys.stderr.write(str(err))
            return None

    def playlist(self, query, outfile=None, count=105, duration=20):
        """So you want to see some porn eh?-

        this function is tied to fire.,Fire() which makes this function
        it's bitch and turns its arguments into positional. mandatory
        arguments for the bingporn command. keyword arguments are treated
        as option flags, since they are, well, optional. (havin a default
        value does that to ya. Also: when the docstring of a function is 6
        times longer than the function itself, do you really need that
        function? turns out most of the times, no. but in this case what i
        need to do is stop smoking that shit and watch some porn.

        Args:
            query (String): Your guilty pleasure, quoted e.g: "Emma Mae"
            count (TYPE, optional): DESCRIPTION. Defaults to 105.
            duration (TYPE, optional): DESCRIPTION. Defaults to 20.

        Returns:
            None.

        """
        self.query = query
        self.duration = duration
        self._outfile = outfile
        self.count = count

        if self._verbose:
            log.debug("playlist(self,query,count,duration)")
            log.debug("self._outfile %s", self._outfile)
            log.debug("query: %s", query)
            log.debug("count: %s", count)
            log.debug("duration: %s", duration)

        try:
            if self._outfile:
                if os.path.isfile(self._outfile):
                    openmode = "w+t"
                else:
                    openmode = "x+t"
                with open(self._outfile, mode=openmode, encoding="utf-8") as of:
                    [of.writeline(uri) for uri in self._get_direct_link()]

            else:
                sys.stdout.writelines(
                    ["{}\n".format(url) for url in self._get_direct_link()]
                )
        except KeyboardInterrupt:
            sys.stderr.write("User Abort Porn\n")
            sys.exit(1)
        finally:
            sys.exit(0)


if __name__ == "__main__":
    fire.Fire(BingPorn())

#  vim: set ft=python sw=4 tw=75 fdm=indent et :
