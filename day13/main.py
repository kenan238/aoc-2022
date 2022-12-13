from json import loads
lines = []
packet_pairs = []
with open(r"input.txt") as f:
	lines = [x.replace("\n", "") for x in f.readlines()]
with open(r"input.txt") as f:
	packet_pairs = f.read().split('\n\n') # didnt wanna format my pairs manually :)

lines = [x for x in lines if len(x) != 0]
pairs = []

while len(lines) > 0:
	pairs.append(lines[:2])
	del lines[:2]


pairs = [[eval(v) for v in x] for x in pairs]

def validatePair(pair):
	try:
		for i in range(len(pair[0])):
			lv = pair[0][i]
			rv = pair[1][i]
			if isinstance(lv, int) and isinstance(rv, int):
				if lv < rv:
					return True
				elif lv > rv:
					return False

			elif isinstance(lv, list) and isinstance(rv, int):
				if validatePair([lv, [rv]]) != None:
					return validatePair([lv, [rv]])

			elif isinstance(lv, int) and isinstance(rv, list):
				if validatePair([[lv], rv]) != None:
					return validatePair([[lv], rv])

			else:
				if validatePair([lv, rv]) != None:
					return validatePair([lv, rv])

		if len(pair[0]) < len(pair[1]):
			return True

		return None
	except IndexError:
		return False

def sort_and_get_key(A): # some sorting thing
	for k in range(1, len(A)):
		cur = A[k]
		j = k
		while j > 0 and validatePair([cur, A[j-1]]):
			A[j] = A[j-1]
			j -= 1
			A[j] = cur
	return A

validPairsIndices = []
for index, pair in enumerate(pairs):
	if validatePair(pair):
		validPairsIndices.append(index + 1)
print(sum(validPairsIndices))
packets = [loads(packet) for pair in packet_pairs for packet in pair.split('\n')]
packets.append([[2]])
packets.append([[6]])
sorted = sort_and_get_key(packets)
# get the last indices (+ 1 to get their non index representation) and multiply
# by themselves
print((sorted.index([[2]]) + 1) * (sorted.index([[6]]) + 1))