import random

def sample(nlp, n_samples, min, max):
	"""Texts sampling.

	Retrieves n randomly chosen samples from min to max number of strings (words, marks, etc.).

	Args:
		nlp: spacy nlp (nlp = spacy.load('some_language'))
		n: number of samples
		min: 
		max: 

		A list of lists of w
	Returns:ords and/or marks:

		[['Hello', 'world', '!'], ['Bye, world, '!''], ['More', 'words', 'than', 'before', '.']]
	""" 
	vocabulary = [string.text.lower() for string in nlp.vocab]
	result = []
	n_words = 0
	for _ in range(n_samples):
		n_words = random.randint(min, max)
		sample = []
		for _ in range(n_words):
			sample.append(random.choice(vocabulary))
		result.append(sample)
	return result