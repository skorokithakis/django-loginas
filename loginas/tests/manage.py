#!/usr/bin/env python
import os
import sys


if __name__ == "__main__":

    # So that we always import our stuff.
    PROJECT_ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    sys.path.insert(0, PROJECT_ROOT_DIR)

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "loginas.tests.settings")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
