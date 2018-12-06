from typing import List, Tuple
from collections import Counter

with open('data/day6_input.txt', 'r')  as fp:
    lines = fp.readlines()

def coords(lines : List[str]) -> Tuple[int, int]:
    return [(int(x[0]), int(x[1]))
                for x in (line.split(", ") 
                        for line in lines)]


def rect(coords : Tuple[int, int]) -> Tuple[int, int, int, int]: 
    """Return a rectangle representation as 4 points ( x_min, x_max, y_min, y_max)"""
    min_x = min([x for x, _ in coords])
    max_x = max([x for x, _ in coords])
    min_y = min([y for _, y in coords])
    max_y = max([y for _, y in coords])

    return (min_x, max_x, min_y, max_y)


def is_edge(point : (int, int), rect : Tuple[int, int, int, int]) -> bool:
    if point[0] <= rect[0] or point[0] >= rect[1]:
        return True
    elif point[1] <= rect[2] or point[1] >= rect[3]:
        return True
    return False


def distance(point1, point2):
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])


def closest_coord(
    point : Tuple[int, int], 
    my_coords : List[Tuple[int, int]]) -> Tuple[int, Tuple[int, int]]:
    sorted_coords = [i for i in sorted(enumerate(my_coords), key=lambda x: distance(x[1], point))]
    # if tied return None
    if (distance(sorted_coords[0][1], point) == distance(sorted_coords[1][1], point)):
        return None
    else:
        return sorted_coords[0]


def get_largest_non_infinite_coord(my_coords):
    my_rect = rect(my_coords)
    closest_coords = list()
    infinite_coords = set()

    for i in range(my_rect[0], my_rect[1] + 1):
        for j in range(my_rect[2], my_rect[3] + 1):
            my_closest = closest_coord((i,j), my_coords)
            if my_closest is not None:
                if (is_edge((i, j), my_rect)):
                    infinite_coords.add(my_closest[0])
                else:
                    closest_coords.append(my_closest[0])
    clean_coords = [x for x in closest_coords if x not in infinite_coords]

    x = Counter(clean_coords)
    biggest_coord = x.most_common(1)[0]
    return biggest_coord

def total_distance(
    point : Tuple[int, int],
    my_coords : List[Tuple[int, int]]) -> int:
    total_distance = 0
    for c in my_coords:
        total_distance += distance(point, c)
    return total_distance

my_coords = coords(lines)

print("Part A:")
print(get_largest_non_infinite_coord(my_coords)[1])

def part_b(my_coords, N):
    my_rect = rect(my_coords)
    counts = 0
    for i in range(my_rect[0], my_rect[1] + 1):
        for j in range(my_rect[2], my_rect[3] + 1):
            # check that my search region is enclosed by the rectangle's edges, which makes the search easy
            if (is_edge((i, j), my_rect)):
                if total_distance((i,j), my_coords) < N:
                    assert True == False
            else:
                if total_distance((i, j), my_coords) < N:
                    counts += 1
    return counts

print("Part B:")
print(part_b(my_coords, 10000))