import bz2
import spacy

print('Loading model')
nlp = spacy.load('es')
docs = []

print('Procesing text')
with bz2.open('extracted/AA/wiki_01.bz2', 'rt') as inputfile:
	line = inputfile.readline()
	while line:
		docs.append(nlp(line))
		line = inputfile.readline()

print('Selecting sentences')
docs = [doc for doc in docs if len(doc) > 10 and len(doc) < 40 and doc[0].text[0].isupper()]

print(docs)

