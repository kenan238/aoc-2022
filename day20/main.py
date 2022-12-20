# aoc 20 - a good relief, and as we all know, reliefs end with hell
# not excited for tomorrow

import time

encrypted = []

def timed(func):
	def time():
		start = time.time()
		func()
		end = time.time()
		printf("----- RAN IN %.2f SECONDS -----" % end - start)
	return time

with open(r"input.txt") as f:
	encrypted = [int(x) for x in f.readlines()]

@timed
def mix_dec(iterations=1):
	length = len(encrypted) # too lazy to retype len(encrypted) lol
	indices = list(range(length))
	for _ in range(iterations):
		for i, num in enumerate(encrypted):
			if num == 0: continue
			indicesIndex = indices.index(i)
			old = indices.pop(indicesIndex)
			movedIdx = (indicesIndex + num) % (length - 1)
			indices.insert(movedIdx, old)
	return [encrypted[i] for i in indices]

def mixed_to_coords(mixed):
	actualIndices = ((mixed.index(0) + a) % len(mixed) for a in [1000, 2000, 3000])
	return sum(mixed[i] for i in actualIndices)

print('part 1', mixed_to_coords(mix_dec()))

DECRYPTION_KEY = 811589153
encrypted = [a * DECRYPTION_KEY for a in encrypted]
print('part 2', mixed_to_coords(mix_dec(10)))