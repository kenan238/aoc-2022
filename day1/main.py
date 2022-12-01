# aoc day 1 - python
cals = []

with open("input.txt", "r") as f:
  contents = f.read().splitlines()
  l = []
  for line in contents:
    if line == "":
      cals.append(l)
      l = []
    else:
      l.append(int(line))
      if contents[-1] == line:
        cals.append(l)

sumd = [sum(x) for x in cals]
print(max(sumd))