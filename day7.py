from typing import Tuple, List, Iterable
from collections import Counter, OrderedDict
import re

with open('data/day7_input.txt', 'r')  as fp:
    lines = fp.readlines()

with open('data/day7_test_input.txt', 'r')  as fp:
    test_lines = fp.readlines()

def parse_lines(lines : List[str]) -> List[Tuple[str, str]]:
    p = re.compile(r'Step ([A-Z]) must be finished before step ([A-Z]) can begin')
    return [p.match(line).groups() for line in lines]


class DependencyGraph:
    def __init__(self, instructions : List[Tuple[str, str]]):    
        a = dict()
        for i in instructions:
            if i[1] not in a:
                dependency = dict()
                dependency[i[0]] = None
                a[i[1]] = dependency
            else:
                dependency = a[i[1]]
                dependency[i[0]] = None
            if i[0] not in a:
                a[i[0]] = dict()

        self.graph = a


    def next(self) -> str:
        if len(self.graph) == 0:
            return None

        # get first step with no dependencies
        for k, v in sorted(self.graph.items(), key=lambda x: x[0]):
            if len(v) == 0:
                step = k
                break

        # remove the instruction from the dependencies of others
        for k in self.graph:
            if step in self.graph[k]:
                del self.graph[k][step]

        del self.graph[step]
        return step

def part_a(my_lines):
    parsed_lines = parse_lines(my_lines)
    graph = DependencyGraph(parsed_lines)

    output_string = ''
    while (True):
        s = graph.next()
        if s is None:
            break
        else:
            output_string += s

    return output_string

assert part_a(test_lines) == "CABDFE"
print(part_a(lines))

        


