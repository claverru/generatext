import os
import sys
import time
import logging
from random import sample
from itertools import combinations, product, chain

from utils import get_lines, get_tokenizer, p_distribution, ordereddict_to_list
from magic import *
sys.path.append('../text')
from constants import LOG_FORMAT


VAL_RATIO = 0.1
BATCH_SIZE = 1024
EPOCHS = 50


def grid_search():
	"""Grid Search for models' architecture."""
	n_conv_layers = range(2, 4)
	filter_sizes = chain.from_iterable(combinations(range(1, 4), n) for n in n_conv_layers)
	n_filters = chain.from_iterable(combinations(range(25, 101, 25), n) for n in n_conv_layers)
	embedding_dim = range(100, 151, 50)
	n_denses = range(1, 3)
	dense_neurons = range(50, 101, 50)
	dropout = range(25, 51, 25)
	return product(embedding_dim, 
		filter_sizes, 
		n_filters,
		n_denses, 
		dense_neurons,
		dropout)


def create_keras_sequences(data_path='../text/cleaned/'):
	"""Previous stuff before running model train."""
	logging.info('Loading and wrangling data.')
	lines = get_lines(data_path)
	tokenizer = get_tokenizer(lines)
	all_words_list = ordereddict_to_list(tokenizer.word_counts) 
	p = p_distribution(lines)
	index = int(len(lines)*VAL_RATIO)
	return (TextSequence(lines[:-index], tokenizer, all_words_list, BATCH_SIZE, 8, 20, p),
		TextSequence(lines[-index:], tokenizer, all_words_list, BATCH_SIZE, 8, 20, p),
		len(tokenizer.word_index)+1)


def train(vocab_size, maxlen, p, train_s, val_s):
	name = str(p)
	logging.info('Training new model')
	if name not in os.listdir('models'):
		model = cnn_concat_model(vocab_size=vocab_size, 
			maxlen=maxlen,
			embedding_dim=p[0], 
			filter_sizes=p[1], 
			n_filters=p[2],
			n_denses=p[3], 
			dense_neurons=p[4],
			dropout_ratio=p[5]/100)
		model.summary()
		os.mkdir('models/{}'.format(name))
		dropout = next(filter(lambda layer: 'dropout' in layer.name, model.layers)).get_config()['rate']
		with open('models/'+name+'/architecture.txt', 'w') as file:
			model.summary(print_fn=lambda x: file.write(x + '\n'))
			file.write('\n')
			file.write('Dropout: {}'.format(dropout))
		model.fit_generator(train_s, 
			validation_data=val_s,
			epochs=EPOCHS,
			use_multiprocessing=True,
			workers=12, 
			shuffle=False,
			callbacks=callbacks(name))
		del model
	else:
		logging.info('Model with {} already trained'.format(name))


def main():
	train_s, val_s, vocab_size = create_keras_sequences()
	p = grid_search()
	for model_conf in p:
		train(vocab_size, 20, model_conf, train_s, val_s)


if __name__ == '__main__':
	logging.basicConfig(format=LOG_FORMAT, level=logging.INFO)
	main()
