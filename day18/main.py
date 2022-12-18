from collections import deque
import numpy as np

cubes = set()

with open("input.txt") as f:
	for line in f.readlines():
		preparedTuple = tuple(int(val) for val in line.split(',')) # a vec2 that's easier to loop through
		cubes.add(preparedTuple)

facesToCheck = (
	(1, 0, 0),
    (-1, 0, 0),
    (0, 1, 0),
    (0, -1, 0),
    (0, 0, 1),
    (0, 0, -1),
)

def getExposed(cubes):
	exposed = 0

	for x, y, z in cubes:
		for cx, cy, cz in facesToCheck:
			if (x + cx, y + cy, z + cz) not in cubes:
				exposed += 1

	return exposed

print('part 1', getExposed(cubes))

adjacentFaces = [
    np.array([1,0,0]),
    np.array([0, 1, 0]),
    np.array([0, 0, 1]),
    np.array([-1,0,0]),
    np.array([0, -1, 0]),
    np.array([0, 0, -1]),
]

# need to give one unit of extra space for the flood fill to navigate.
extreme_coords = [
    max(p[0] for p in cubes) + 1,
    max(p[1] for p in cubes) + 1,
    max(p[2] for p in cubes) + 1,
    min(p[0] for p in cubes) - 1,
    min(p[1] for p in cubes) - 1,
    min(p[2] for p in cubes) - 1,
]

def continueFill(x, y, z): # should continue fill
    return extreme_coords[0] >= x >= extreme_coords[3] and extreme_coords[1] >= y >= extreme_coords[4] and extreme_coords[2] >= z >= extreme_coords[5]

surfaceArea = 0
explored = set()
queue = deque([(1, 0, 0)])

while queue:
    node = queue.popleft()

    if continueFill(*node):
        for aa in adjacentFaces:
            neighbor = tuple(node + aa) # get the neighbor
            if neighbor in cubes:
                surfaceArea += 1
            elif neighbor not in explored:
                explored.add(neighbor) # mark this as explored
                queue.append(neighbor)

print('part 2', surfaceArea)