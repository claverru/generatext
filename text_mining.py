import bz2
import spacy
import os


print('Loading model')
nlp = spacy.load('es')
docs = []

folders = 0
files = 0
lines = 0
useful_sentences = 0


def is_useful(doc):
	return len(doc) > 7 and len(doc) < 21 and doc[0].text[0].isupper()


print('Procesing text and selecting docs')
for subdirectory_name in os.listdir('extracted'):
	for file_name in os.listdir('extracted/{}'.format(subdirectory_name)):
		with bz2.open('extracted/{}/{}'.format(subdirectory_name, file_name), 'rt') as inputfile:
			line = inputfile.readline()
			while line:
				doc = nlp(line)
				if is_useful(doc):
					docs.append(doc)
					useful_sentences += 1
				lines += 1
				print('Folders: {}, Files: {}, Lines: {}, Useful sentences: {}'.format(folders, files, lines, useful_sentences), end='\r')
				line = inputfile.readline()
		files += 1
	folders += 1

'''
with bz2.open('extracted/AA/wiki_01.bz2', 'rt') as inputfile:
	line = inputfile.readline()
	while line:
		doc = nlp(line)
		if is_useful(doc):
			docs.append(doc)
			useful_sentences += 1
		lines += 1
		print('Folders: {}, Files: {}, Lines: {}, Useful sentences: {}'.format(folders, files, lines, useful_sentences), end='\r')
		line = inputfile.readline()
'''

with open('sentences.txt', 'w') as file:
	for doc in docs:
		file.write(doc.text)
