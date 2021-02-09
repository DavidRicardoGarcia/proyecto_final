import pants
import math
import random

nodes = []
for _ in range(20):
  x = random.uniform(-10, 10)
  y = random.uniform(-10, 10)
  nodes.append((x, y))

def euclidean(a, b):
    return math.sqrt(pow(a[1] - b[1], 2) + pow(a[0] - b[0], 2))

world = pants.World(nodes, euclidean)

solver = pants.Solver()

solution = solver.solve(world)

print(solution.distance)
print(solution.tour)   
print(solution.path) 