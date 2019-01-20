import sys
import logging
from time import time
from collections import Counter
from random import sample, shuffle, randint, choice

from utils import load_all_lines
from magic import cnn_concat_model, TextSequence, callbacks
sys.path.append('../text')
import counter
from constants import LOG_FORMAT


VAL_RATIO = 0.1
BATCH_SIZE = 128
EPOCHS = 50


def before_starting():
	"""Previous stuff before running model train."""
	c = counter.load_object('../text/counter')
	indexed = sorted(c + Counter(['-']))
	lines = load_all_lines('../text/cleaned/')
	shuffle(lines)
	index = int(len(lines)*VAL_RATIO)
	model = cnn_concat_model(len(indexed), 50, 20)
	return list(c.elements()), indexed, lines[index:], lines[-index:], model


if __name__ == '__main__':
	logging.basicConfig(format=LOG_FORMAT, level=logging.INFO)
	every_word_list, indexed, train, val, model = before_starting()
	train_sequence = TextSequence(
		train, BATCH_SIZE, every_word_list, indexed, 20)
	val_sequence = TextSequence(
		val, BATCH_SIZE, every_word_list, indexed, 20)
	model.summary()
	model.fit_generator(
		train_sequence, 
		validation_data=val_sequence, 
		# steps_per_epoch=STEPS,
		# validation_steps=1,
		epochs=EPOCHS,
		use_multiprocessing=True,
		workers=12, 
		shuffle=False,
		callbacks=callbacks()
		)
	model.save('models/model_{}.h5'.format(round(time.time())))
