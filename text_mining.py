import bz2
import spacy
import os


print('Loading model')
nlp = spacy.load('es')
docs = []


"""
print('Procesing text')
with bz2.open('extracted/AA/wiki_01.bz2', 'rt') as inputfile:
	line = inputfile.readline()
	while line:
		docs.append(nlp(line))
		line = inputfile.readline()
"""

folders = 0
files = 0
lines = 0

print('Procesing text')
for subdirectory_name in os.listdir('extracted'):
	for file_name in os.listdir('extracted/{}'.format(subdirectory_name)):
		with bz2.open('extracted/{}/{}'.format(subdirectory_name, file_name), 'rt') as inputfile:
			line = inputfile.readline()
			while line:
				docs.append(nlp(line))
				lines += 1
				print('Folders: {}, Files: {}, Lines: {}'.format(folders, files, lines), end='\r')
				line = inputfile.readline()
		files += 1
	folders += 1


print('Selecting sentences')
docs = [doc for doc in docs if len(doc) > 10 and len(doc) < 40 and doc[0].text[0].isupper()]

print(docs)
