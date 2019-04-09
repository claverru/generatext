import os
import random
import logging
from random import sample
from itertools import chain
from collections import Counter

from tensorflow.keras.preprocessing.text import Tokenizer


def get_lines(data_path='../text/cleaned/', ngram_len=9, n_ngrams=2):
	lines = reduce_lines(load_all_lines(data_path), ngram_len, n_ngrams)
	return sample(lines, len(lines))


def load_all_lines(folder_path='../text/cleaned/'):
	"""Read and return every line in every file in folder_path together."""
	return list(chain.from_iterable(
			[open(folder_path+file_name, 'r').readlines() for file_name in os.listdir(folder_path)]))


def get_tokenizer(lines):
	tokenizer = Tokenizer(lower=False)
	tokenizer.fit_on_texts(lines)
	return tokenizer


def reduce_lines(lines, n_gram, n_common):
	"""Removes certain lines in order to avoid repetitions."""
	grams = multiple_n_grams(lines, n_gram)
	c = Counter(grams)
	grams_to_check = [' '.join(gram_count[0]) for gram_count in c.most_common(n_common)]
	return [line for line in set(lines) if 
			not any(gram in line for gram in grams_to_check)]


def sample_line(all_words_list, n):
	"""Return a whole string line from sample_list"""
	return ' '.join(sample_list(all_words_list, n))
# usage:
# sample_line(all_words_list, numpy.random.choice(numpy.arange(8, 21), p=p))


def sample_list(all_words_list, n):
	"""Return a random list of words picked by sample_word."""
	return [sample_word(all_words_list) for i in range(n)]


def sample_word(all_words_list):
	"""Random pick from list."""
	return random.choice(all_words_list)


def multiple_n_grams(lines, n):
	return list(chain.from_iterable(n_grams(line, n) for line in lines))


def n_grams(line, n):
	word_list = line.split()
	return list(zip(*[word_list[i:len(word_list)-n+i+1] for i in range(n)]))


def ordereddict_to_list(od):
	result = []
	for k, v in od.items():
		for i in range(v):
			result.append(k)
	return result


def p_distribution(lines):
	c = Counter(len(line.split()) for line in lines)
	return [c[e]/len(lines) for e in sorted(c)]


def best_model_path(models_folder='models'):
	best = '1.0000.h5'
	best_folder = '()'
	for folder in os.listdir(models_folder):
			if '.txt' not in folder:
				for file in os.listdir('{}/{}'.format(models_folder, folder)):
					if '.h5' in file and file[-9:] < best[-9:]:
						best = file
						best_folder = folder
	return best_folder + '/' + best 