# -*- encoding: utf-8 -*-
# Written by kenkeiras
# 
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://sam.zoy.org/wtfpl/COPYING for more details.

from elisa.core.components.resource_provider import ResourceProvider
from elisa.core.log import Loggable
from elisa.core.utils import defer


from twisted.web2 import responsecode
from twisted.web2.stream import BufferedStream

from elisa.plugins.http_client.http_client import ClientRequest, ElisaHttpClient
from elisa.plugins.liberateca.models import LiberatecaVideoModel

from sys import stderr

def getHost(uri):
    return uri.split("://")[1].split("/")[0]

def getQuery(uri):
    return '/' + uri.split("://")[1].split("/",1)[1]

class LiberatecaResourceProvider(ResourceProvider):
    """
    Holds user data.

    @ivar user: API user
    @type user: C{unicode}
    @ivar password: API password
    @type password: C{unicode}
    """
    user = None
    password = None
    serie = None # For internal use
    temporada = None # For internal use

    def login(self, username = None, password = None):
        """
        Loads API username and password.

        @param username: API user
        @type username: C{str}

        @param password: API password
        @type password: C{str}

        """
        self.user = username
        self.password = password
        return defer.succeed(None)

    def clean(self):
        """
        Removes user and password information.
        """
        self.user = None
        self.password = None

    def get(self, media_uri, context_model = None, title = "", uri = ""):
        """
        Retrieves a uri model
        """
        if context_model == None:
            result_model = LiberatecaVideoModel(title, uri)
        else:
            result_model = context_model

        return result_model, defer.succeed(result_model)

