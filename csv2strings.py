import localization

import csv
import re

import sys

if len(sys.argv) <= 1:
    sys.stderr.write('Input csv file as parameter\n')
    exit()

class CSVImporter(localization.Importer):
    def __init__(self, filename, **opt):
        f = open(filename, 'r')
        self.reader = csv.reader(f, **opt)

    def gen_words(self):
        order = self.reader.next()
        key_index = order.index('key')
            
        locales = []
        for i, locale in enumerate(order):
            m1 = re.match('^[a-z][a-z]$', locale)
            m2 = re.match('^[a-z][a-z]-[A-Z][A-Z]$', locale)
            if not m1 and not m2:
                continue
            locales.append((i, locale))

        for row in self.reader:
            key = row[key_index]
            for i, locale in locales:
                if not row[i]:
                    continue
                yield localization.Word(locale, key, row[i])


dictset = localization.Dictset()
infilename = sys.argv[1]
print 'Input:', infilename
importer = CSVImporter(infilename)

outfilename = sys.argv[2] if len(sys.argv) > 2 else infilename
exporter = localization.StringsExporter(outfilename)
dictset.process(importer)
print 'Result:'
for locale, result in dictset.export(exporter):
    print locale, result
