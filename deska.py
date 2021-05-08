#!/usr/bin/env python3

# MIT License
#
# Copyright (c) 2021 Ferhat Geçdoğan All Rights Reserved.
# Distributed under the terms of the MIT License.
#

# DeskA - Desktop Application generator from CLI
#   command-line based websites based application
#   creator tool in Python3.
#
#   github.com/ferhatgec/deska
#


import pathlib
import urllib

from requests import get
from sys import argv
from re import search
from os import getenv

if len(argv) < 2:
    print('Where\'s my argument buddy?')
    exit(1)

env = getenv('SUDO_USER')

PATH = f'/home/{env}/.local/share/deska/'
DESKTOP = '/usr/share/applications/{name}.desktop'


def get_root_domain(url):
    head, sep, tail = url.partition('//')
    domain = tail.split('/', 1)[0] if '/' in tail else url

    return search(r'(.*)\.', domain.replace('https://', '').replace('www.', '')).group(1)


if not pathlib.Path(PATH).exists():
    pathlib.Path(PATH).mkdir(exist_ok=True)

dot_desktop = ''.join(['[Desktop Entry]\n',
                       'Name={app_name}\n',
                       'Exec=xdg-open {link}\n',
                       'Icon={path}\n',
                       'Type=Application\n',
                       'Keywords=web;browser;internet;\n',
                       'Categories=GTK;GNOME;Network;Web;\n',
                       'Terminal=false'])

url = search(
    r"\b((?:https?://)?(?:(?:www\.)?(?:[\da-z\.-]+)\.(?:[a-z]{2,6})|(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)|(?:(?:[0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,7}:|(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}|(?:[0-9a-fA-F]{1,4}:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}|(?:[0-9a-fA-F]{1,4}:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}|(?:[0-9a-fA-F]{1,4}:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:(?:(?::[0-9a-fA-F]{1,4}){1,6})|:(?:(?::[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(?::[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(?:ffff(?::0{1,4}){0,1}:){0,1}(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])|(?:[0-9a-fA-F]{1,4}:){1,4}:(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])))(?::[0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])?(?:/[\w\.-]*)*/?)\b",
    argv[1]).group(1)

if not 'http' in url:
    url = f'https://{url}'

req = urllib.request.Request(url + '/favicon.ico', headers={'User-Agent': 'Mozilla/5.0'})
res = urllib.request.urlopen(req)

name_of_app = get_root_domain(url)

with open(PATH + f'{argv[1]}.ico', "wb") as icon:
    icon.write(res.read())

dot_desktop = dot_desktop.format(app_name=get_root_domain(url).title(),
                                 link=url,
                                 path=PATH + f'{argv[1]}.ico')

with open(DESKTOP.format(name=name_of_app), "w") as file:
    file.write(dot_desktop)