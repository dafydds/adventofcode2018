from typing import Tuple
from collections import Counter
import re

def does_react(str1 : str, str2 : str) -> bool:
    if (str1.lower() == str2.lower()) and (str1 != str2):
        return True
    return False


def react(my_string : str, idx : int) -> Tuple[str, int]:
    if (idx == 0):
        return (my_string, 1)
    elif idx == len(my_string):
        return (my_string, idx)
    else:
        l = my_string[idx-1:idx]
        r = my_string[idx:idx+1]
        if does_react(l, r):
            new_string = my_string[:idx-1] + my_string[idx+1:]
            return (new_string, idx - 1)
        else:
            return (my_string, idx + 1)


def polymer(my_string : str) -> str:
    idx = 0
    while (True):
        my_string, idx = react(my_string, idx)
        if (idx == len(my_string)):
            return my_string


def min_with_one_removed(my_string : str) -> int:
    my_min = 10e7
    lc = my_string.lower()
    for x in Counter(lc):
        new_str = re.sub('[' + x + str(x).upper() + ']', '', my_string)
        new_polymer = polymer(new_str)
        my_min = min(my_min, len(new_polymer))
    return my_min


test_string = "dabAcCaCBAcCcaDA"
assert polymer(test_string) == "dabCBAcaDA"
assert min_with_one_removed(test_string) == 4

test_string = "aBbA"
assert polymer(test_string) == ""

with open('day5_input.txt', 'r')  as fp:
    my_string = fp.read()

part_a = len(polymer(my_string))
print(part_a)

part_b = min_with_one_removed(my_string)
print(part_b)

