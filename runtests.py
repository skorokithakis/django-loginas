#!/usr/bin/env python
import os
import sys

from django.conf import settings


if not settings.configured:
    settings.configure(**{
        'ROOT_URLCONF': 'loginas.tests.urls',
        'INSTALLED_APPS': (
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.auth',
            'loginas',
            'loginas.tests',
        ),
        'DATABASES': {"default": {"ENGINE": "django.db.backends.sqlite3"}},
    })


def run_tests():
    parent = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, parent)

    from django.test.simple import DjangoTestSuiteRunner
    failures = DjangoTestSuiteRunner(
        verbosity=1, interactive=True, failfast=False).run_tests(['tests'])
    sys.exit(failures)


if __name__ == '__main__':
    run_tests()
