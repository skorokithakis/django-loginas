#!/usr/bin/env python
from loginas import __version__

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
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 2.2",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.0",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
