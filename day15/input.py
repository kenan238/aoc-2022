from collections import namedtuple

point = namedtuple('Point', ['x', 'y'])
search_area = namedtuple(
    'SearchArea', ['top', 'bottom', 'left', 'right', 'radius'])


def manhattan_dist(p1, p2):
    return abs(p1.x-p2.x) + abs(p1.y-p2.y)


def solve_part_1(closest):
    areas = [] # contains all areas, or "diamond" shaped things
    beacons = set()

    for sensor in closest:
        beacon = closest[sensor]
        beacons.add(beacon)
        dist = manhattan_dist(sensor, beacon)

        areas.append(search_area(
            top=point(sensor.x, sensor.y-dist),
            bottom=point(sensor.x, sensor.y+dist),
            left=point(sensor.x-dist, sensor.y),
            right=point(sensor.x+dist, sensor.y),
            radius=dist)
        )

    y = 2000000
    intervals = []
    for area in areas:
        if area.top.y <= y <= area.bottom.y: # select appropriate areas
            min_y = min(y, area.left.y)
            max_y = max(y, area.left.y)
            remaining = area.radius*2+1 - (max_y - min_y) * 2
            start = area.left.x + (max_y - min_y)
            intervals.append((start, start + remaining - 1)) # calculate intervals

    intervals.sort()
    stack = []
    for start, end in intervals:
        if stack and stack[-1][1] >= start:
            stack[-1][1] = max(stack[-1][1], end)
        else:
            stack.append([start, end])

    res = 0
    for start, end in stack:
        res += end-start+1

    for beacon in beacons:
        if beacon.y != y:
            continue
        for start, end in stack:
            if start <= beacon.x <= end:
                res -= 1

    return res


def solve_part_2(closest):
    # forgot DRY
    #     Dont Repeat Yourself
    areas = []

    for sensor in closest:
        beacon = closest[sensor]
        dist = manhattan_dist(sensor, beacon)

        areas.append(search_area(
            top=point(sensor.x, sensor.y-dist),
            bottom=point(sensor.x, sensor.y+dist),
            left=point(sensor.x-dist, sensor.y),
            right=point(sensor.x+dist, sensor.y),
            radius=dist)
        )

    for y in range(4000000+1):
        intervals = []

        for area in areas:
            if area.top.y <= y <= area.bottom.y:
                min_y = min(y, area.left.y)
                max_y = max(y, area.left.y)
                remaining = area.radius*2+1 - (max_y - min_y) * 2
                start = area.left.x + (max_y - min_y)
                intervals.append((start, start + remaining - 1))

        intervals.sort()
        stack = []
        for start, end in intervals:
            if stack and (stack[-1][1] >= start or start-stack[-1][1] == 1):
                if stack[-1][1] >= start:
                    stack[-1][1] = max(stack[-1][1], end)
                else:
                    stack[-1][1] = end
            else:
                stack.append([start, end])

        if len(stack) == 2: # calculate fine tuning signal
            return (stack[0][-1]+1)*4000000 + y

    return -1


if __name__ == '__main__':
    with open('input.txt') as f:
        closest = {}

        for line in f.readlines(): # get closest 
            sensor, beacon = line.strip().split(': ')

            x, y = sensor.split(' ')[-2:]
            x_int = int(x.split('=')[1][:-1])
            y_int = int(y.split('=')[1])
            sensor = point(x_int, y_int)

            x, y = beacon.split(' ')[-2:]
            x_int = int(x.split('=')[1][:-1])
            y_int = int(y.split('=')[1])
            closest[sensor] = point(x_int, y_int)

        print("Part 1:", solve_part_1(closest))
        print("Part 2:", solve_part_2(closest))
