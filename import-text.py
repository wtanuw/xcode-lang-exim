import fnmatch
import os
from xlrd import open_workbook
import codecs
import sys, getopt

texts = {}
docs = {}

def safeGet(v, keys):
    root = v
    for k in keys:
        if k in root:
            root = root[k]
        else:
            return None
    return root

#Command Line Arguments
inputfile = 'lang.xlsx'
outputfile = ''
try:
   opts, args = getopt.getopt(sys.argv[1:],"hi:o:",["ifile=","ofile="])
except getopt.GetoptError:
   print 'test.py -i <inputfile> -o <outputfile>'
   sys.exit(2)
for opt, arg in opts:
   if opt == '-h':
      print 'test.py -i <inputfile> -o <outputfile>'
      sys.exit()
   elif opt in ("-i", "--ifile"):
      inputfile = arg
   elif opt in ("-o", "--ofile"):
      outputfile = arg
print 'Input file is "', inputfile
#print 'Output file is "', outputfile

#os.walk
for root, dirnames, filenames in os.walk('./'):
    for filename in fnmatch.filter(filenames, '*.strings'):
        dirs = root.split("/")
        lang = dirs[len(dirs)-1]
        if not filename in texts:
            texts[filename] = {}
        docs[lang + filename] = os.path.join(root, filename)

        if not lang in texts[filename]:
            texts[filename][lang] = {}

        with open(os.path.join(root, filename)) as f:
            content = f.readlines()
            for item in content:
                parts = item.split("=")
                if (len(parts) == 2):
                    key = parts[0].strip()[1:-1]
                    value = parts[1].strip()[1:-2]
                    texts[filename][lang][key] = value.decode('utf-8', 'ignore')

changes = {}

#import excels file
wb = open_workbook(inputfile)
for s in wb.sheets():
    langs = []
    for col in range(1, s.ncols):
        value  = s.cell(0,col).value
        langs.append(value)
    for row in range(1, s.nrows):
        key = s.cell(row,0).value
        for col in range(1, s.ncols):
            lang = langs[col-1]
            oldValue = safeGet(texts, [s.name, lang, key])
            newValue = s.cell(row,col).value
            if (oldValue != newValue):
                doc = docs[lang + s.name]
                if not doc in changes:
                    changes[doc] = {}
                changes[doc][key] = newValue

for filepath in changes:
    with open(filepath) as f:
        content = f.readlines()
        for i in range(len(content)):
            line = content[i]
            parts = line.split("=")
            if (len(parts) == 2):
                key = parts[0].strip()[1:-1]
                if key in changes[filepath]:
                    out = "\"" + key + "\" = \"" + changes[filepath][key] + "\";\n"
                    content[i] = out.encode('utf-8')
        output = ''.join([x for x in content]).decode('utf-8', 'ignore')
        with codecs.open(filepath, 'w', 'utf-8') as f2: f2.write(output)
