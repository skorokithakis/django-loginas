#!/usr/bin/env python

import sys, os
from loginas import __version__
assert sys.version >= '2.5', "Requires Python v2.5 or above."
from distutils.core import setup
from distutils.command.build import build as _build
from setuptools.command.install_lib import install_lib as _install_lib
from distutils.cmd import Command
from setuptools import find_packages

class compile_translations(Command):
    description = 'compile message catalogs to MO files via django compilemessages'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        curdir = os.getcwd()
        os.chdir(os.path.realpath('loginas'))
        from django.core.management import call_command
        call_command('compilemessages')
        os.chdir(curdir)


class build(_build):
    sub_commands = [('compile_translations', None)] + _build.sub_commands


class install_lib(_install_lib):
    def run(self):
        self.run_command('compile_translations')
        _install_lib.run(self)


setup(
    name="django-loginas",
    version=__version__,
    author="Stochastic Technologies",
    author_email="info@stochastictechnologies.com",
    url="https://github.com/stochastic-technologies/django-loginas/",
    description="""An app to add a "Log in as user" button in the Django user admin page.""",
    long_description="A short Django app that adds a button in the Django user admin page. "
                     "When a superuser clicks the button, they are instantly logged in as that "
                     "user.",
    license="BSD",
    keywords="django",
    zip_safe=False,
    include_package_data=True,
    packages=find_packages(),
    cmdclass={'build': build, 'install_lib': install_lib,
        'compile_translations': compile_translations}
)
