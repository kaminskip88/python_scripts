#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tmdbsimple as tmdb
from difflib import SequenceMatcher
import logging
import re
import requests
from translit import translit
import sys
from time import sleep

logging.basicConfig(level=logging.DEBUG,
                    #filename='myscript.log',
                    format='%(asctime)s %(levelname)s %(message)s'
                    )

TMDB_API_KEY = 'd9a25ef6b180e7989d91669153624afe'
GOOGLE_API_KEY = 'AIzaSyDuqyHg8Di9_tm-sKi8g5vo_deA9Q_Fs_s'


tmdb.API_KEY = TMDB_API_KEY


def get_year_from_string(string):
    logging.debug('Searching for year in title: {}'.format(string.encode('utf-8')))
    result = re.search("[1-2]\d{3}", string)
    if result:
        year = result.group(0)
        logging.debug('Year found: {}'.format(year))
        return year
    else:
        logging.warn('No year found in title')
        return None

def split_string(string):
    replace_dict = {' ': '_',
                    '.': '_'}
    remove_list = ['[',
                   ']',
                   '(',
                   ')']
    logging.debug('Splitting title: {}'.format(string.encode('utf-8')))
    for i, j in replace_dict.iteritems():
        string = string.replace(i, j)
    for i in remove_list:
        string = string.replace(i, '')
    result = string.split('_')
    return filter(lambda a: a, result)  # filter empty values


def words_filter(words):
    logging.debug('Applying filters')
    rm_list = ['scarabey',
                'Blu.?ray',
                '0ptimus',
                'LEONARDO',
                'DivX',
                'XviD',
                'IMAX',
                'KinoGadget',
                'MediaClub',
                'HELLYWOOD',
                '\d+p',
                'x264',
                'HDTV',
                'HQ-ViDEO',
                'Froloff77',
                'DUAL',
                'rip',
                '^\d+$',
                'movie',
                'unrated',
                'ac3',
                'fd',
                'se',
                'avi',
                'mkv',
                'org',
                'mp4',
                'rus',
                'eng',
                'avc',
                'dts']
    for regexp in rm_list:
        words = filter(lambda word: not re.search(regexp, word, re.IGNORECASE), words)
    #if len(words) > 1:
    #    words = filter(lambda word: not len(word) <= 3, words)
    return words


def get_score(api_title, title):
    obj = SequenceMatcher(None, api_title, title)
    logging.debug('Match "{}" against "{}"'.format(api_title.encode('utf-8'), title.encode('utf-8')))
    return int(obj.ratio())
    # return relevancy.score(api_title, title)

def curl(url, params=None):
    """
    :param url: string request URL
    :param params: request parameters as dict
    :return: request object
    """
    result = requests.get(url, params=params, timeout=100)
    if result.status_code == 200:
        return result
    else:
        print "Error, API respond with {0}".format(result.status_code)
        sys.exit(1)



#title = 'John Wick.2014.1080p.BluRay.x264-LEONARDO_[scarabey.org].mkv                           '
#year = get_year_from_string(title)
#words = split_string(title)
#words = words_filter(words)
#title = ' '.join(words)

#search = tmdb.Search()
#response = search.movie(query='John')
#for s in search.results:
#    print s['title'], s['id'], s['release_date']
def speller(text):
    speller_api_url = 'http://speller.yandex.net/services/spellservice.json/checkText'
    response = curl(speller_api_url, params={'text': text, 'int': 768, 'lang': 'ru'})
    if response.json():
        return False
    else:
        return True

for i in translit('Orugeyniy'):
    s = speller(i)
    if s:
        print i