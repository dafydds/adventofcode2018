from typing import List, Callable
import timeit

class Elf:
    def __init__(self, idx, recipies):
        self._idx = idx
        self._recipies = recipies

    
    def move(self):
        steps_forward = self._recipies[self._idx] + 1
        self._idx = (self._idx + steps_forward) % len(self._recipies)

    def current_recipe(self):
        return self._recipies[self._idx]

def get_next_recipies(total : int) -> List[int]:
    val_str = str(total).zfill(2)
    if (val_str[-2] == '0'):
        return [ int(val_str[-1]) ]
    else:
        return [ int(val_str[-2]), int(val_str[-1]) ]



def part_a_stopping_condition(recipies, stopping_value) -> bool:
    return (len(recipies) == stopping_value + 10)

def magic( aList, base=10 ):
    n= 0
    l = len(aList)
    i = 1
    for d in aList:
        n += base**(l - i) * d
        i += 1
    return n

def part_b_stopping_condition(recipies, stopping_value) -> bool:
    m = magic(recipies[-6:])
    return stopping_value == magic(recipies[-6:])

def part_a_output(recipies) -> str:
    return ''.join(str(i) for i in recipies[-10:])

def part_b_output(recipies) -> str:
    return str(len(recipies) - 6)


def loop(stopping_value : int, stopping_func : Callable, output_func : Callable) -> str:
    while (True):
        total = sum([elf.current_recipe() for elf in elves])
        next_recipies = get_next_recipies(total)
        recipies.extend(next_recipies)
        for elf in elves:
            elf.move()
        
        if stopping_func(recipies, stopping_value):
            return output_func(recipies)


def part_b_loop(stopping_value : int, elves : List[Elf], recipies : List[int]) -> str:
    val_len = len(str(stopping_value))
    while (True):
        total = sum([elf.current_recipe() for elf in elves])
        next_recipies = get_next_recipies(total)
        
        recipies.extend(next_recipies)
        if len(recipies) % 1000000 <= 1:
            print(len(recipies), ":",  timeit.default_timer() - start_time)
        for elf in elves:
            elf.move()
        for i in range(len(next_recipies)):
            m = magic(recipies[(-val_len - i):(len(recipies) - i)])
            if m == stopping_value:
                return str(len(recipies) - val_len - i)
    
recipies = [3, 7]
elves = [ Elf(0, recipies), Elf(1, recipies) ]

stopping_value = 824501
output_part_a = loop(stopping_value, part_a_stopping_condition, part_a_output)
assert output_part_a == '1031816654'
print(output_part_a)
  
recipies = [3, 7]
elves = [ Elf(0, recipies), Elf(1, recipies) ]

stopping_value = 59414


start_time = timeit.default_timer()

output_part_b = part_b_loop(stopping_value, elves, recipies)
print(output_part_b)
assert output_part_b == '2018'