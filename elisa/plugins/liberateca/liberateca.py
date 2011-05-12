# -*- encoding: utf-8 -*-
# Written by kenkeiras
# 
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://sam.zoy.org/wtfpl/COPYING for more details.

from sys import stderr
import urllib2, base64

def unroll(text ):
    """
    Converts the text into 'native' variables.
    Quick & Dirty, a manipulated server could inyect code :/
    """
    foo = []
    exec "foo.append(%s)" % text
    return foo[0]

def toUrl(base, url):
    url = url.replace("__",str(base))
    return url

# Clase principal
class liberateca:
    """
    Liberateca API interface.

    @ivar user: API user
    @type user: C{unicode}
    @ivar passwd: API password
    @type passwd: L{elisa.core.media_uri.MediaUri}
    """

    # Inicialización
    def __init__(self, user, passwd, baseUrl = "https://liberateca.net/api/v1" ):
        """
        Constructor. Initializes all the fields.

        @param user: API user
        @type user: C{str}

        @param passwd: API password
        @type passwd: C{str}

        @param baseUrl: API base url
        @type baseUrl: C{str}

        """
        self.user = user
        self.passwd = passwd

        # Url's varias
        self.SerieListUrl = baseUrl+"/series"
        self.SerieUrl     = baseUrl+"/series/__"
        self.SerieTUrl    = baseUrl+"/series/__/seasons"
        self.SerieTNUrl   = baseUrl+"/series/__/"
        self.SerieTEUrl   = baseUrl+"/series/__/"

    # Lee una url, para usos internos
    def getUrl(self, url ):

        # Prepara la petición
        r = urllib2.Request(url )

        # Prepara la autenticación
        authStr = base64.encodestring('%s:%s' % (self.user, self.passwd))[:-1]

        # Añade la cabecera
        r.add_header("Authorization", "Basic %s" % authStr)

        # Envía la petición y devuelve el resultado
        return urllib2.urlopen(r).read()

    # Muestra la lista de series como un array de diccionarios
    def getSerieList(self ):
        """
        Shows the serie list as a dictionary array.
        """

        raw = self.getUrl(self.SerieListUrl).strip()
        return unroll(raw )

    # Muestra la información de una serie
    def getSerie(self, serie ):
        """
        Retrieves a series information.

        @param serie: series ID
        @type serie: int
        """

        url = toUrl(serie, self.SerieUrl)
        return unroll(self.getUrl(url).strip())

    # Muestra la información de una temporada de una serie
    def getSerieT(self, serie, temporada = -1):
        """
        Retrieves the series season list or some season information.

        @param serie: series ID
        @type serie: int

        @param temporada: season
        @type temporada: int
        """

        if (temporada == -1): # No se usa t = None para ayudar a ShedSkin
            url = toUrl(serie, self.SerieTUrl)
            return unroll(self.getUrl(url).strip())

        url = toUrl(serie, self.SerieTNUrl) + str(temporada)
        return unroll(self.getUrl(url).strip())

    # Muestra la información de un capítulo
    def getSerieEp(self, serie, temporada, episodio):
        """
        Retrieves a series chapter information.

        @param serie: series ID
        @type serie: int

        @param temporada: season
        @type temporada: int

        @param episodio: chapter
        @type episodio: int
        """

        url = toUrl(serie, self.SerieTEUrl) + str(temporada) + "/" + str(episodio)
        return unroll(self.getUrl(url).strip())

# Hmm... creo te has confundido...
if __name__=="__main__":
    print >>stderr, "Esto no es un script, prueba a ejecutar el otro ;)"
