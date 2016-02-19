#!/usr/bin/env python
# -*- coding: utf-8 -*-

from string import maketrans

literal_mapping = (
    u"abvgdezijklmnoprstufhc'y'",
    u"абвгдезийклмнопрстуфхцъыь"
    )

complex_mapping = {
    u"zh": u"ж",
    u"ts": u"ц",
    u"ch": u"ч",
    u"sh": u"ш",
    u"sch": u"щ",
    u"ju": u"ю",
    u"ja": u"я",
    u"ya": u"я",
    u"yu": u"ю",
}

#ambiguity_mapping = {
#    u"g": [u"г", u"ж"],
#    u"j": [u"ж", u"й"],
#    u"y": [u"й", u"ы"],
#}

class Transliterate(object):

    def __init__(self):
        table_in = literal_mapping[0]
        table_out = literal_mapping[1]
        table_in = [ord(char) for char in table_in]
        translate_table = dict(zip(table_in, table_out))
        self.literal_mapping = translate_table
        self.complex_mapping = complex_mapping
        #self.ambiguity_mapping = ambiguity_mapping
        self.complex_mapping_keys = self.complex_mapping.keys()

    def translit(self, string):
        result = []
        string = unicode(string).lower()
        if self.complex_mapping:
            for rule in sorted(self.complex_mapping_keys,key=len,reverse=True):
                string = string.replace(rule, self.complex_mapping[rule])
        if self.literal_mapping:
            string = string.translate(self.literal_mapping)
        #if self.ambiguity_mapping:
        #    for ambiguity_char, values in self.ambiguity_mapping.iteritems():
        #        if ambiguity_char in string:
        #            for value in values:
        #                result.append(string.replace(ambiguity_char, value))
        return string


def translit(string):
    inst = Transliterate()
    return inst.translit(string)
