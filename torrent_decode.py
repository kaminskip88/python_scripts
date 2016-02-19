#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

def tokenize(text, match=re.compile("([idel])|(\d+):|(-?\d+)").match):
    i = 0
    while i < len(text):
        m = match(text, i)
        s = m.group(m.lastindex)
        i = m.end()
        if m.lastindex == 2:
            yield "s"
            yield text[i:i+int(s)]
            i = i + int(s)
        else:
            yield s

def decode_item(next, token):
    if token == "i":
        # integer: "i" value "e"
        data = int(next())
        if next() != "e":
            raise ValueError
    elif token == "s":
        # string: "s" value (virtual tokens)
        data = next()
    elif token == "l" or token == "d":
        # container: "l" (or "d") values "e"
        data = []
        tok = next()
        while tok != "e":
            data.append(decode_item(next, tok))
            tok = next()
        if token == "d":
            data = dict(zip(data[0::2], data[1::2]))
    else:
        raise ValueError
    return data

def decode(text):
    try:
        src = tokenize(text)
        data = decode_item(src.next, src.next())
        for token in src: # look for more tokens
            raise SyntaxError("trailing junk")
    except (AttributeError, ValueError, StopIteration):
        raise SyntaxError("syntax error")
    return data

#data = open("C:\cygwin\home\Piotr_Kaminski/test.torrent", "rb").read()

#torrent = decode(data)

#print torrent['publisher-url']

#print relevancy.score(api_title, title)

#import relevancy

#print relevancy.score('Грань будущего', 'Гран будусчего')

#from translit import translit

#t = u'O chem govoryat mujchiny'

#title = translit(t)
#print title

#from difflib import SequenceMatcher
#a = SequenceMatcher(None,u'O чем говорят муйчины', u'О чём говорят мужчины')
#print a.ratio()

import unicodedata

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



text = u'ddмммdd'

print detect_cyrillic(text)