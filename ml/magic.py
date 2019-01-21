import sys
import logging
from random import shuffle, randint

from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.utils import Sequence
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.callbacks import EarlyStopping, TensorBoard, ModelCheckpoint
from tensorflow.keras.layers import Conv1D, Dense, Embedding, Dropout, Flatten, Input, concatenate

from utils import texts_to_sequences, word_list_to_sequence
sys.path.append('../text')
import counter


def cnn_concat_model(vocab_size, embedding_dim, maxlen):
	in_layer = Input(shape=(maxlen, )) 
	embedding = Embedding(input_dim=vocab_size, output_dim=embedding_dim)(in_layer)
	st_conv2 = Conv1D(100, 2, activation='relu', padding='same')(embedding)
	st_conv3 = Conv1D(50, 3, activation='relu', padding='same')(embedding)
	concat = concatenate([st_conv3, st_conv2])
	nd_conv = Conv1D(25, 2, activation='relu', padding='same')(concat)
	flatten = Flatten()(nd_conv)
	st_drop = Dropout(0.1)(flatten)
	dense = Dense(50, activation='relu')(st_drop)
	nd_drop = Dropout(0.1)(dense)
	out_layer = Dense(1, activation='sigmoid')(nd_drop)
	model = Model(inputs=in_layer, outputs=out_layer)
	model.compile(optimizer='adam',
				loss='binary_crossentropy',
				metrics=['binary_accuracy'])
	return model


def callbacks(checkpoint_name='models/{epoch:02d}-{val_loss:.2f}.h5'):
	"""Useful callbacks for Keras model's fit."""
	early_stop = EarlyStopping(
		monitor='val_loss',
		min_delta=0,
		patience=0,
		verbose=0, 
		mode='auto')
	tensor_board = TensorBoard(
		log_dir='logs', 
		histogram_freq=0, 
		write_graph=True, 
		write_images=True)
	checkpoint = ModelCheckpoint(
		checkpoint_name,
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
		lines: Cleaned strings ("the quick brown fox jumps over the lazy dog")
		batch_size: Number of cleaned lines to process and return.
		indexed: Every word in all lines list (repeated words too).
		maxlen: Maximum length in words to pad.
    """

	def __init__(self, lines, batch_size, c, indexed, maxlen):
		self.lines = lines
		self.batch_size = batch_size
		self.c = c
		self.indexed = indexed
		self.maxlen = maxlen

	def __len__(self):
		"""Returns number of iterations (length of data / batch size)"""
		return int(len(self.lines)/self.batch_size)

	def __getitem__(self, idx):
		"""Transforms and returns the data to train.

		Transform means:
			- Generating target data (y).
			- Generating and transforming random sentences.
			- Processing and pad input data (X).

		Args:
			idx: th batch to be returned.
		"""
		logging.debug('Getting item {}'.format(idx + 1))
		batch_y = [1]*self.batch_size + [0]*self.batch_size
		good_x = texts_to_sequences(
			self.lines[idx * self.batch_size:(idx + 1) * self.batch_size],
			self.indexed)
		bad_x = [word_list_to_sequence(
			counter.sample_list(self.c, randint(4, 20)), 
			self.indexed) for i in range(self.batch_size)]
		
		z = list(zip(good_x+bad_x, batch_y))
		shuffle(z)
		X, y = (list(t) for t in zip(*z))
		return pad_sequences(X, self.maxlen), y