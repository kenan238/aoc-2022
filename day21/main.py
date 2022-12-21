from parse import parse
from sympy import symbols, solve_linear

monkeys = {}

with open(r"input.txt") as f:
	for line in f.readlines():
		parsed = parse("{}: {}", line.replace('\n', ''))
		name = parsed[0]
		operation = parsed[1] # remove \n
		operation = operation.split(" ")
		directResult = None
		deps = None
		if len(operation) == 1:
			directResult = int(operation[0])
			operation = None
		if operation != None:
			deps = [operation[0], operation[2]]
		monkeys[name] = { 
			'op': operation, 
			'res': directResult,
			'deps': deps,
			'solvedDeps': [],
			'hasDirectVal': directResult != None
		}


def monkeyToStr(monkey):
	return f"<monkey res({monkey['res']}) deps({monkeys['deps']}) op({monkeys['op']})"

def findValOf(mname):
	if monkeys[mname]['hasDirectVal']:
		# print(mname + ' yells ' + str(monkeys[mname]['res']))
		return

	# figure out val
	dependencies = monkeys[mname]['deps']

	for dependency in dependencies:
		if monkeys[dependency]['res'] == None:
			findValOf(dependency)
		# make sure all dependency monkeys have their values

	# we got the value of all dependencies
	# now perform the operation
	depMonkey = monkeys[dependencies[0]]
	depMonkey1 = monkeys[dependencies[1]]

	monkeys[mname]['solvedDeps'].append(depMonkey['res'])
	monkeys[mname]['solvedDeps'].append(depMonkey1['res'])

	op = monkeys[mname]['op'][1]

	if op == '*': monkeys[mname]['res'] = depMonkey['res'] * depMonkey1['res']
	if op == '+': monkeys[mname]['res'] = depMonkey['res'] + depMonkey1['res']
	if op == '-': monkeys[mname]['res'] = depMonkey['res'] - depMonkey1['res']
	if op == '/': monkeys[mname]['res'] = depMonkey['res'] / depMonkey1['res']
	if op == '=': monkeys[mname]['res'] = int(depMonkey['res'] == depMonkey1['res'])

	# print(mname + ' yells ' + str(monkeys[mname]['res']) + ' from ' + str(depMonkey) + ' and ' + str(depMonkey1))

solveP2 = True

if not solveP2:
	findValOf('root')
	print('part 1 root yells ' + str(monkeys['root']['res']))
	monkeys['root']['op'][1] = '='

elif solveP2:
	monkeys['humn']['res'] = symbols("humn")
	monkeys['root']['res'] = None

	print(monkeys['humn'])

	findValOf('root')
	solved = solve_linear(monkeys['root']['solvedDeps'][0], monkeys['root']['solvedDeps'][1])
	print('part 2 humn should yell ' + str(solved[1]))