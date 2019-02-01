from itertools import product, combinations, chain


n_conv_layers = range(2, 4)
filter_sizes = chain.from_iterable(combinations(range(1, 4), n) for n in n_conv_layers)
n_filters = chain.from_iterable(combinations((25, 50, 100), n) for n in n_conv_layers)
embedding_dim = range(50, 151, 50)
n_denses = range(1, 4)
dense_neurons = range(25, 101, 25)
dropout = range(10, 51, 10)
p = product(embedding_dim, 
		filter_sizes, 
		n_filters,
		n_denses, 
		dense_neurons,
		dropout)	
for e in p:
	print(e)
	print()
