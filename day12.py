import numpy as np
from typing import List, Tuple

def char_to_int(character : str) -> int:
    return (1 if character == "#" else 0)


def int_to_char(val : int) -> str:
    return ('#' if val == 1 else '.')

class Generation:

    def __init__(self, initial_state, mappings):
        self.mapp

    def next_generation():


def parse_file(f):
    with open(f, 'r')  as fp:
        lines = fp.readlines()
        initial_state = [char_to_int(x) for x in lines[0]][15:]]
        mapping_string = lines[2:]

        maps = dict()
        for m in mapping_string:
            key = m[:5]
            val = m[9]
            maps[key] = val

        return (initial_state, maps)


