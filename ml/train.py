import sys
import logging
from time import time
from random import sample, shuffle, randint, choice

from tensorflow.keras.preprocessing.text import Tokenizer

from utils import load_all_lines
from magic import *
sys.path.append('../text')
from constants import LOG_FORMAT


VAL_RATIO = 0.1
BATCH_SIZE = 1024
EPOCHS = 50
MOLDEL_NAME = 'modelito'

def ordereddict_to_list(od):
	result = []
	for k, v in od.items():
		for i in range(v):
			result.append(k)
	return result


def before_starting():
	"""Previous stuff before running model train."""
	logging.info('Processing text and setting up utilities.')
	lines = load_all_lines('../text/cleaned/')
	tokenizer = Tokenizer(lower=False)
	tokenizer.fit_on_texts(lines)
	all_words_list = ordereddict_to_list(tokenizer.word_counts) 
	shuffle(lines)
	index = int(len(lines)*VAL_RATIO)
	train_s = TextSequence(lines[:-index], tokenizer, all_words_list, BATCH_SIZE, 4, 20)
	val_s = TextSequence(lines[-index:], tokenizer, all_words_list, BATCH_SIZE, 4, 20)
	model = cnn_concat_model(len(tokenizer.word_index)+1, 100, 20)
	return train_s, val_s, model


if __name__ == '__main__':
	logging.basicConfig(format=LOG_FORMAT, level=logging.INFO)
	train_s, val_s, model = before_starting()
	model.summary()
	model.fit_generator(
		train_s, 
		validation_data=val_s, 
		validation_steps=1,
		epochs=EPOCHS,
		use_multiprocessing=True,
		workers=12, 
		shuffle=False,
		# callbacks=callbacks(MOLDEL_NAME)
		)
	# model.save('models/{}_{}.h5'.format(MODEL_NAME, round(time())))