#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import re
import sys
import json
import os


search_objects = {
                    'OS':{
                        'name':'Обновление прошивки',
                        'link':''
                    },
                    'DB':{
                        'name':'Обновление GPS-базы',
                        'link':''
                    }
                }
match_pattern = '''<a href=["']([^'"]+)["'](\s*download="[^"]*")?>{0}</a>'''
site_url = 'http://9700a.neoline.ru/'
state_file = './.neoline.state'
dl_target_location = '/storage/download/NEOLINE/'

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
        print "Error, site respond with {0}".format(result.status_code)
        sys.exit(1)


def read_state(sfile):
    with open(sfile) as data_file:
        return json.load(data_file)

def write_state(state,sfile):
    print 'Updating state file'
    with open(sfile, 'w+') as outfile:
        json.dump(state, outfile)

def download(url,target):
    print 'downloading', url, 'to', target
    local_filename = url.split('/')[-1]
    r = requests.get(url, stream=True)
    with open('{0}/{1}'.format(target, local_filename), 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
    return target

response = curl(site_url)

for key, value in search_objects.iteritems():
    match = re.search(match_pattern.format(value['name']), response.text.encode('utf-8'))
    if match:
        value['link'] = '{0}{1}'.format(site_url, match.groups()[0])
    else:
        print 'No {0} update link found'.format(key)

state = {}

if os.path.isfile(state_file):
    state = read_state(state_file)
    search_objects['OS']['state'] = state['OS']
    search_objects['DB']['state'] = state['DB']
else:
    search_objects['OS']['state'] = ''
    search_objects['DB']['state'] = ''

for key, value in search_objects.iteritems():
    print 'Comparing {0}'.format(key)
    if value['state'] == value['link']:
        print '{0} up-to-date'.format(key)
    else:
        download(value['link'], dl_target_location)
        state[key] = value['link']

write_state(state, state_file)
