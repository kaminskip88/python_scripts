#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import sys
import re

API_ADDR = 'http://api.kinopoisk.cf'


def curl(url, params=False):
    result = requests.get(url, params=params)
    if result.status_code == 200:
        return result
    else:
        print "Error, API respond with {0}".format(result.status_code)
        sys.exit(1)


def api_curl(url, params=None):
    result = curl(url, params)
    return result.json()


def get_film(film_id):
    return api_curl('{0}/getFilm'.format(API_ADDR), {'filmID': str(film_id)})


def generate_title(film):
    params = {}
    for i in ['nameEN', 'nameRU', 'year']:
        try:
            params[i] = film[i].encode('utf-8')
        except TypeError:
            params[i] = ''
    if params['nameEN']:
        result = '{nameEN}_[{nameRU}]_({year})'.format(**params)
    else:
        result = '{nameRU}_({year})'.format(**params)
    return result.replace(' ', '_')


def get_film_by_torrent_url(url):
    page = curl(url).text.encode('utf-8')
    match = re.search('http://www.kinopoisk.ru(/\w+)+/(\d\d+).*', page)
    if match:
        return match.groups()[1]
    else:
        print 'URL contains no Kinopoisk link'
        sys.exit(1)
