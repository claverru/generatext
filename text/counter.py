import os
import pickle
import logging
from random import randrange
from functools import reduce
from collections import Counter
from itertools import chain, islice

from constants import LOG_FORMAT


def save_object(name, object):
	with open('{}.pickle'.format(name), 'wb') as handle:
	    pickle.dump(object, handle, protocol=pickle.HIGHEST_PROTOCOL)


def load_object(name):
	with open('{}.pickle'.format(name), 'rb') as handle:
	    return pickle.load(handle)


def create_counter(folder_path):
	logging.info(folder_path)
	return reduce(
		(lambda x, y: x+y),
		(create_counter_one(folder_path + file_name) for file_name in os.listdir(folder_path))
		)


def create_counter_one(file_path):
	logging.info(file_path)
	with open(file_path, 'r') as file:
		return Counter(list(chain.from_iterable(
			[line.split() for line in file.readlines()]
			)))


def sample(c):
	"""Weighed random pick from Counter c."""
	return next(islice(c.elements(), randrange(sum(c.values())), None))


if __name__ == '__main__':
	logging.basicConfig(format=LOG_FORMAT, level=logging.INFO)
	result = create_counter('cleaned/')
	logging.info(result.most_common(20))
	save_object('counter', result)