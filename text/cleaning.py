import re
import os
import sys
import logging

from unidecode import unidecode
from langdetect import detect
import spacy

from constants import *


def clean(in_path, out_path, nlp):
	logging.debug('IN')
	all_files = os.listdir(in_path)
	for file in all_files:
		# clean input files lines
		lines = read_in(in_path, file, nlp)
		# write cleaned lines in output file
		write_out(lines, out_path, file)


def read_in(path, file, nlp):
	logging.debug('IN')
	lines = []
	with open(path+file, 'r') as inputfile:
		logging.info('Cleaning {}{}'.format(path, file))
		raw_line = inputfile.readline()
		while raw_line:
			for sent in nlp(raw_line).sents:
				line = clean_line(nlp, sent.text.replace('\n', ''))
				if line != None:
					lines.append(line)
			raw_line = inputfile.readline()
	return lines


def write_out(lines, path, file):
	logging.debug('IN')
	with open(path+file, 'w') as output_file:
		logging.info('Writing {}{}'.format(path, file))
		for line in lines:
			output_file.write(line+'\n')


def decimal_numbers(line):
	"""Finds and replaces decimal numbers for unique token."""
	logging.debug(line)
	line = NUM_REG.sub(NUM_TOKEN, line)
	return line


def roman_numbers(line):
	"""Finds and replaces roman numbers when referred to centuries (spanish) for unique token."""
	logging.debug(line)
	m = R_CENT_ROMAN.search(line)
	while m:
		replacement = m.group(0)
		logging.debug('roman number found - {}'.format(replacement))
		line = line.replace(replacement, R_ROMAN.sub(NUM_TOKEN, replacement), 1)
		m = R_CENT_ROMAN.search(line)
	return line


def surrounded(line):
	"""Finds and removes <tags> and (parenthesis)."""
	logging.debug(line)
	line = TAG_REG.sub('', line)
	line = PARENTHESIS_REG.sub('', line)
	return line


def entities(nlp, line):
	"""Finds and replaces entities for unique token."""
	logging.debug(line)
	for ent in nlp(line).ents:
		logging.debug('Found entity "{}", {}'.format(ent.text, ent.label_))
		line = line.replace(ent.text, ent.label_)
	return line


def separate_tokens(line):
	"""Put white spaces in both sides of a token."""
	logging.debug(line)
	for TOKEN in TOKENS:
		line = line.replace(TOKEN, ' {} '.format(TOKEN))
	return line


def to_lower(line):
	"""Gets everything lower except the tokens."""
	logging.debug(line)
	return ' '.join([w if any(token in w for token in TOKENS) else w.lower() for w in line.split()])


def alphanumeric(line):
	logging.debug(line)
	return ' '.join(''.join([e if e.isalnum() else ' ' for e in w]) for w in line.split())


def keep(line):
	"""Decides if line goes ahead after cleaned."""
	logging.debug(line)
	word_list = line.split()
	n_words = len(word_list)
	if n_words < 4:
		return False
	n_tokens = len(list(filter(lambda x: x in TOKENS, word_list)))
	# excesive number of tokens
	return n_tokens/(n_words-1)<=TOKEN_THROW_RATIO


def clean_line(nlp, line):
	"""Cleaning pipeline."""
	logging.debug('Cleaning \"{}\"'.format(line))
	try:
		if detect(line) != 'es':
			return None
	except:
		logging.info('Cant detect language in \"{}\"'.format(line))
		return None
	line = surrounded(line)
	line = entities(nlp, line)
	line = decimal_numbers(line)
	line = roman_numbers(line)
	line = separate_tokens(line)
	line = unidecode(line)
	line = alphanumeric(line)
	line = to_lower(line)
	return line if keep(line) else None


if __name__ == '__main__':
	logging.basicConfig(format=LOG_FORMAT, level=logging.INFO)
	logging.info('Loading model - {}'.format(ES_MODEL))
	nlp = spacy.load(ES_MODEL)
	clean(MINED_FOLDER, CLEANED_FOLDER, nlp)