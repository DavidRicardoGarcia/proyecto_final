import itertools

stuff = [1, 2, 3]

for subset in itertools.permutations(stuff):
        print(subset)