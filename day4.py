from typing import List, Tuple, Iterable, Set, Dict
from dateutil.parser import parse
from datetime import datetime
import collections

with open('day4_input.txt', 'r')  as fp:
    lines = fp.readlines()


with open('day4_test_input.txt', 'r')  as fp:
    test_lines = fp.readlines()


def parse_date(line : str) -> datetime:
    txt = line.partition("[")[2].partition("]")[0]
    return parse(txt)


def is_new_guard(line : str) -> int:
    if line.find("Guard") >= 0:
        guard_id = int(line.partition("#")[2].partition(" ")[0])
        return guard_id
    else:
        return -1


def get_next_shift(lines : List[str]) -> Iterable[Tuple[int, List[int]]]:
    for line in lines:
        temp_id = is_new_guard(line)
        if temp_id >= 0:
            guard_id = temp_id
        elif line.find("falls asleep") >= 0:
            sleep_date = parse_date(line)
        elif line.find("wakes up") >= 0:
            awake_date = parse_date(line)
            mins = [x for x in range(sleep_date.minute, awake_date.minute)]
            yield (guard_id, mins)


def get_sleepiest_guard(sorted_lines : List[str]) -> int:
    """Get the id of the guard that sleeps the most"""
    d=collections.defaultdict(int)
    for guard_id, mins in get_next_shift(sorted_lines):
        d[guard_id] += len(mins)
    sorted_by_value = sorted(d.items(), key=lambda kv: -kv[1])
    return sorted_by_value[0]


def get_most_common_guard_minute(
            sorted_lines : List[str], 
            my_guard : int = None) -> Tuple[Tuple[int, int], int]:
    """Return the tuple (guard id, minute) which occurs most frequently"""
    d = dict()
    for guard_id, mins in get_next_shift(sorted_lines):
        if my_guard is None or guard_id == my_guard:
            for minute in mins:  
                guard_min = (guard_id, minute) 
                if guard_min in d:
                    d[guard_min] = d[guard_min] + 1
                else:
                    d[guard_min] = 1
    sorted_by_value = sorted(d.items(), key=lambda kv: -kv[1])
    return sorted_by_value[0]


def part_a(lines):
    sorted_lines = sorted(lines, key=parse_date)
    guard, _ = get_sleepiest_guard(sorted_lines)  
    guard_min, _ = get_most_common_guard_minute(sorted_lines, guard)
    _, most_common_min = guard_min
    return guard * most_common_min

# Part A
assert part_a(test_lines) == 240
print(part_a(lines))


def part_b(lines):
    sorted_lines = sorted(lines, key=parse_date)
    guard_min, _ = get_most_common_guard_minute(sorted_lines)
    guard, most_common_min = guard_min
    return guard * most_common_min


# Part B
assert part_b(test_lines) == 4455
print(part_b(lines))