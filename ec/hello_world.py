import random
from deap import creator, base, tools, algorithms
from string import printable
from fuzzywuzzy import fuzz


objective = "Hello world!"

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

toolbox.register("attr_bool", random.choice, printable)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, n=len(objective))
toolbox.register("population", tools.initRepeat, list, toolbox.individual)


def evaluate(individual):
	val = 0
	for i in range(len(individual)):
		if individual[i] == objective[i]:
			val += 1
	return val, 


def mutate(individual, indpb):
	for i in range(len(individual)):
		if random.random() <= indpb:
			individual[i] = random.choice(printable)
	return individual,


toolbox.register("evaluate", evaluate)
toolbox.register("mate", tools.cxUniform, indpb=0.1)
toolbox.register("mutate", mutate, indpb=0.2)
toolbox.register("select", tools.selTournament, tournsize=3)

population = toolbox.population(n=300)

NGEN=1000

for gen in range(NGEN):
	offspring = algorithms.varAnd(population, toolbox, cxpb=0.5, mutpb=0.4)
	fits = toolbox.map(toolbox.evaluate, offspring)
	for fit, ind in zip(fits, offspring):
		ind.fitness.values = fit
	population = toolbox.select(offspring, k=len(population))
	print("Generación {}/{}: {}".format(gen+1, NGEN, tools.selBest(population, k=1)[0]))

top10 = tools.selBest(population, k=10)