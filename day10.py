from typing import List, Tuple
import re

with open('data/day10_input.txt', 'r')  as fp:
    lines = fp.readlines()

class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def __eq__(self, othr):
        return (isinstance(othr, type(self))
                and (self.x, self.y) ==
                    (othr.x, othr.y))

    def __hash__(self):
        return (hash((self.x, self.y)))

class Particle:
    def __init__(self, x0, y0, v_x, v_y):
        self._x0 = x0
        self._y0 = y0
        self._v_x = v_x
        self._v_y = v_y

    def get_position(self, t : int) -> Coord:
        return Coord(self._x0 + t * self._v_x, 
                        self._y0 + t * self._v_y)
    
def parse_input(lines : List[str]) -> List[Particle]:
    particles = list()
    for line in lines:    
        p = re.compile("position=<([0-9\s-]+),([0-9\s-]+)> velocity=<([0-9\s-]+),([0-9\s-]+)>")
        m = p.match(line).groups()
        particles.append( Particle(int(m[0]), int(m[1]), int(m[2]), int(m[3])))
    return particles

particles = parse_input(lines)
t3 = [x.get_position(3) for x in particles]

def get_top_left(coords : List[Coord]):
    x = min([c.x for c in coords])
    y = max([c.y for c in coords])
    return Coord(x, y)

def get_bottom_right(coords : List[Coord]):
    x = max([c.x for c in coords])
    y = min([c.y for c in coords])
    return Coord(x, y)

def distance(c1 : Coord, c2 : Coord):
    return abs(c1.x - c2.x) + abs(c1.y - c2.y)

def rect_metric(coords : List[Coord]):
    return distance(get_top_left(coords),
                         get_bottom_right(coords))


def gradient(particles : List[Particle], t : int):
    f0 = rect_metric([x.get_position(t) for x in particles])
    f1 = rect_metric([x.get_position(t + 1) for x in particles])
    return f1 - f0

def get_potential_messages(particles : List[Particle], distance_threshold : int):
    t = 0
    iterations = 0
    while (True):
        iterations += 1
        coords = [x.get_position(t) for x in particles]
        d = rect_metric(coords)
        grad = gradient(particles, t)
        if d < distance_threshold:
            yield (coords, t)
        t += max(int( -d / grad  * 0.2), 1)
        if iterations >= 400:
            break


def print_grid(top_left : Coord, position_coords : List[Coord], grid_x : int, grid_y : int):

    position_set = set(position_coords)
    for j in range(top_left.y - grid_y, top_left.y + 2):
        line = ""
        for i in range(top_left.x, top_left.x + grid_x):
            c = Coord(i, j)
            s = "#" if c in position_set else "."
            line += s
        print(line)
    pass


for c, t in get_potential_messages(particles, 80):
    print_grid(get_top_left(c), c, 90, 10)
    print("Time:", t)

