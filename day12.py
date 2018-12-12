import numpy as np
from typing import List, Tuple, Dict, DefaultDict
from collections import defaultdict


class Generation:

    def __init__(self, state : str, first: int):
        self.state = list(state)
        self.first = first
        self.last = first + len(state) - 1

    def __repr__(self):
        return str(self.first) + '  ' + str(self.get_pots())
        

    def next_generation(self, mapping : DefaultDict[str, str]):
        window = 5
        w = int((window - 1) / 2)
        padding = ['.' for i in range(window - 1)]
        padded_state = padding + self.state + padding
        out = ''
        for i in range(len(padded_state) - 5):
            seed_string = "".join(padded_state[i:(i+5)])
            out += mapping[seed_string]

        # find first and last occurrence of # in string
        first = out.find('#')
        last = out.rfind('#')
        stripped = out[first:(last+1)]
        return Generation(stripped, self.first - w + first)
            
    def get_pots(self) -> List[int]:
        return [i + self.first for i, x in enumerate(self.state) if x== '#']



def parse_file(f):
    with open(f, 'r')  as fp:
        lines = [x.rstrip() for x in fp.readlines()]
        initial_state = [x for x in lines[0]][15:]
        mapping_string = lines[2:]

        maps = defaultdict(lambda : '.')
        for m in mapping_string:
            key = m[:5]
            val = m[9]
            maps[key] = val

        return (initial_state, maps)

state, mapping = parse_file("data/day12_input.txt")

pot_index_sum = 0
g = Generation(state, 0)
print("0: ", g)
pot_index_sum = sum(g.get_pots())
for i in range(2000):
    g = g.next_generation(mapping)
    p = sum(g.get_pots())
    print(str(i) + ": ", p)


