import os
from itertools import chain


def texts_to_sequences(lines, indexed):
	"""Transform strings into integer sequences."""
	return [text_to_sequence(line, indexed) for line in lines]


def text_to_sequence(line, indexed):
	"""Transform string to an integer sequence."""
	return word_list_to_sequence(line.split(), indexed)


def word_list_to_sequence(word_list, indexed):
	"""Transform a list of word-strings to a integer sequence."""
	return [indexed.index(word) for word in word_list]


def load_all_lines(folder_path):
	"""Read and return every line in every file in folder_path together."""
	return list(chain.from_iterable(
			[open(folder_path+file_name, 'r').readlines() for file_name in os.listdir(folder_path)]
		))