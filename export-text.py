import fnmatch
import os
import xlsxwriter
import collections
import sys, getopt

texts = {}

#Command Line Arguments
inputfile = ''
outputfile = 'lang.xlsx'
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
#print 'Input file is "', inputfile
print 'Output file is "', outputfile

#walk
for root, dirnames, filenames in os.walk('./'):
    for filename in fnmatch.filter(filenames, '*.strings'):
    	dirs = root.split("/")
    	lang = dirs[len(dirs)-1]
    	if not filename in texts:
    		texts[filename] = {}

    	if not lang in texts[filename]:
    		texts[filename][lang] = {}

    	with open(os.path.join(root, filename)) as f:
    		content = f.readlines()
    		for item in content:
    			parts = item.split("=")
                        print parts
    			if (len(parts) == 2):
	    			key = parts[0].strip()[1:-1]
	    			value = parts[1].strip()[1:-2]
	    			texts[filename][lang][key] = value
                                print value

#export excels file
COL = []
for i in range(ord('A'), ord('Z') + 1):
	COL.append(chr(i))
for i in range(ord('A'), ord('Z') + 1):
	COL.append('A' + chr(i))


workbook = xlsxwriter.Workbook(outputfile)
for sheet in texts:
	worksheet = workbook.add_worksheet(sheet)
	langKeylist = texts[sheet].keys()
	langKeylist.sort()
	lang_index = 1

	allTextInLang = []
	allTextInLangDict = {}

	for lang in langKeylist:
		col = COL[lang_index] + "1"
		worksheet.write(col, lang)
		lang_index += 1

		for key in texts[sheet][lang]:
			if not allTextInLangDict.has_key(key):
				allTextInLangDict[key] = True
				allTextInLang.append(key)
	allTextInLang.sort()

	for i in range(len(allTextInLang)):
		_key = allTextInLang[i]
		worksheet.write(COL[0] + `(i+2)`, _key.decode('utf-8', 'ignore'))
		for j in range(len(langKeylist)):
			_lang = langKeylist[j]
			if texts[sheet][_lang].has_key(_key):
				worksheet.write(COL[j + 1] + `(i+2)`, texts[sheet][_lang][_key].decode('utf-8', 'ignore'))



workbook.close()
