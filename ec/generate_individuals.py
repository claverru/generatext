import sys
import random
from collections import Counter
import multiprocessing

from deap import creator, base, tools, algorithms
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

sys.path.append('../ml')
from utils import word_list_to_sequence
sys.path.append('../text')
from counter import load_object


c = load_object('../text/counter')
listed = list(c.elements()) # every word list including repetitions
indexed = sorted(c + Counter(['-']))
model = load_model('../ml/models/{}'.format('05-0.00.h5'))



creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
# pool = multiprocessing.Pool()
# toolbox.register("map", pool.map)


def random_word_index(listed):
	return indexed.index(random.choice(listed))


toolbox.register("attr_bool", random_word_index, listed)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, n=random.randint(4, 20))
toolbox.register("population", tools.initRepeat, list, toolbox.individual)


def evaluate(individual):
	if len(individual) < 4 or len(individual) > 20:
		return 0.,
	return model.predict(pad_sequences([individual], 20))[0], 


def mutate(individual, indpb):
	for i in range(len(individual)):
		if random.random() <= indpb:
			individual[i] = random_word_index(listed)
	return individual,


def mate(ind1, ind2):
	n1 = random.randint(1, 3) # Number of elements from 1 
	r1 = random.randint(0, len(ind1)-n1-1) # first th element to be picked from 1
	n2 = random.randint(1, 3)
	r2 = random.randint(0, len(ind1)-n2-1)
	ind1[r1:r1+n1], ind2[r2:r2+n2] = ind2[r2:r2+n2], ind1[r1:r1+n1]
	return ind1, ind2


toolbox.register("evaluate", evaluate)
toolbox.register("mate", mate)
toolbox.register("mutate", mutate, indpb=0.2)
toolbox.register("select", tools.selStochasticUniversalSampling)# , tournsize=3)

population = toolbox.population(n=500)

NGEN=1000

for gen in range(NGEN):
	offspring = algorithms.varAnd(population, toolbox, cxpb=0.5, mutpb=0.4)
	fits = toolbox.map(toolbox.evaluate, offspring)
	for fit, ind in zip(fits, offspring):
		ind.fitness.values = fit
	population = toolbox.select(offspring, k=len(population)-250)
	population += toolbox.population(n=250)
	best = ' '.join(indexed[i] for i in tools.selBest(population, k=1)[0])
	print("Generation {}/{}: {}".format(gen+1, NGEN, best))

top10 = tools.selBest(population, k=10)


"""

l = [0,0,0,0,0,0,0]
k = [1,1,1,1,1,1,1,1,1,1]
n1 = random.randint(1, 3)
r1 = random.randint(0, len(l)-n1-1)
n2 = random.randint(1, 3)
r2 = random.randint(0, len(k)-n2-1)
l[r1:r1+n1], k[r2:r2+n2] = k[r2:r2+n2], l[r1:r1+n1]
l
k
"""