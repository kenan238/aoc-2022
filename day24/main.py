from collections import deque, namedtuple

MOVES = [(0, 1), (0, -1), (1, 0), (-1, 0), (0, 0)]

Blizzards = namedtuple('Blizzards', ['rows', 'cols', 'left', 'right', 'up', 'down'])

def parse(data):
    lines = [l[1:-1] for l in data.splitlines()[1:-1]] # Cut off walls
    rows, cols = len(lines), len(lines[0])
    left = frozenset((r, c) for r in range(rows) for c in range(cols) if lines[r][c] == '<')
    right = frozenset((r, c) for r in range(rows) for c in range(cols) if lines[r][c] == '>')
    up = frozenset((r, c) for r in range(rows) for c in range(cols) if lines[r][c] == '^')
    down = frozenset((r, c) for r in range(rows) for c in range(cols) if lines[r][c] == 'v')
    return Blizzards(rows, cols, left, right, up, down)

def shortest_path(blizz, start, end, start_time):
    visited = set()
    q = deque()
    while True:
        # When do we enter the board? We can enter at any time after the start_time
        while not q:
            start_time += 1 # Increment first, because it takes one timestep to enter the board
            if is_free(blizz, start[0], start[1], start_time):
                q.append((start[0], start[1], start_time))
        r, c, t = q.popleft()
        if (r, c, t) in visited:
            continue
        visited.add((r, c, t))
        if (r, c) == end:
            return t + 1
        for dr, dc in MOVES:
            nr, nc = r + dr, c + dc
            if 0 <= nr < blizz.rows and 0 <= nc < blizz.cols and is_free(blizz, nr, nc, t + 1):
                q.append((nr, nc, t + 1))

def is_free(blizz, r, c, t):
    return not any((
        (r, (c - t) % blizz.cols) in blizz.right,
        (r, (c + t) % blizz.cols) in blizz.left,
        ((r - t) % blizz.rows, c) in blizz.down,
        ((r + t) % blizz.rows, c) in blizz.up
    ))

b = parse(open('input.txt', 'r').read())
start = (0, 0)
end = (b.rows - 1, b.cols - 1)
t1 = shortest_path(b, start, end, 0)
t2 = shortest_path(b, end, start, t1)
t3 = shortest_path(b, start, end, t2)
print(t1)
print(t3)
