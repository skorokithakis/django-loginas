#!/usr/bin/env python

import os
import sys
from distutils.cmd import Command
from distutils.command.build import build as _build

from setuptools.command.install_lib import install_lib as _install_lib

from loginas import __version__

assert sys.version >= "2.5", "Requires Python v2.5 or above."

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


class compile_translations(Command):
    description = "compile message catalogs to MO files via django compilemessages"
    user_options = []  # type: list

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        curdir = os.getcwd()
        os.chdir(os.path.realpath("loginas"))
        from django.core.management import call_command

        call_command("compilemessages")
        os.chdir(curdir)


class build(_build):
    sub_commands = [("compile_translations", None)] + _build.sub_commands


class install_lib(_install_lib):
    def run(self):
        self.run_command("compile_translations")
        _install_lib.run(self)


setup(
    name="django-loginas",
    version=__version__,
    author="Stochastic Technologies",
    author_email="info@stochastictechnologies.com",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/stochastic-technologies/django-loginas/",
    description="""An app to add a "Log in as user" button in the Django user admin page.""",
    license="BSD",
    keywords="django",
    zip_safe=False,
    include_package_data=True,
    cmdclass={"build": build, "install_lib": install_lib, "compile_translations": compile_translations},
    packages=["loginas"],
    package_dir={"loginas": "loginas"},
)
