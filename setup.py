#!/usr/bin/env python

import sys
assert sys.version >= '2.5', "Requires Python v2.5 or above."
from distutils.core import setup
from setuptools import find_packages

setup(
    name="django-loginas",
    version="0.1.2",
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
    test_suite='runtests.run_tests',
    tests_require=['Django>=1.4'],
)
