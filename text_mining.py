import bz2
import spacy
import os

def is_useful(doc, min=7, max=21):
	return len(doc) > min and len(doc) < max and doc[0].text[0].isupper()

def run(nlp):
	docs = []
	folders = 0
	files = 0
	lines = 0
	useful_sentences = 0
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
	with open('sentences.txt', 'w') as file:
		for doc in docs:
			file.write(doc.text)

def run_in_one(nlp, document_path='extracted/AA/wiki_01.bz2'):
	"""Find sentences with characteristics defined in is_useful in one document."""
	docs = []
	folders = 0
	files = 0
	lines = 0
	useful_sentences = 0
	print('DEBUG: Procesing text and selecting docs in {}'.format(document_path))	
	with bz2.open(document_path, 'rt') as inputfile:
		line = inputfile.readline()
		while line:
			doc = nlp(line)
			if is_useful(doc):
				docs.append(doc)
				useful_sentences += 1
			lines += 1
			print('INFO: Folders: {}, Files: {}, Lines: {}, Useful sentences: {}'.format(folders, files, lines, useful_sentences), end='\r')
			line = inputfile.readline()
	print()
	return docs


if __name__ == "__main__":
	print('INFO: Loading model')
	nlp = spacy.load('es')
	results = run_in_one(nlp)
	print('DEBUG:')
	print(results)
