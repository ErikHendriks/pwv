#!/usr/bin/env bash

mkdir -p '$HOME/.passwordVault'
mkdir -p '$HOME/.passwordVault/database'
touch '$HOME/.passwordVault/hashfile'

./setupwv.py

# TODO
# import gnupg
# https://pypi.python.org/packages/57/0f/df2f8ba32c32ad5fb21822cfdc251e82341a2de334a878a2f354178fda56/gnupg-2.3.0-py2.7.egg#md5=5c3a29cea62d690ac5cd6856cd1b805f

# https://pypi.python.org/pypi?:action=show_md5&digest=5c3a29cea62d690ac5cd6856cd1b805f

# https://pypi.python.org/packages/57/0f/df2f8ba32c32ad5fb21822cfdc251e82341a2de334a878a2f354178fda56/gnupg-2.3.0-py2.7.egg.asc
