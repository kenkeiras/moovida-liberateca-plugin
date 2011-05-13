#!/usr/bin/env python
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
import urllib, urllib2

from sys import stderr

def array_expand(s, n):
    while len(s ) < n:
        s = [ 0 ] + s

    return s
    

class linkExtractor:
    """
    Reads the direct link from file hosting services.
        (currently just megaupload and megavideo)

    @ivar megauploadRegExp: Megaupload url matcher
    @type megauploadRegExp: C{str}

    @ivar MUmatcher: Megaupload download link matcher
    @type MUmatcher: SRE_Pattern

    @ivar MUsleepTime: Time to wait for downloading with megaupload
    @type MUsleepTime: C{int}

    @ivar megavideodRegExp: Megavideo url matcher
    @type megavideoRegExp: C{str}
    """
    megauploadRegExp = "(http://){0,1}(www.){0,1}megaupload.com/?.*d=.*"
    megavideoRegExp = "(http://){0,1}(www.){0,1}megavideo.com/?.*v=.*"

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

    def getMVlink(self, link):
        """
        Reads a download link from a Megavideo link
        """

        def shred(s ):
            arr = []
            for c in s:
                arr.append( int(c) )
            return arr

        # Mezcla los parámetros de Megavideo para producir lo necesario para la url
        def MVsmash( k1, k2, s ):
            # Caracteres hexadecimales
            hx = map(lambda x: str(x), range(10)) + \
                 map(lambda x: chr(x), range(0x61, 0x67))

            expanded = []
            for c in s:
                expanded += array_expand(shred((bin( hx.index(c))[ 2 : ])) , 4 )

            fuzzed = []
            for i in xrange( 384 ):
                k1 = ((k1 * 11) + 77213) % 81371
                k2 = ((k2 * 17) + 92717) % 192811
                fuzzed.append((k1 + k2) & 127)
              
            for i in xrange( 256, 0, -1 ):
                aux = fuzzed[i]
                aux2 = i & 127
                aux3 = expanded[aux]
                expanded[aux] = expanded[aux2]
                expanded[aux2] = aux3

            for i in xrange( 128 ):
                expanded[i] = expanded[i] ^ (fuzzed[ i + 256 ] & 1)

            bin_final = []
            
            for i in xrange( 0, len(expanded), 4 ):
                d = ''.join(map(lambda x: str(x), expanded[ i : i + 4 ]))
                bin_final.append( d )
 
            final = ""

            for c in bin_final:
                final += (hx[int(c,2)])
                
            return final

            

        v = link.split("v=")[-1].split("&")[0]
        infoLnk = "http://www.megavideo.com/xml/videolink.php?v=" + v
        r = urllib2.Request( infoLnk )
        data = urllib2.urlopen(r).read()

        link = ""
        try: # Look for HD video
            link = data.split('hd_url="')[1].split('"')[0]
            link = urllib.unquote_plus(link)

        except: # else fallback to normal video :/
            s = data.split(' s="')[1].split('"')[0]

            k1 = int(data.split(' k1="')[1].split('"')[0] )
            k2 = int(data.split(' k2="')[1].split('"')[0] )
            un = data.split(' un="')[1].split('"')[0]

            link = "http://www" + s + ".megavideo.com/files/"    
            link += MVsmash( k1, k2, un) + "/"

        return link

    def getLink(self, link):
        """
        Reads a download link from the service which matches the url.
        """
        if re.match(self.megauploadRegExp, link):
            return self.getMUlink(link)
        elif re.match(self.megavideoRegExp, link):
            return self.getMVlink(link)
        else:
            raise Exception("Server \"%s\" not supported" %
                            link.split("://")[-1].split("/")[0] )


if __name__=="__main__":
    from sys import argv
    if len(argv) < 2:
        print >>stderr, argv[0], "<link>"
        exit(0)
    x = linkExtractor()
    print x.getLink(argv[1])
