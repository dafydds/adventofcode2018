from typing import List, Tuple, Iterable, Set

with open('day3_input.txt', 'r')  as fp:
    lines = fp.readlines()

class Rect:
    def __init__(self, left, top, width, height):
        self.left = left
        self.top = top
        self.width = width
        self.height = height


def parse_rect(rect_text : str) -> Rect:
    """Convert string encoding into a tuple (left, top, x, y)"""
    _, _, x = rect_text.partition("@")
    position, _, size = x.partition(":")
    left, _, top = position.partition(",")
    x, _, y = size.partition("x")
    return Rect(int(left), int(top), int(x), int(y))


def encode(rect : Rect) -> List[Tuple[int, int]]:
    return [(x,y)
        for y in range(rect.top, rect.top + rect.height)
            for x in range(rect.left, rect.left + rect.width)]


def get_disputed_claims(rects : List[Rect]) -> Iterable[Tuple[int, int]]:
    all_pts = set()
    for rect in rects:
        for pts in encode(rect):
            if (pts in all_pts):
                yield pts
            else:
                all_pts.add(pts)


def disputes(lines : List[str]) -> Set[Tuple[int, int]]:
    rects = [parse_rect(x) for x in lines]
    disputed_pts = set()
    for x in get_disputed_claims(rects):
        disputed_pts.add(x)
    return disputed_pts

test_lines = [
    "#1 @ 1,3: 4x4",
    "#2 @ 3,1: 4x4",
    "#3 @ 5,5: 2x2"
]

assert len(disputes(test_lines)) == 4

print("Part 1:")
overlapping_pts = disputes(lines)
test_overlapping_pts = disputes(test_lines)
print(len(overlapping_pts))

def overlap(
        pts : List[Tuple[int, int]], 
        disputes : Set[Tuple[int, int]]) -> bool:
    for p in pts:
        if p in disputes:
            return False
    return True


def find_separate_rects(lines : List[str], 
                    disputes : Set[Tuple[int, int]]) -> Iterable:
    for idx, line in enumerate(lines):
        rect = parse_rect(line)
        pts = encode(rect)
        if overlap(pts, disputes):
            yield idx + 1

for x in find_separate_rects(test_lines, test_overlapping_pts):
    assert x == 3

for x in find_separate_rects(lines, overlapping_pts):
    print(x)

