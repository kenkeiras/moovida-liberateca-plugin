# -*- encoding: utf-8 -*-
# Written by kenkeiras
# 
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://sam.zoy.org/wtfpl/COPYING for more details.

from elisa.core.utils import defer

def liberateca_decorator(controller):
    """
    Internet video decorator.        
    """
    controller.append_plugin('liberateca', 'Liberateca', '/poblesec/liberateca/main')
    return defer.succeed(None)
