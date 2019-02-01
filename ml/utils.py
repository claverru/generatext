import os
import random
from itertools import chain
from collections import Counter


def load_all_lines(folder_path='../text/cleaned/'):
	"""Read and return every line in every file in folder_path together."""
	return list(chain.from_iterable(
			[open(folder_path+file_name, 'r').readlines() for file_name in os.listdir(folder_path)]))


def reduce_lines(lines, n_gram, n_common):
	grams = multiple_n_grams(lines, n_gram)
	c = Counter(grams)
	grams_to_check = [' '.join(gram_count[0]) for gram_count in c.most_common(n_common)]
	return [line for line in set(lines) if 
			not any(gram in line for gram in grams_to_check)]


def sample_line(all_words_list, n):
	"""Return a whole string line from sample_list"""
	return ' '.join(sample_list(all_words_list, n))


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
