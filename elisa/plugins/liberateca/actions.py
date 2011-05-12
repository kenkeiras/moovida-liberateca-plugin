# -*- encoding: utf-8 -*-
# Written by kenkeiras
# 
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://sam.zoy.org/wtfpl/COPYING for more details.

from elisa.plugins.database.actions import MoreOptionsAction
from elisa.plugins.poblesec.actions import OpenControllerAction
from elisa.core.action import ContextualAction

from elisa.plugins.poblesec.actions import LinkAction

class OpenLiberatecaControllerAction(OpenControllerAction):
    def execute(self, item):
        return self.open_controller(self.path, item.title, liberateca_model = item)

class AuthenticationAction(ContextualAction):
    """
    Log in button.

    @ivar name: button text
    @type name: C{unicode}
    """

    def __init__(self, controller):
        """
        Constructor.
        """
        super(AuthenticationAction, self).__init__(controller)
        self.name = "Introducir datos"

    def execute(self, item):
        """
        Opens the login form.
        """
        def controller_appended(result):
            self.name = "Reintentar"
            return result

        browser = self.controller.frontend.retrieve_controllers('/poblesec/browser')[0]
        path = "/poblesec/liberateca/login"
        title = "Introducir datos"
        dfr = browser.history.append_controller(path, title)
        dfr.addCallback(controller_appended)
        return dfr
