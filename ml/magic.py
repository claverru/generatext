import sys
import logging
from random import shuffle, randint

from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.utils import Sequence
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.callbacks import EarlyStopping, TensorBoard, ModelCheckpoint
from tensorflow.keras.layers import Conv1D, Dense, Flatten, GRU
from tensorflow.keras.layers import Embedding, Dropout, concatenate, Input, Bidirectional

from utils import sample_line


def cnn_concat_model(vocab_size, embedding_dim, maxlen):
	in_layer = Input(shape=(maxlen, )) 
	embedding = Embedding(input_dim=vocab_size, output_dim=embedding_dim)(in_layer)
	st_conv3 = Conv1D(50, 3, activation='relu', padding='same')(embedding)
	st_conv2 = Conv1D(100, 2, activation='relu', padding='same')(embedding)
	concat = concatenate([st_conv3, st_conv2])
	nd_conv = Conv1D(100, 3, activation='relu', padding='valid')(concat)
	rd_conv = Conv1D(100, 2, activation='relu', padding='valid')(nd_conv)
	st_drop = Dropout(0.3)(Flatten()(rd_conv))
	dense = Dense(50, activation='relu')(st_drop)
	nd_drop = Dropout(0.3)(dense)
	out_layer = Dense(1, activation='sigmoid')(nd_drop)
	model = Model(inputs=in_layer, outputs=out_layer)
	model.compile(optimizer='adam',
				loss='binary_crossentropy',
				metrics=['binary_accuracy'])
	return model


def rnn_model(vocab_size, embedding_dim, maxlen):
	in_layer = Input(shape=(maxlen, )) 
	embedding = Embedding(input_dim=vocab_size, output_dim=embedding_dim, mask_zero=True)(in_layer)
	st_rnn = Bidirectional(GRU(100, return_sequences=True))(embedding)
	nd_rnn = Bidirectional(GRU(100))(st_rnn)
	st_drop = Dropout(0.3)(nd_rnn)
	dense = Dense(50, activation='relu')(st_drop)
	nd_drop = Dropout(0.3)(dense)
	out_layer = Dense(1, activation='sigmoid')(nd_drop)
	model = Model(inputs=in_layer, outputs=out_layer)
	model.compile(optimizer='adam',
				loss='binary_crossentropy',
				metrics=['binary_accuracy'])
	return model

def callbacks(checkpoint_name='modelito'):
	"""Useful callbacks for Keras model's fit."""
	early_stop = EarlyStopping(
		monitor='val_loss',
		min_delta=0,
		patience=2,
		verbose=1, 
		mode='auto')
	tensor_board = TensorBoard(
		log_dir='logs/' + checkpoint_name + '/',
		histogram_freq=0, 
		write_graph=True, 
		write_images=True)
	checkpoint = ModelCheckpoint(
		'models/' + checkpoint_name + '{epoch:02d}-{val_loss:.2f}.h5',
		monitor='val_loss',
		verbose=0,
		save_best_only=True,
		save_weights_only=False,
		mode='auto',
		period=1)
	return [early_stop, tensor_board, checkpoint]


class TextSequence(Sequence):
	"""Implemented Keras Sequence Class.
	
	Read keras.io/utils/ for mas info
	This class returns double the batch_size data, possible refactor.

	Attributes:
		lines: Cleaned strings ("the quick brown fox jumps over the lazy dog").
		tokenizer: Keras's already fit Tokenizer.
		all_words_list: List of every word in corpus (including repetitions).
		batch_size: Number of cleaned lines to process and return.
		minlen: Minimum lenght in words for lines to be sampled.
		maxlen: Maximum lenght in words for lines to be sampled.
	"""

	def __init__(self, lines, tokenizer, all_words_list, batch_size, minlen, maxlen):
		self.lines = lines
		self.tokenizer = tokenizer
		self.all_words_list = all_words_list
		self.batch_size = batch_size
		self.minlen = minlen
		self.maxlen = maxlen

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
		X = self.tokenizer.texts_to_sequences(
			self.lines[idx * self.batch_size:(idx + 1) * self.batch_size] + \
			[sample_line(self.all_words_list, randint(self.minlen, self.maxlen)) for i in range(self.batch_size)]
		)
		
		z = list(zip(X, batch_y))
		shuffle(z)
		X, y = (list(t) for t in zip(*z))
		return pad_sequences(X, self.maxlen), y