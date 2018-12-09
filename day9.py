import re
from typing import Tuple
from collections import defaultdict, deque
import timeit

start_time = timeit.default_timer()
print(timeit.default_timer() - start_time)


puzzle_input = "470 players; last marble is worth 72170 points"

def parse_input(input : str) -> Tuple[int, int]:
    p = re.compile("([0-9]+) players; last marble is worth ([0-9]+) points")
    m = p.match(puzzle_input)
    return ( int(m[1]), int(m[2]))


class Marble:
    def __init__(self, id):
        self.id = id

    def __repr__(self):
        return str(self.id)

class Circle:
    def __init__(self):
        self.marbles = deque()
        self.marbles.appendleft(Marble(0))

    def move_clockwise(self, steps):
        self.marbles.rotate(-steps)

    def get_current_marble(self):
        return self.marbles[0]

    def add_marble(self, marble):
        self.marbles.appendleft(marble)
        pass

    def remove_marble(self) -> Marble:
        return self.marbles.popleft()

    def move(self, marble : Marble) -> Marble:
        if (marble.id % 23 == 0):
            self.move_clockwise(-7)
            return self.remove_marble()
        else:
            self.move_clockwise(2)
            self.add_marble(marble)
            return None


def get_max_player_score(num_players, last_marble_worth):
    c = Circle()
    player_scores = defaultdict(int)
    player_id = 1
    marble_id = 1
    while(True):
        m = c.move(Marble(marble_id))
        if m is not None:
            player_scores[player_id] += (m.id + marble_id)
        player_id += 1
        if player_id > num_players:
            player_id = 1
        marble_id += 1
        if (marble_id > last_marble_worth):
            break
        if (marble_id % 100000 == 0):
            print(marble_id, timeit.default_timer() - start_time)
    return max(player_scores[k] for k in player_scores)

assert get_max_player_score(9, 25) == 32
out = get_max_player_score(10, 1618)
assert out == 8317
assert get_max_player_score(13,7999) == 146373
assert get_max_player_score(17,1104) ==2764
assert get_max_player_score(21, 6111) == 54718
assert get_max_player_score(30, 5807) == 37305

print("Part A:")
print(get_max_player_score(470, 72170))

print("Part B:")
print(get_max_player_score(470, 72170 * 100))