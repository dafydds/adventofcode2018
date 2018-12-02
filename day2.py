from collections import Counter

with open('input_day2.txt', 'r')  as fp:
    lines = fp.readlines()

vals = [x.strip() for x in lines]

def has_n_characters(n, word):
    c = Counter(word)
    for _, v in c.items():
        if (n == v):
            return 1
    return 0

def checksum(ids):
    twos = sum([has_n_characters(2, x) for x in ids])
    threes = sum([has_n_characters(3, x) for x in ids])

    return (twos * threes)
    
print(checksum(vals))

test = ["abcdef", "bababc","abbcde", "abcccd", "aabcdd", "abcdee", "ababab"]
assert checksum(test) == 12

def count_diffs(word1, word2):
    diffs = sum([x != y for x, y in zip(word1, word2)])
    return diffs + abs(len(word1) - len(word2))


def get_most_similar_pair(words):
    N = len(words)
    for i in range(N):
        for j in range(N):
            if (i < j):
                if (count_diffs(words[i], words[j]) == 1):
                    return (i,j)
                    
p1, p2 = get_most_similar_pair(vals)

def get_matching_chars(p1, p2):
    return ''.join([ x for x,y in zip(vals[p1], vals[p2]) if x == y ])
    
print(get_matching_chars(p1, p2))
