# aoc day 16
from parse import *
from dataclasses import dataclass
from functools import cache
from collections import (
    Counter,
    defaultdict,
)

TIME_LIMIT = 30
TIME_CURTIME = 0
nodes = []

rates = {}
links = {}

@cache
def dfs(valve, time, visited):
	if time <= 1:
		return 0
	res = 0
	for link in links[valve]:
		res = max(res, dfs(link, time - 1, visited))
	if valve not in visited and rates[valve] > 0:
		visited = tuple(sorted([*visited, valve]))
		res = max(res, dfs(valve, time - 1, visited) + rates[valve] * (time - 1))

	return res

with open(r"input.txt") as f:
	for line in f.readlines():
		r = list(parse("Valve {} has flow rate={}; tunnels lead to valves {}", line.replace("\n", "")))
		name = r.pop(0)
		flowrate = int(r.pop(0))
		connections = r.pop(0).split(", ")
		rates[name] = flowrate
		links[name] = connections

print('part 1', dfs('AA', 30, ()))

weighted = defaultdict(Counter)
for i in rates:
    for j in rates:
        if i == j:
            weighted[i][j] = 0
        elif j in links[i]:
            weighted[i][j] = 1
        else:
            weighted[i][j] = float('inf')
for i in rates:
    for j in rates:
        if i == j:
            continue
        for k in rates:
            if k == i or k == j:
                continue
            weighted[i][j] = min(weighted[i][j], weighted[i][k] + weighted[k][j])
wlinks = defaultdict(dict)
for i in rates:
    for j in rates:
        if weighted[i][j] < float('inf') and rates[j] > 0:
            wlinks[i][j] = weighted[i][j]
working = {valve: rate for valve, rate in rates.items() if rate > 0}
@cache
def dfs(player1, player2, visited): # double player dfs
    res = 0
    for v, rate in working.items():
        if v in visited:
            continue
        new_visited = tuple(sorted([*visited, v]))
        valve1, time1 = player1
        if v in wlinks[valve1] and time1 - wlinks[valve1][v] >= 1:
            time_left = time1 - wlinks[valve1][v] - 1
            player1_move = dfs((v, time_left), player2, new_visited) + time_left * rate
            res = max(res, player1_move)
        valve2, time2 = player2
        if v in wlinks[valve2] and time2 - wlinks[valve2][v] >= 1:
            time_left = time2 - wlinks[valve2][v] - 1
            player2_move = dfs(player1, (v, time_left), new_visited) + time_left * rate
            res = max(res, player2_move)
    return res

print('part 2', dfs(('AA', 26), ('AA', 26), ()))