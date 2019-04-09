import sys
import random
import multiprocessing

import numpy
from deap import creator, base, tools, algorithms
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

sys.path.append('../ml')
from utils import *



# https://deap.readthedocs.io/en/master/api/



model = load_model('../ml/models/{}'.format(best_model_path('../ml/models')))
lines = get_lines()
tokenizer = get_tokenizer(lines)
all_words_list = ordereddict_to_list(tokenizer.word_counts) 
p = p_distribution(lines)
reverse_word_map = dict(map(reversed, tokenizer.word_index.items()))

creator.create("FitnessMax", base.Fitness, weights=(1.0, 0.25))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
# pool = multiprocessing.Pool()
# toolbox.register("map", pool.map)


def random_word_index(all_words_list):
	return tokenizer.word_index[sample_word(all_words_list)]


toolbox.register("word_index", random_word_index, all_words_list)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.word_index, 
	n=numpy.random.choice(numpy.arange(8, 21), p=p))
toolbox.register("population", tools.initRepeat, list, toolbox.individual)


def evaluate(individual):
	if len(individual) > 20 or len(individual) < 4:
		return 0., 0.
	return model.predict(pad_sequences([individual], 20))[0][0], len(set(individual))/len(individual)


def mutate(individual): # , indpb):
	for i in range(len(individual)):
		if random.random() <= 1/len(individual):
			individual[i] = random_word_index(all_words_list)
	return individual,


def mate(ind1, ind2):
	"""Swaps a random 1-to-3-words n_gram of both individuals."""
	if len(ind1) < 4 or len(ind2) < 4:
		return ind1, ind2
	n1 = random.randint(1, 3) # Number of elements from ind1 
	r1 = random.randint(0, len(ind1)-n1-1) # first th element to be picked from ind1
	n2 = random.randint(1, 3)
	r2 = random.randint(0, len(ind2)-n2-1)
	ind1[r1:r1+n1], ind2[r2:r2+n2] = ind2[r2:r2+n2], ind1[r1:r1+n1]
	return ind1, ind2


def print_individuals(individuals):
	for ind in individuals:
		print(' '.join(reverse_word_map[word] for word in ind), ind.fitness)


toolbox.register("evaluate", evaluate)
toolbox.register("mate", mate)
toolbox.register("mutate", mutate) # , indpb=0.1)
toolbox.register("select", tools.selBest) # , tournsize=3)

population = toolbox.population(n=1000)
hof = tools.HallOfFame(10)

NGEN=200

print('-'*80)
print('FIRST POPULATION')
print('-'*80)
print_individuals(population[:5])

for gen in range(NGEN):
	# Mutate and mate
	offspring = algorithms.varAnd(population, toolbox, cxpb=0.2, mutpb=0.5)

    # Evaluate individuals
	fits = toolbox.map(toolbox.evaluate, offspring)
	for fit, ind in zip(fits, offspring):
		ind.fitness.values = fit

	# Select
	population = toolbox.select(offspring, k=500)
	hof.update(population)

	# Repopulate
	population += toolbox.population(n=100)

	# Logger
	bests = tools.selBest(population, k=4)
	print('-'*80)
	print("{}/{} GENERATION:".format(gen+1, NGEN))
	print('-'*80)
	print_individuals(bests)


# top10 = tools.selBest(population, k=10)
print('-'*80)
print('HALL OF FAME: ')
print('-'*80)
print_individuals(hof)
print('-')