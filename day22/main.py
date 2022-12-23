import re

data = open('input.txt').read().split('\n\n')
tiles = dict()
directions = [1, 1j, -1, -1j] # R D L U
turns = {'R': 1, 'L': -1, '': 0}
start = 0
width = 1
depth = 1

for y, row in enumerate(data[0].splitlines(), 1):
    depth = max(depth, y)
    for x, tile in enumerate(row, 1):
        width = max(width, x)
        if not start and tile == '.':
            start = x+y*1j
        if tile != ' ':
            tiles[x+y*1j] = tile

instructions = [(int(s), turns[t]) for (s,t) in re.findall('(\d+)([RL]?)', data[1])]

# my input is this shape:
#   A B
#   C
# D E
# F
# The coordinate and direction swap is hard-coded

def follow_path(start, instructions, part2 = False):
    position = start
    facing = 0
    for (steps, turn) in instructions:
        for _ in range(steps):
            new = position
            new += directions[facing]
            switch = False
            if part2:
                if new not in tiles:
                    switch = True
                    if facing == 0: # R
                        if 1 <= new.imag <= 50: # B's right to E's right, facing left
                            x = 100
                            y = 151 - new.imag
                            new_facing = 2 
                        elif 51 <= new.imag <= 100: # C's right to B's bottom, facing up
                            x = 50 + new.imag
                            y = 50
                            new_facing =  3
                        elif 101 <= new.imag <= 150: # E's right to B'right, facing left
                            x = 150
                            y = 51 - (new.imag-100)
                            new_facing = 2
                        else: # F's right to E's bottom, facing up
                            x = 50 + (new.imag-150)
                            y = 150
                            new_facing = 3
                    elif facing == 1: # D
                        if 101 <= new.real <= 150: # B's bottom to C's right, facing left
                            x = 100
                            y = 50 + (new.real - 100)
                            new_facing = 2
                        elif 51 <= new.real <= 100: # E's bottom to F's right, facing left
                            x = 50
                            y = 150 + (new.real - 50)
                            new_facing = 2
                        else: # F's bottom to B's top, no rotation
                            x = new.real + 100
                            y = new.imag - 200
                            new_facing = facing
                    elif facing == 2: # L
                        if 1 <= new.imag <= 50: # A's left to D's left, facing right
                            x = 1
                            y = 151 - new.imag
                            new_facing = 0
                        elif 51 <= new.imag <= 100: # C's left to D's top, facing down
                            x = new.imag - 50
                            y = 101
                            new_facing = 1
                        elif 101 <= new.imag <= 150: # D's left to A's left, facing right
                            x = 51
                            y = 151 - new.imag
                            new_facing = 0
                        else: # F's left to A's top, facing down
                            x = 50 + (new.imag - 150)
                            y = 1
                            new_facing = 1
                    else: # U
                        if 1 <= new.real <= 50: # D's top to C's left, facing right
                            x = 51
                            y = 50 + new.real
                            new_facing = 0
                        elif 51 <= new.real <= 100: # A's top to F's left, facing right
                            x = 1
                            y = 100 + new.real
                            new_facing = 0
                        else: # B's top to F's bottom, no rotation
                            x = new.real - 100
                            y = 200
                            new_facing = facing
                    new = x+y*1j
            else: # part 1
                while new not in tiles:
                    new += directions[facing]
                    x = new.real
                    x = width if x < 1 else x
                    x = 1 if x > width else x
                    y = new.imag
                    y = depth if y < 1 else y
                    y = 1 if y > depth else y
                    new = x + y*1j
            if tiles[new] == '.':
                position = new
                if switch:
                    facing = new_facing
            else:
                break
        facing = (facing+turn) % 4
    return int(position.imag*1000 + position.real*4 + facing)

print(follow_path(start, instructions), follow_path(start, instructions, True))
