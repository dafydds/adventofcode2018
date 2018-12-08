from typing import List, Tuple

test_string = "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2"
with open('data/day8_input.txt', 'r')  as fp:
    my_string = fp.read()


class Node:
    def __init__(self):
        self.metadata = list()
        self.children = list()

    def checksum(self):
        return sum([x for x in self.metadata])

    def add_child(self, child):
        self.children.append(child)
        pass

    def value(self):
        if len(self.children) == 0:
            return self.checksum()
        else:
            val = 0
            for m in self.metadata:
                if m > 0 and m <= len(self.children):
                    val += self.children[m-1].value()
            return val


def parse_string(my_string : str) -> List[int]:
    return [int(x) for x in my_string.split(" ")]


def parse_node(codes: List[int], idx : int) -> Tuple[Node, int]:
    num_children = codes[idx]
    num_metadata = codes[idx + 1]
    node = Node()

    j = idx + 2
    for i in range(num_children):
        child, j = parse_node(codes, j)
        node.add_child(child)

    meta = list()
    for i in range(num_metadata):
        meta.append(codes[j])
        j += 1
    node.metadata = meta
    return (node, j)


codes = parse_string(my_string)
tree, _ = parse_node(codes, 0)

def checksum(node):
    c = node.checksum()
    for child in node.children:
        c += checksum(child)
    return c


print(checksum(tree))
print(tree.value())