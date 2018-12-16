from typing import List, Tuple, Dict, DefaultDict
from collections import defaultdict
import numpy as np
import sys

sys.setrecursionlimit(3000)

class State:
    ALIVE = 1
    DEAD = 0

class Creature:
    def __init__(self, id, creature_type, x, y):
        self.id = id
        self.creature_type = creature_type
        self.x = x
        self.y = y
        self.attack_power = 3
        self.hit_points = 200
        self.state = State.ALIVE

    def __repr__(self):
        return str(self.creature_type) + " " + str(self.id) + ": " + str((self.x, self.y))

    def move(self, board) -> bool:
        return False

    def attack(self, creature):
        assert self.creature_type != creature.creature_type
        creature.hit_points -= 3
        if creature.hit_points <= 0:
            creature.state = State.DEAD


class Grid:
    def __init__(self, lines):
        self.lines = lines
        self.width = len(self.lines[0])
        self.length = len(self.lines)

    def value(self, x : int, y : int) -> str:
        return self.lines[y][x]

    def is_feasible(self, x : int, y : int) -> bool:
        if (x >= 0 and x <= self.width - 1 and y >= 0 and y <= self.length - 1):
            return True
        return False

def min_distance(grid : Grid, coords, coords_dest):
    visited_points = set()
    min_dists = defaultdict(lambda : 1000)
    min_dists[coords] = 0

    current_node = coords
    to_visit_next = list()

    while True:
        x, y = current_node

        if current_node == coords_dest:
            return (True, min_dists)
        moves = [(x + 1, y), (x - 1, y), (x, y - 1), (x, y + 1)]

        for m in moves:
            x_m, y_m = m
            if grid.is_feasible(x_m, y_m) and m not in visited_points:
                val = grid.value(x_m, y_m)
                if val == '.':
                    min_dists[m] = min(min_dists[current_node] + 1, min_dists[m] )
                    to_visit_next.append(m)

        visited_points.add(current_node)

        # repeat with the min distance coord
        to_visit_next.sort( key=lambda x: -min_dists[x])
        if len(to_visit_next) > 0:
            current_node = to_visit_next.pop()
        else:
            return (False, min_dists)




def parse_file(f):
    with open(f, 'r')  as fp:
        lines = [x.rstrip() for x in fp.readlines()]
        return lines

def print_board(lines):
    for l in lines:
        print(l)

lines = parse_file("data/day15_test_input.txt")
print_board(lines)
g = Grid(lines)

test = min_distance(g, (2, 2), (5, 5))


def parse_creatures(lines):
    idx = 0
    creature_list = list()
    for j,line in enumerate(lines):
        for i,x in enumerate(line):
            if x == 'G' or x == 'E':
                creature_list.append(Creature(idx, x, i, j))
                idx += 1
    return creature_list

# round_idx = 1
# creatures = parse_creatures(lines)
# while (True):
#     creatures.sort(key=lambda c : c.y * 10000 + c.x)
#     elves = [x for x in creatures if x.creature_type == 'E']
#     goblins = [x for x in creatures if x.creature_type == 'G']

#     # move the creatures
#     for c in creatures:
#         enemies = elves if c.creature_type == 'G' else goblins
#         c.move(lines)


