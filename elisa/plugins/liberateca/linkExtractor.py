# -*- encoding: utf-8 -*-
# Written by kenkeiras
# 
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://sam.zoy.org/wtfpl/COPYING for more details.

import re
import time
import urllib2

class linkExtractor:
    """
    Reads the direct link from file hosting services.
        (currently just megaupload)

    @ivar megauploadRegExp: Megaupload url matcher
    @type megauploadRegExp: C{str}

    @ivar MUmatcher: Megaupload download link matcher
    @type MUmatcher: SRE_Pattern

    @ivar MUsleepTime: Time to wait for downloading with megaupload
    @type MUsleepTime: C{int}
    """
    megauploadRegExp = "(http://){0,1}(www.){0,1}megaupload.com/?.*d=.*"

    MUmatcher = re.compile('"downloadlink"><a\shref="([^"]*)".*')

    MUsleepTime = 46

    def cleanUrl(self, url):
        """
        Returns a URL which urllib can open.
        """
        if not ("http://" in url and url.index("http://") == 0):
            return "http://" + url
        return url

    def getMUlink(self, link):
        """
        Reads a download link from a Megaupload link
        """
        r = urllib2.Request(self.cleanUrl(link))
        data = urllib2.urlopen(r).read()

        m = self.MUmatcher.search( data)
        if not m:
            raise Exception("Error requesting file")

        time.sleep( self.MUsleepTime)
        return m.group(1)

    def getLink(self, link):
        """
        Reads a download link from the service which matches the url.
        """
        if re.match(self.megauploadRegExp, link):
            return self.getMUlink(link)

        else:
            raise Exception("Server \"%s\" not supported" %
                            link.split("://")[-1].split("/")[0] )


if __name__=="__main__":
    from sys import argv, stderr
    if len(argv) < 2:
        print >>stderr, argv[0], "<link>"
        exit(0)
    x = linkExtractor()
    print x.getLink(argv[1])
