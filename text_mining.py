import bz2
import spacy
import os


def is_useful(doc, min=7, max=21):
	"""Condition function for a text document to be selected."""
	return len(doc) > min and len(doc) < max and doc[0].text[0].isupper() and not doc.text.endswith(':\n')

def mine_extracted(nlp, parent_folder_path='extracted'):
	docs = []
	print('Procesing text and selecting docs')
	for folder_name in os.listdir(parent_folder_path):
		folder_path = '{}/{}'.format(parent_folder_path, folder_name) 
		docs.append(mine_folder(nlp, folder_path))
	return docs


def mine_folder(nlp, folder_path='extracted/AA'):
	docs = []
	for document_name in os.listdir(folder_path):
		document_path = '{}/{}'.format(folder_path, document_name)
		docs.append(mine_document(nlp, document_path))
	return docs


def mine_document(nlp, document_path='extracted/AA/wiki_01.bz2'):
	"""Find sentences with characteristics defined in is_useful in one document."""
	docs = []
	with bz2.open(document_path, 'rt') as inputfile:
		line = inputfile.readline()
		while line:
			doc = nlp(line)
			if is_useful(doc):
				docs.append(doc)
				print(doc)
			line = inputfile.readline()
	return docs


if __name__ == "__main__":
	print('INFO: Loading model')
	nlp = spacy.load('es')
	results = mine_extracted(nlp)