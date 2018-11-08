import random
import thinc.extra.datasets
from random_sample import sample
from random import shuffle

def load_IMDB_data(limit=0, split=0.8):
    """Load data from the IMDB dataset."""
    # Partition off part of the train data for evaluation
    train_data, _ = thinc.extra.datasets.imdb()
    random.shuffle(train_data)
    train_data = train_data[-limit:]
    texts, labels = zip(*train_data)
    cats = [{'POSITIVE': bool(y)} for y in labels]
    split = int(len(train_data) * split)
    return (texts[:split], cats[:split]), (texts[split:], cats[split:])

# texts[:split][0:2] : ('...', '...', ...)
# cats[:split][0:2] : [{'POSITIVE': False}, {'POSITIVE': False}]

def data_generator(nlp, n, min, max):
	# random part
	while True:
		yield sample(nlp, n, min, max)