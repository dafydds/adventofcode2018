from typing import List, Tuple, Dict, DefaultDict
from collections import defaultdict
import numpy as np
import sys

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

    def attack(self, creature):
        assert self.creature_type != creature.creature_type
        creature.hit_points -= 3
        if creature.hit_points <= 0:
            creature.state = State.DEAD
            creature.hit_points = 0

    def move(self, new_coord):
        self.x, self.y = new_coord
        pass

class Grid:
    LOOKUP = {
        "." : 0,
        "#" : 1,
        "G" : 2,
        "E" : 3
    }

    LOOKBACK = {
        0 : '.',
        1 : '#',
        2 : 'G',
        3 : 'E'
    }

    def __init__(self, lines):
        self.initial_lines = lines
        self.width = len(self.initial_lines[0])
        self.length = len(self.initial_lines)
        self.matrix = np.zeros(shape = (self.length, self.width), dtype=np.int8)
        self.walls = set()
        for j in range(self.length):
            for i in range(self.width):
                self.matrix[j, i] = Grid.LOOKUP[lines[j][i]]
                if Grid.LOOKUP[lines[j][i]] == "#":
                    self.walls.add((i,j))

    def value(self, x : int, y : int) -> str:
        return Grid.LOOKBACK[self.matrix[y, x]]

    def remove(self, coord):
        x, y = coord
        self.matrix[y, x] = 0

    def move(self, from_coord, to_coord):
        x1, y1 = from_coord
        x2, y2 = to_coord
        v1 = self.matrix[y1, x1]
        v2 = self.matrix[y2, x2]
        self.matrix[y1, x1] = 0  # set to available
        self.matrix[y2, x2] = v1

    def is_feasible(self, x : int, y : int) -> bool:
        if (x >= 0 and x <= self.width - 1 and y >= 0 and y <= self.length - 1):
            return True
        return False

    def print_me(self):
        for i in range(self.length):
            row = self.matrix[i,:]
            print("".join([Grid.LOOKBACK[x] for x in row]))


def min_distance(grid : Grid, coords, coords_dest, creatures):
    visited_points = set()
    path = list()
    min_dists = defaultdict(lambda : 1000)
    min_dists[coords] = 0

    for x in g.walls:
        visited_points.add(x)
        min_dists[x] = 1000
    for c in creatures:
        if (c.x, c.y) != coords and (c.x, c.y) != coords_dest:
            visited_points.add((c.x, c.y))
            min_dists[(c.x, c.y)] = 1000
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

lines = parse_file("data/day15_test_input.txt")

g = Grid(lines)
g.print_me()

def parse_creatures(lines):
    idx = 0
    creature_list = list()
    for j,line in enumerate(lines):
        for i,x in enumerate(line):
            if x == 'G' or x == 'E':
                creature_list.append(Creature(idx, x, i, j))
                idx += 1
    return creature_list


def manhattan_dist(coord1, coord2):
    return abs(coord1[0] - coord2[0]) + abs(coord1[1] - coord2[1])

def get_in_range_coords(grid, enemies):
    for enemy in enemies:
        moves = [(enemy.x + 1, enemy.y), (enemy.x - 1, enemy.y), (enemy.x, enemy.y - 1), (enemy.x, enemy.y + 1)]
        for m in moves:
            x, y = m
            if grid.is_feasible(x, y):
                if grid.value(x,y) == ".":
                    yield m


def get_reachable(grid, enemies, actor, creatures):
    for c in get_in_range_coords(grid, enemies):
        is_reachable, dists = min_distance(grid, (actor.x, actor.y), c, creatures)
        if is_reachable:
            yield (c, dists)


def get_distance(from_coords, lookup):
    to_coord, dist_dict = from_coords, lookup
    return dist_dict[to_coord]

def is_next_to_enemy(a, grid):
    moves = [(a.x + 1, a.y), (a.x - 1, a.y), (a.x, a.y - 1), (a.x, a.y + 1)]
    for move in moves:
        x, y = move
        val = grid.value(x,y)
        if a.creature_type == 'G' and val == 'E':
            return True
        if a.creature_type == 'E' and val == 'G':
            return True  
    return False
        
        

def get_next_move(from_coords, lookup, grid, creatures):
    dist_dict = lookup
    dist  = lookup[from_coords]
    vals = [x for x in dist_dict if dist_dict[x] == 1]
    vals.sort(key=lambda x: x[1] * 10000 + x[0])
    for val in vals:
        aa, bb =  min_distance(grid, val, from_coords, creatures)
        if bb[from_coords] == dist - 1:
            return val

def move(from_coord, to_coord, grid):
    x, y = from_coord.x, from_coord.y
    val1 = grid.value(x, y)

    x1, y1 = to_coord
    val2 = grid.value(x1,y1)

    grid.lines[y1][x1] = val1
    grid.lines[y][x] = val2

def move_creature(c, enemies, g, creatures):
    rs = list()
    for coord, dists in get_reachable(g, enemies, c, creatures):
        rs.append((coord, dists, dists[coord], get_next_move(coord, dists, g, creatures)))

    if (len(rs) > 0):
        min_dist = min([x[2] for x in rs])
        options = sorted([x for x in rs if x[2] == min_dist], key=lambda x: x[0][1] * 10000 + x[0][0])
        #print(c, options[0][0], options[0][2], options[0][3])
        g.move((c.x, c.y), options[0][3])
        c.move(options[0][3])
        #g.print_me()
        pass

def get_target(a, enemies, grid):
    possible_targets = list()
    for enemy in enemies:
        if manhattan_dist((enemy.x, enemy.y), (a.x, a.y)) == 1:
            possible_targets.append(enemy)

    if (len(possible_targets) == 0):
        return None
    
    possible_targets.sort(key=lambda c : c.hit_points * 10e6 + (c.x + c.y * 1000))
    return possible_targets[0]

round_idx = 0
creatures = parse_creatures(lines)

end_game = False
while(not end_game):
    complete_round = True
    creatures.sort(key=lambda c : c.y * 10000 + c.x)
    elves = [x for x in creatures if x.creature_type == 'E']
    goblins = [x for x in creatures if x.creature_type == 'G']

    # move the creatures
    for c in creatures:
        enemies = elves if c.creature_type == 'G' else goblins
        if len([x for x in enemies if x.state == State.ALIVE]) == 0:
            end_game = True
            complete_round = False
            break
        
        if is_next_to_enemy(c, g):
            bla  = 1#print(c, "Stay still")
        else:
            move_creature(c, enemies, g, creatures)

        target = get_target(c, enemies, g)
        if target is not None:
            c.attack(target)
            if target.state == State.DEAD:
                g.remove((target.x, target.y))

    if complete_round:
        round_idx += 1

    creatures = [x for x in creatures if x.state == State.ALIVE]
    print("Round", round_idx)
    g.print_me()

print(round_idx)
print(sum( [x.hit_points for x in creatures if x.state == State.ALIVE]))

print(round_idx * sum( [x.hit_points for x in creatures if x.state == State.ALIVE]))
