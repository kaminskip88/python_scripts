#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import sys
import re
from difflib import SequenceMatcher
from translit import translit
import unicodedata
import logging

logging.basicConfig(level=logging.DEBUG)


API_ADDR = 'http://api.kinopoisk.cf'

dir=['[2007]_I_Am_Legend_720p_Blu-ray.mkv                                                ',
'[2014]_Gran_buduschego_BDRip-AVC.mkv                                                   ',
'Alien.1979.720p.BluRay.x264-LEONARDO_[scarabey.org].mkv                                ',
'Aliens.1986_SE_HDRip___[scarabey.org].avi                                              ',
'A Nightmare on Elm Street.1984.720p.BluRay.x264-LEONARDO_[scarabey.org].mkv            ',
'Automata.2014.x264.BDRip.720p.0ptimus.mkv                                              ',
'Avatar.2009.720p.BluRay.x264-LEONARDO_[scarabey.org].mkv                               ',
'Avatar.Legenda.ob.Aange.Trilogiya(3.sezona.iz.3).2005-2008.DivX.DVDRip                 ',
'Constantine.2005.720p.LEONARDO_[scarabey.org].mkv                                      ',
'Despicable Me.2010.720p.BluRay.x264-LEONARDO_[scarabey.org].mkv                        ',
'Django.2012.720p.x264-LEONARDO_[scarabey.org].mkv                                      ',
'Futurama.V.Dikuju.Zelenuju.Dal.2009.DUAL.BDRip.XviD.AC3.-HQ-ViDEO.avi                  ',
'Guardians.of.the.Galaxy.2014.BDRip.IMAX.FD.avi                                         ',
'Hancock.2008.720p.Unrated.BluRay.x264-LEONARDO_[scarabey.org].mkv                      ',
'Hodjachij.zamok.2004.x264.BDRip.AVC.MediaClub.mkv                                      ',
'Idiocracy.2006.720p.HDTV.x264.dts.ac3-Skazhutin.mkv                                    ',
'Interstellar.2014.D.BDRip.720p_KinoGadget.mp4                                          ',
'Intouchables.2011.720p.BluRay.x264-LEONARDO_[scarabey.org].mkv                         ',
'John Wick.2014.1080p.BluRay.x264-LEONARDO_[scarabey.org].mkv                           ',
'Jurassic.Park.1993.BDRip.720p.mkv                                                      ',
'Koshmar.na.ulice.Vjazov.2010_HDRip_[scarabey.org].avi                                  ',
'Kung Fu Panda.2008.BDRip.LEONARDO_[scarabey.org].mkv                                   ',
'LArrivee dun train a la Ciotat (The Arrival of the Mail Train) 1895.avi                ',
'Lord of the Rings                                                                      ',
'Madagascar.2005.BDRip720p.DHT-Movies.mkv                                               ',
'Matrix.1999-2003.720p.BluRay.x264-LEONARDO_[scarabey.org]                              ',
'Mimi wo sumaseba.1995.720p.BluRay.x264-LEONARDO_[scarabey.org].mkv                     ',
'Mir.jrskogo.perioda.2015.x264.BDRip.(AVC).mkv                                          ',
'O_chem_govoryat_mujchiny_HDRip__[scarabey.org].avi                                     ',
'Orugeyniy.Baron.2005.x264.BDRip(AVC)-MediaClub.mkv                                     ',
'RED.2010.XviD.DUAL.AC3.HDRip.Rus.Eng                                                   ',
'Saylent.Hill.Dilogy.[2006-2012].-HELLYWOOD                                             ',
'Sen to Chihiro no kamikakushi.2001.720p.x264-LEONARDO_[scarabey.org].mkv               ',
'Shrek.2001.RUS.BDRip.XviD.AC3.-HQ-ViDEO.avi                                            ',
'Star Wars.1980.720p.BluRay.x264-LEONARDO_[scarabey.org].mkv                            ',
'Star Wars.1983.720p.BluRay.x264-LEONARDO_[scarabey.org].mkv                            ',
'Star Wars.1999.720p.BluRay.x264-LEONARDO_[scarabey.org].mkv                            ',
'Star Wars.2002.720p.BluRay.x264-LEONARDO_[scarabey.org].mkv                            ',
'Star Wars.2005.720p.BluRay.x264-LEONARDO_[scarabey.org].mkv                            ',
'Sumerki_2008_HDRip__[scarabey.org].avi                                                 ',
'Sumerki.Saga.Novolunie.2009.BDRip.Xvid.AC3.-HELLYWOOD                                  ',
'Sumerki_Saga_Novolunie_2009_HDRip_[scarabey.org].avi                                   ',
'Sumerki.Saga.Rassvet.Chast.I.II.[2011_2012]                                            ',
'The Hobbit An Unexpected Journey 2012 BDrip-AVC Froloff777.mkv                         ',
'Tonari no Totoro.1988.720p.BluRay.x264-LEONARDO_[scarabey.org].mkv                     ',
'Ya.Robot.2004.DUAL.BDRip.x264.-HELLYWOOD.mkv                                           ',
'Дракула.mkv                                                                            ',
'Дух времени (Zeitgeist) (2007).avi                                                     ',
'Не грози Южному Централу, попивая сок у себя в квартале [Goblin].avi                   ',
'Сумерки. Сага. Затмение_[scarabey.org]                                                 ',
'Х1.2000.720p.BluRay.x264-LEONARDO_[scarabey.org].mkv                                   ',
'Шерлок Холмс                                                                           ']

def curl(url, params=None):
    """
    :param url: string request URL
    :param params: request parameters as dict
    :return: request object
    """
    result = requests.get(url, params=params)
    if result.status_code == 200:
        return result
    else:
        print "Error, API respond with {0}".format(result.status_code)
        sys.exit(1)


def api_curl(url, params=None):
    """
    :return: dict object
    """
    result = curl(url, params)
    return result.json()


def get_film(film_id):
    """
    Get Film info dict by film ID
    :return: dict object
    """
    return api_curl('{0}/getFilm'.format(API_ADDR), {'filmID': str(film_id)})


def generate_title(film):
    """
    Generate title string
    :param film: dict with film information
    :return: string
    """
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
    """
    Get film ID by torrnet URL
    :param url: string
    :return: int
    """
    page = curl(url).text.encode('utf-8')
    match = re.search('http://www.kinopoisk.ru(/\w+)+/(\d\d+).*', page)
    if match:
        return int(match.groups()[1])
    else:
        print 'URL contains no Kinopoisk link'
        sys.exit(1)


################


def search_films(keyword):
    keyword = keyword.encode('utf-8')
    logging.debug('Search movies using {} keyword'.format(keyword))
    response = api_curl('{0}/searchFilms'.format(API_ADDR), {'keyword': keyword})
    try:
        if response['pagesCount'] == 0:
            logging.info('No results found')
            return []
        result = response['searchFilms']
        logging.debug('{} movies found'.format(len(result)))
        for p in result: logging.info('Found movies id: {}'.format(p['id']))
    except KeyError as e:
        logging.error('API response parsing error: {}'.format(e))
        logging.error('Response: {}'.format(response))
        sys.exit(1)
    return result


def year_filter(film_list, year, range=0):
    year = int(year)
    logging.debug('Filtering out movies by year {} with year dispersion {}'.format(year, range))
    logging.debug('{} movies in'.format(len(film_list)))
    film_list = filter(lambda i: 'year' in i, film_list)
    film_list = filter(lambda i: year - range <= int(i['year']) <= year + range, film_list)
    logging.debug('{} movies out'.format(len(film_list)))
    return film_list


def non_movie_filter(film_list):
    filter_list = [u'(видео)', u'(ТВ)']
    for string in filter_list:
        film_list = filter(lambda i: not string in i['nameEN'], film_list)
    return film_list


def get_year_from_string(string):
    result = re.search("[1-2]\d{3}", string)
    if result:
        return result.group(0)
    else:
        return '1900'  # temporarily


def split_string(string):
    replace_dict = {' ': '_',
                    '.': '_'}
    remove_list = ['[',
                   ']',
                   '(',
                   ')']
    for i, j in replace_dict.iteritems():
        string = string.replace(i, j)
    for i in remove_list:
        string = string.replace(i, '')
    result = string.split('_')
    return filter(lambda a: a, result)


def wordsFilter(words):
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



def get_score(api_title,title):
    obj = SequenceMatcher(None, api_title, title)
    return obj.ratio()
    #return relevancy.score(api_title, title)


def find_film_results(words, year,lang='en'):
    result_films = []
    if lang == 'tr':
        words = [translit(t) for t in words]
    films = search_films('_'.join(words))
    films_filtered = year_filter(films, year)
    # TODO make max range global variable
    if not films_filtered:
        films_filtered = year_filter(films, year, range=1)
    films = non_movie_filter(films_filtered)
    for film in films:
        if lang == 'tr':
            film_name = film['nameRU']
        elif lang == 'ru':
            film_name = film['nameRU']
        else:
            film_name = film['nameEN']
        score = get_score(film_name, ' '.join(words))
        film['rel_score'] = score
        result_films.append(film)
    return result_films


def get_best_result(title):
    title = title.decode('utf-8')
    year = get_year_from_string(title)
    words = split_string(title)
    words = wordsFilter(words)
    if detect_cyrillic(''.join(words)):
        lg_films = find_film_results(words, year, lang='ru')
        #for p in lg_films: logging.info('movie found matching RU title: {} (score:{})'.format(p['nameRU'],p['rel_score']))
    else:
        lg_films = find_film_results(words, year)
        #for p in lg_films: logging.info('movie found matching EN title: {} (score:{})'.format(p['nameEN'],p['rel_score']))
    tr_films = find_film_results(words, year, lang='tr')
    #for p in lg_films: logging.info('movie found matching RU title with transliteration: {} (score:{})'.format(p['nameRU'],p['rel_score']))
    result_films = tr_films+lg_films
    if result_films:
        result = max(result_films, key=lambda film: film['rel_score'])
    else:
        result = None
    return result

def detect_cyrillic(string, pos=0.5):
    string = unicode(string)
    cc = 0
    for char in string:
        if 'CYRILLIC' in unicodedata.name(char):
            cc += 1
    if float(cc) / float(len(string)) >= pos:
        #LOG
        return True
    else:
        #LOG
        return False


#for title in dir:
#    print '###', title, '###'
#    if get_best_result(title):
#        print generate_title(get_best_result(title))
#    else:
#        print '[RENAME_FAILED]_'+title

print get_best_result('Idiocracy.2006.720p.HDTV.x264.dts.ac3-Skazhutin.mkv                                    ')
