# -*- encoding: utf-8 -*-
# Written by kenkeiras
# 
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://sam.zoy.org/wtfpl/COPYING for more details.

from elisa.core import common
from elisa.core.utils import defer
from elisa.core.utils.i18n import install_translation

from elisa.plugins.poblesec.plugins_settings import GenericSettingsController
from elisa.plugins.poblesec.login import LoginController
from elisa.plugins.liberateca.actions import AuthenticationAction

from sys import stderr

_poblesec = install_translation('poblesec')

def liberateca_settings_decorator(controller):
    controller.append_plugin('liberateca', 'Liberateca', '/poblesec/liberateca/settings')
    return defer.succeed(None)

class LiberatecaSettingsController(GenericSettingsController ):

    def populate_model(self):
        action = AuthenticationAction(self)
        action.connect('name-changed', self._action_name_changed_cb)
        model = [action,]
        return defer.succeed(model)

    def _action_name_changed_cb(self, *args ):
        self.refresh()

# Liberateca provider
def get_liberateca_provider():

    provider_path = 'elisa.plugins.liberateca.resource_provider:LiberatecaResourceProvider'
    manager = common.application.resource_manager
    provider = manager.get_resource_provider_by_path(provider_path)

    return provider

##################################################################
class LiberatecaLoginController(LoginController):
    def login(self, username, password):
        try:
            provider = get_liberateca_provider()
        except Exception as e:
            return defer.fail(e)
        else:
            return provider.login(username, password)

    def success(self, result):
        browser = self.frontend.retrieve_controllers('/poblesec/browser')[0]
        paths = [('/poblesec/internet_menu', _poblesec('INTERNET MEDIA'), {}),
                 ('/poblesec/video/internet', _poblesec('Video'), {}),
                 ('/poblesec/liberateca/main', _poblesec('Liberateca'), {})]
        return browser.navigate(paths)

