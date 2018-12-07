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


def test_job_time(s : str) -> int:
    return ord(s) - 64

def job_time(s : str) -> int:
    return ord(s) - 4

assert test_job_time('A') == 1
assert job_time('A') == 61


class State:
    BUSY = 1
    AVAILABLE = 0

class Worker:
    def __init__(self):
        self._state = State.AVAILABLE
        self._job_end = 0
        self._job = None

    def state(self, second : int) -> State:
        return self._state

    def give_job(self, job : str, second : int, job_length : int):
        self._job_end = second + job_length
        self._job = job
        self._state = State.BUSY

    def output(self, second : int):
        if (second == self._job_end):
            self._state = State.AVAILABLE
            return self._job
        else:
            return None


class DependencyGraph:
    def __init__(self, 
                instructions : List[Tuple[str, str]], 
                workers : List[Worker],
                job_length_fn):  
        """build dependency structure as a dict of dicts"""  
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
        self.workers = workers
        self.second = -1
        self._job_length_fn = job_length_fn

    def get_available_instructions(self):
        """get next available instructions"""
        instructions = list()
        for k, v in sorted(self.graph.items(), key=lambda x: x[0]):
            if len(v) == 0:
                instructions.append(k)
        return instructions


    def tick(self) -> List[str]:
        self.second += 1
        
        busy_workers =  len([w for w in self.workers 
                            if w.state(self.second) == State.BUSY])

        if len(self.graph) == 0 and busy_workers == 0:
            return None

        # check workers to see if they have produced anything by the start of this second
        outputs = list()
        for w in self.workers:
            out = w.output(self.second)
            if out is not None:
                outputs.append(out)

        # remove the completed instructions from the dependencies of others
        for step in outputs:    
            for k in self.graph:
                if step in self.graph[k]:
                    del self.graph[k][step]

        next_steps = self.get_available_instructions()
        free_workers =  [w for w in self.workers 
                            if w.state(self.second) == State.AVAILABLE]

        # distribute the jobs amongst the free workers
        for x, worker in zip(next_steps, free_workers):
            worker.give_job(x, self.second, self._job_length_fn(x))
            del self.graph[x]

        return sorted(outputs, key=lambda x: x)

def part_a(my_lines, job_length_fn):
    parsed_lines = parse_lines(my_lines)
    w = Worker()
    graph = DependencyGraph(parsed_lines, [w], job_length_fn)

    output_string = ''
    while (True):
        s = graph.tick()
        if s is None:
            break
        else:
            output_string += ''.join(s)

    return output_string

print(part_a(test_lines, test_job_time))
assert part_a(test_lines, test_job_time) == "CABDFE"
print(part_a(lines, job_time))


def part_b(my_lines, job_time_fn, num_workers):
    parsed_lines = parse_lines(my_lines)
    workers = list()
    for i in range(num_workers):
        workers.append(Worker())
    graph = DependencyGraph(parsed_lines, workers, job_time_fn)

    output_string = ''
    while (True):
        s = graph.tick()
        if s is None:
            break
        elif len(s) > 0:
            output_string += ''.join(s)

    return (output_string, graph.second - 1)


test_part_b = part_b(test_lines, test_job_time, 2)
assert test_part_b[0]  == "CABFDE"
assert test_part_b[1] == 15

print(part_b(lines, job_time, 5))
        


