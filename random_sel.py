import spacy
import random

nlp = spacy.load('es')

word_list = []

[word_list.append(word) for word in nlp.vocab.strings]

print(random.choice(word_list).lower())