import os
from itertools import chain
import random


def load_all_lines(folder_path):
	"""Read and return every line in every file in folder_path together."""
	return list(chain.from_iterable(
			[open(folder_path+file_name, 'r').readlines() for file_name in os.listdir(folder_path)]
		))


def sample_line(all_words_list, n):
	"""Return a whole string line from sample_list"""
	return ' '.join(sample_list(all_words_list, n))


def sample_list(all_words_list, n):
	"""Return a random list of words picked by sample_word."""
	return [sample_word(all_words_list) for i in range(n)]


def sample_word(all_words_list):
	"""Random pick from list."""
	return random.choice(all_words_list)

