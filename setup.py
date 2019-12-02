#!/usr/bin/env python

import sys

from loginas import __version__

assert sys.version >= "3.4", "Requires Python v3.4 or above."

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

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
    packages=["loginas"],
    package_dir={"loginas": "loginas"},
    python_requires='>3.3',
)
