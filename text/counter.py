import os
import pickle
import logging
from random import randrange, choice
from functools import reduce
from collections import Counter
from itertools import chain, islice

from constants import LOG_FORMAT, CLEANED_FOLDER


def save_object(name, object):
	"""Saves an object to a pickle."""
	with open('{}.pickle'.format(name), 'wb') as handle:
	    pickle.dump(object, handle, protocol=pickle.HIGHEST_PROTOCOL)


def load_object(name):
	"""Loads an object from a pickle."""
	with open('{}.pickle'.format(name), 'rb') as handle:
	    return pickle.load(handle)


def create_counter(folder_path):
	"""Creates words Counter from every text file in folder_path."""
	logging.info(folder_path)
	return reduce(
		(lambda x, y: x+y),
		(create_counter_one(folder_path + file_name) for file_name in os.listdir(folder_path))
		)


def create_counter_one(file_path):
	"""Create words Counter from one text file."""
	logging.info(file_path)
	with open(file_path, 'r') as file:
		return Counter(list(chain.from_iterable(
			[line.split() for line in file.readlines()]
			)))


# def sample_word(c):
# 	"""Weighed random picks from Counter c."""
# 	return next(islice(c.elements(), randrange(sum(c.values())), None))


def sample_list(from_here, n):
	"""Return a random list of words picked by sample_word."""
	return [sample_word(from_here) for i in range(n)]


def sample_word(listed):
	"""Random pick from list."""
	return choice(listed)


if __name__ == '__main__':
	logging.basicConfig(format=LOG_FORMAT, level=logging.INFO)
	result = create_counter(CLEANED_FOLDER)
	logging.info(result.most_common(20))
	save_object('counter', result)