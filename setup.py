# -*- encoding: utf-8 -*-
# kenkeiras <kenkeiras@gmail.com>

import os
from setuptools import setup, find_packages, Extension
from elisa.core.utils.dist import find_packages, TrialTest, Clean

packages, package_dir = find_packages(os.path.dirname(__file__))
cmdclass = dict(test=TrialTest, clean=Clean)

setup(
    name='elisa-plugin-liberateca',
    version='0.1',
    description='Liberateca',
    long_description='Busca series en Liberateca.',
    license='WTFPLv2',
    author='kenkeiras',
    author_email='kenkeiras@gmail.com',
    namespace_packages=['elisa', 'elisa.plugins', 'elisa.plugins.liberateca'],
    packages=packages,
    package_dir=package_dir,
    cmdclass=cmdclass,
    
    decorator_mappings=[
        ('/poblesec/video/internet',
         'elisa.plugins.liberateca.decorator:liberateca_decorator'),
        ('/poblesec/settings/plugins', 
         'elisa.plugins.liberateca.settings:liberateca_settings_decorator'),
        ],

    controller_mappings=[
        ('/poblesec/liberateca/main', 
         'elisa.plugins.liberateca.controllers:LiberatecaController'),
        ('/poblesec/liberateca/temporadas', 
         'elisa.plugins.liberateca.controllers:LiberatecaSeasonController'),
        ('/poblesec/liberateca/caps', 
         'elisa.plugins.liberateca.controllers:LiberatecaChapterController'),
        ('/poblesec/liberateca/settings', 
         'elisa.plugins.liberateca.settings:LiberatecaSettingsController'),
        ('/poblesec/liberateca/login',
         'elisa.plugins.liberateca.settings:LiberatecaLoginController'),
        ],

    entry_points="""\
    [elisa.core.components.resource_provider]
    LiberatecaResourceProvider = elisa.plugins.liberateca.resource_provider:LiberatecaResourceProvider
    [elisa.core.plugin_registry]
    use = elisa.plugins.liberateca.controllers:use_me_hook
    """,
    package_data={
        '': ['*.png', '*.conf', '*.pyd', '*.so'],
        },
    data_files = [
        ('elisa/plugins/liberateca/icons',
          ['elisa/plugins/liberateca/icons/icon1.png',
          'elisa/plugins/liberateca/icons/icon2.png']),
    ],
    zip_safe=False,
)

