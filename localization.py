#!/usr/bin/python

import os

class Importer(object):
    def gen_words(self):
        assert(False) # yield words!

class Exporter(object):
    def export(self, dictionary):
        self.export_init(dictionary)
        for k, word in dictionary.words.iteritems():
            self.export_word(dictionary, word)
        self.export_final(dictionary)
        return self.export_result()

    def export_init(self, dictionary):
        assert(False) # implement this!

    def export_word(self, dictionary, word):
        assert(False) # implement this!

    def export_final(self, dicitonary):
        assert(False) # implement this!

    def export_result(self):
        assert(False) # implement this!

class Word(object):
    def __init__(self, locale, key, value):
        self.locale = locale
        self.key = key
        self.value = value

class Dictionary(object):
    def __init__(self, locale, category=None):
        self.locale = locale
        self.category = category
        self.words = {}

    def append(self, word):
        self.words[word.key] = word

class Dictset(object):
    def __init__(self):
        self.dictset = {}

    def process(self, importer):
        for word in importer.gen_words():
            try:
                dic = self.dictset[word.locale]
            except KeyError:
                self.dictset[word.locale] = Dictionary(word.locale)
                dic = self.dictset[word.locale]
            dic.append(word)

    def export(self, exporter):
        for locale, dic in self.dictset.iteritems():
            yield dic.locale, exporter.export(dic)

class StringsExporter(Exporter):
    def __init__(self, dirname=None):
        self.dirname = dirname

    def export_init(self, dictionary):
        self.outs = []

    def export_word(self, dictionary, word):
        out = '"{key}" = "{value}";'.format(key=word.key.replace('"',r'\"'), value=word.value.replace('"',r'\"'))
        self.outs.append(out)

    def export_final(self, dictionary):
        self.output = '\n'.join(self.outs)
        if self.dirname:
            print self.dirname
            path_comps = self.dirname.split('/')
            filename = path_comps[-1]
            path_comps = path_comps[:-1] + [dictionary.locale + '.lproj']
            dirname = '/'.join(path_comps)
            try:
                os.mkdir(dirname)
            except OSError:
                pass
            f = open(dirname + '/' + filename + '.strings', 'w')
            self.result = 'write to ' + filename
            self.result += ' : ' + str(f.write(self.output))
        else:
            self.result = self.output

    def export_result(self):
        return self.result
