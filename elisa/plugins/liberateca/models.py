# -*- encoding: utf-8 -*-
# Written by kenkeiras
# 
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://sam.zoy.org/wtfpl/COPYING for more details.


from sys import stderr

from elisa.core.utils import defer
from elisa.core.media_uri import MediaUri
from elisa.core.common import application
from elisa.plugins.base.models.video import VideoModel

from elisa.plugins.liberateca.settings import get_liberateca_provider

class LiberatecaVideoModel(VideoModel):
    """
    Contains video data.

    @ivar title: the title of the video
    @type title: C{unicode}
    @ivar uri: uri where the video is located
    @type uri: L{elisa.core.media_uri.MediaUri}
    @ivar plain_uri: uri where the video is located, in a plain string
    @type plain_uri: C{unicode}
    """
    source_properties = {}
    
    def __init__(self, title, uri):
        """
        Constructor. Initializes all the fields

        @param title: video title
        @type title: C{str}

        @param uri: video uri
        @type uri: C{str}
        """
        super(LiberatecaVideoModel, self).__init__()
        self.title = title

        self.uri = MediaUri(uri)
        self.plain_uri = uri
        self.playable_model = None

    def get_poster(self):
        """
        Return a deferred that will return the local path of the video poster
        (not available yet)
        """
        return defer.succeed(None)

    def get_playable_model(self):
        """
        Return a deferred that will return an instance of
        L{elisa.plugins.base.models.media.PlayableModel} for the video.

        @rtype:  L{elisa.core.utils.defer.Deferred}
        """
        def got_playable(model):
            dfr = defer.succeed(model)
            return dfr
        
        model = None
        if self.playable_model:
            model = self.playable_model
            dfr = defer.succeed(self.playable_model)
        else:
            muri = self.playable_uri
            pro = get_liberateca_provider()
            model, dfr = \
                pro.get(muri, self, self.title, self.plain_uri)
            
        dfr.addCallback(got_playable)
        dfr.addErrback(lambda failure: stderr.write("[liberateca] >:/ %s" % failure))
        return dfr

