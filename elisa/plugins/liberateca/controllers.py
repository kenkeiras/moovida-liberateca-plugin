# -*- encoding: utf-8 -*-
# Written by kenkeiras
# 
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://sam.zoy.org/wtfpl/COPYING for more details.

from elisa.core.common import application
from elisa.core.utils import defer
from elisa.core.media_uri import MediaUri
from elisa.plugins.poblesec.plugins_settings import GenericSettingsController
from elisa.core.utils.i18n import install_translation

from elisa.core.action import ContextualAction

from elisa.plugins.liberateca.models import LiberatecaVideoModel
from elisa.plugins.liberateca.settings import get_liberateca_provider
from elisa.plugins.liberateca.liberateca import liberateca
from elisa.plugins.liberateca.linkExtractor import linkExtractor

from sys import stderr

_poblesec = install_translation('poblesec')

#########################################################################
def use_me_hook(frontend):
    browser = frontend.retrieve_controllers('/poblesec/browser')[0]
    paths = [('/poblesec/internet_menu', _poblesec('INTERNET MEDIA'), {}),
             ('/poblesec/video/internet', _poblesec('Video'), {}),
             ('/poblesec/liberateca/main', _poblesec('Liberateca'), {})]
    return browser.navigate(paths)

#########################################################################
class serieButton(ContextualAction):

    def __init__(self, controller, title, id):
        super(serieButton, self).__init__(controller)
        self.name = title
        self.id = id

    def execute(self, item):
        pro = get_liberateca_provider()
        pro.serie = self.id

        browser = self.controller.frontend.retrieve_controllers('/poblesec/browser')[0]
        path = '/poblesec/liberateca/temporadas'
        title = self.name
        dfr = browser.history.append_controller(path, title)
        return dfr

def orderSerieList( list ):

    return sorted(list,
           lambda x, y: cmp(x['name'].lower(), y['name'].lower()))


class LiberatecaController(GenericSettingsController ):
    def populate_model(self):
        p = get_liberateca_provider()
        if p.user == None:
            return defer.fail('No se han introducido los datos')

        
        l = liberateca(p.user, p.password)

        model = []
        try:
            list = l.getSerieList()        
        except Exception as e:
            return defer.fail('Error descargando lista de series [%s]' % str(e))

        # Ordena la lista alfabéticamente
        slist = orderSerieList( list )

        for i in slist:
            action = serieButton(self, i['name'],  i['id'])
            action.connect('name-changed', self._action_name_changed_cb)
            model.append(action)
        return defer.succeed(model)

    def _action_name_changed_cb(self, *args ):
        self.refresh()

#########################################################################
class seasonButton(ContextualAction):

    def __init__(self, controller, title, id):
        super(seasonButton, self).__init__(controller)
        self.name = title
        self.id = id

    def execute(self, item):
        pro = get_liberateca_provider()
        pro.temporada = self.id

        browser = self.controller.frontend.retrieve_controllers('/poblesec/browser')[0]
        path = '/poblesec/liberateca/caps'
        title = self.name
        dfr = browser.history.append_controller(path, title)

        return dfr


class LiberatecaSeasonController(GenericSettingsController ):
    def populate_model(self):
        p = get_liberateca_provider()
        if p.user == None:
            return defer.fail('No se han introducido los datos')

        
        l = liberateca(p.user, p.password)

        model = []
        try:
            list = l.getSerieT(p.serie)
        except Exception as e:
            return defer.fail('Error descargando lista de temporadas [%s]' % str(e))


        for i in list:
            num = i['url'].split("/")[-2]
            action = seasonButton(self, 'Temporada ' + num, num)
            action.connect('name-changed', self._action_name_changed_cb)
            model.append(action)

        self.refresing = False
        return defer.succeed(model)


    def _action_name_changed_cb(self, *args ):
        if not self.refreshing:
            self.refreshing = True
            self.refresh()
            self.refreshing = False

#########################################################################
class chapterButton(ContextualAction):

    def __init__(self, controller, title, id):
        super(chapterButton, self).__init__(controller)
        self.name = title
        self.id = id
        self.model = None

    def execute(self, item):
        #print >>stderr, "[liberateca] go go go!!"

        p = get_liberateca_provider()
        l = liberateca(p.user, p.password)
        try:
            links = l.getSerieEp( p.serie, p.temporada, self.id)['links']
        except Exception as e:
            return defer.fail(e)
        okLink = None
        x = linkExtractor()
        for link in links:
            try:
                print >>stderr, "[liberateca] comprobando link [%s]" % link['url']
                lnk = x.getLink(link['url'])
                print >>stderr, "[liberateca] hay link [ %s ]" % lnk
                okLink = lnk
                break

            except:
                pass

        if not okLink:
            print >>stderr, "[liberateca] no hubo suerte :/"
            return defer.fail(Exception("No se han encontrado servidores soportados"))

        video = LiberatecaVideoModel(self.name, okLink)
        return play_this(video, self.controller.frontend)

def play_this(video, frontend):
    controllers = frontend.retrieve_controllers('/poblesec/video_player')
    player = controllers[0]

    player.player.play_model(video)

    controllers = frontend.retrieve_controllers('/poblesec')
    main = controllers[0]
    main.show_video_player()

    return defer.succeed(video)


def orderCapList( list ):
    return sorted(list,
           lambda x, y: cmp(x['episode'], y['episode']))

class LiberatecaChapterController(GenericSettingsController ):
    def populate_model(self):
        p = get_liberateca_provider()
        if p.user == None:
            return defer.fail('No se han introducido los datos')

        l = liberateca(p.user, p.password)

        model = []
        try:
            list = l.getSerieT(p.serie, p.temporada)
        except Exception as e:
            return defer.fail('Error descargando lista de episodios [%s]' % str(e))

        slist = orderCapList( list )

        for i in slist:
            num = i['episode']
            action = chapterButton(self, i['title'], i['episode'])
            action.connect('name-changed', self._action_name_changed_cb)
            model.append(action)
        return defer.succeed(model)

    def _action_name_changed_cb(self, *args ):
        self.refresh()
