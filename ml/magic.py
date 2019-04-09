import sys
import logging
from random import shuffle, randint, sample

import numpy
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.utils import Sequence
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.callbacks import EarlyStopping, TensorBoard, ModelCheckpoint
from tensorflow.keras.layers import Conv1D, Dense, Flatten, GRU, AveragePooling1D
from tensorflow.keras.layers import Embedding, Dropout, concatenate, Input, Bidirectional

from utils import sample_line


def cnn_concat_model(vocab_size,
	maxlen,
	embedding_dim=100, 
	filter_sizes=(1, 2, 3), 
	n_filters=(25, 50, 100),
	n_denses=2,
	dense_neurons=50,
	dropout_ratio=0.2):
	in_layer = Input(shape=(maxlen, )) 
	embedding = Embedding(input_dim=vocab_size, output_dim=embedding_dim)(in_layer)
	convs_list = [Conv1D(n, size, activation='relu', padding='same')(embedding)
			for n, size in zip(n_filters, filter_sizes)]
	if len(filter_sizes) > 1:
		convs = concatenate(convs_list)
	else:
		convs = convs_list[0]
	dense = Dense(dense_neurons, activation='relu')(Flatten()(convs))
	drop = Dropout(dropout_ratio)(dense)
	for i in range(n_denses-1):
		dense = Dense(dense_neurons, activation='relu')(drop)
		drop = Dropout(dropout_ratio)(dense)
	out_layer = Dense(1, activation='sigmoid')(drop)
	model = Model(inputs=in_layer, outputs=out_layer)
	model.compile(optimizer='adam',
				loss='binary_crossentropy',
				metrics=['binary_accuracy'])
	return model


def callbacks(name='modelito'):
	"""Useful callbacks for Keras model's fit."""
	early_stop = EarlyStopping(
		monitor='val_loss',
		min_delta=0,
		patience=4,
		verbose=1, 
		mode='auto')
	tensor_board = TensorBoard(
		log_dir='models/'+name+'/logs',
		histogram_freq=0, 
		write_graph=True, 
		write_images=True)
	checkpoint = ModelCheckpoint(
		'models/'+ name + '/{epoch:02d}-{val_loss:.4f}.h5',
		monitor='val_loss',
		verbose=0,
		save_best_only=True,
		save_weights_only=False,
		mode='auto',
		period=1)
	return [early_stop, tensor_board, checkpoint]


class TextSequence(Sequence):
	"""Implemented Keras Sequence Class.
	
	Read keras.io/utils/ for more info
	This class returns double the batch_size data, possible refactor.

	Attributes:
		lines: Cleaned strings ("the quick brown fox jumps over the lazy dog").
		tokenizer: Keras's already fit Tokenizer.
		all_words_list: List of every word in corpus (including repetitions).
		batch_size: Number of cleaned lines to process and return.
		minlen: Minimum lenght in words for lines to be sampled.
		maxlen: Maximum lenght in words for lines to be sampled.
		p: probability distribution of a line having from minlen to maxlen words.
	"""

	def __init__(self, lines, tokenizer, all_words_list, batch_size, minlen, maxlen, p):
		self.lines = lines
		self.tokenizer = tokenizer
		self.all_words_list = all_words_list
		self.batch_size = batch_size
		self.minlen = minlen
		self.maxlen = maxlen
		self.p = p

	def __len__(self):
		"""Returns number of iterations (length of data / batch size)"""
		return int(len(self.lines)/self.batch_size)

	def __getitem__(self, idx):
		"""Transforms and returns the data to train.

		Transform means:
			- Generating target data (y).
			- Generating and transforming random sentences.
			- Processing and padding input data (X).

		Args:
			idx: th batch to be returned.
		"""
		logging.debug('Getting item {}'.format(idx + 1))
		batch_y = [1]*self.batch_size + [0]*self.batch_size

		raw_X = self.lines[idx * self.batch_size:(idx + 1) * self.batch_size]
		raw_X += [sample_line(
				self.all_words_list, 
				numpy.random.choice(numpy.arange(self.minlen, self.maxlen+1), p=self.p)
			) for i in range(self.batch_size)]
		X = self.tokenizer.texts_to_sequences(raw_X)
		
		z = list(zip(X, batch_y))
		shuffle(z)
		X, y = (list(t) for t in zip(*z))
		return pad_sequences(X, self.maxlen), y