import itertools
import random
import hashlib
import sys
import multiprocessing
from datetime import datetime
from collections import deque

FINISHED = False

THREADS = 8

BU = 1
BD = -1
RU = 2
RD = -2
GU = 4
GD = -3
PD = 4
PU = -4

sums = []

CARDS = [
    [ BD, RD, PU, GU ],
    [ PD, GD, BU, RU ],
    [ BD, GD, BU, RU ],
    [ PD, RD, BU, GU ],
    [ PD, RD, PU, GU ],
    [ BD, RD, PU, GU ],
    [ RU, GD, BD, PU ],
    [ PU, GD, RD, BU ],
    [ PU, BU, RD, GD ],
]

cards_list = [ 0, 1, 2, 3, 4, 5, 6, 7, 8 ]

# CARDS = [
#     [ BD, BU, BD, BU ],
#     [ BD, BU, BD, BU ],
#     [ BD, BU, BD, BU ],
#     [ BD, BU, BD, BU ],
#     [ BD, BU, BD, BU ],
#     [ BD, BU, BD, BU ],
#     [ BD, BU, BD, BU ],
#     [ BD, BU, BD, BU ],
#     [ BD, BU, BD, BU ],
# ]

def rotate(c, n):
    tmp = deque(c)
    tmp.rotate(n)
    return list(tmp)

def validate(cards):
    # Top row
    if cards[0][1] != cards[1][3] * -1:
        return False
    if cards[1][1] != cards[2][3] * -1:
        return False

    # Second row across
    if cards[3][1] != cards[4][3] * -1:
        return False
    if cards[4][1] != cards[5][3] * -1:
        return False
    # Second row up
    if cards[3][0] != cards[0][2] * -1:
        return False
    if cards[4][0] != cards[1][2] * -1:
        return False
    if cards[5][0] != cards[2][2] * -1:
        return False

    # Third row across
    if cards[6][1] != cards[7][3] * -1:
        return False
    if cards[7][1] != cards[8][3] * -1:
        return False
    # Third row up
    if cards[6][0] != cards[3][2] * -1:
        return False
    if cards[7][0] != cards[4][2] * -1:
        return False
    if cards[8][0] != cards[5][2] * -1:
        return False

    return True

def get_card_ascii(num):
    if num > 0:
        return " {}".format(num)
    return num

def print_row(c, num):
    print("""
   {}       {}       {}
{} + {}  {} + {}  {} + {}
   {}       {}       {}
    """.format(
        get_card_ascii(c[num + 0][0]),
        get_card_ascii(c[num + 1][0]),
        get_card_ascii(c[num + 2][0]),

        get_card_ascii(c[num + 0][3]),
        get_card_ascii(c[num + 0][1]),
        get_card_ascii(c[num + 1][3]),
        get_card_ascii(c[num + 1][1]),
        get_card_ascii(c[num + 2][3]),
        get_card_ascii(c[num + 2][1]),

        get_card_ascii(c[num + 0][2]),
        get_card_ascii(c[num + 1][2]),
        get_card_ascii(c[num + 2][2]),
    ))

def print_cards(c):
    print_row(c, 0)
    print_row(c, 3)
    print_row(c, 6)

def do_test(i, rot_matrix, pcards, results, j):
    pcards = list(pcards)[:]
    for m in rot_matrix:
        tmp = rotate_all(m, pcards[:])
        if validate(tmp):
            results[j] = tmp
            sys.exit(0)
            return

def reset_results(r):
    for i in range(THREADS):
        r[i] = False

def main(rot_matrix):
    i = 0
    j = 0
    threads = []
    start = datetime.now()
    end   = datetime.now()

    manager = multiprocessing.Manager()
    results = manager.list([False] * THREADS)

    for card_list in itertools.permutations(cards_list):
        if j == THREADS:
            for t in threads:
                t.join()

            for r in results:
                if r:
                    print("Found!")
                    print(r)
                    print_cards(r)
                    sys.exit(0)
            j = 0

        pcards = [ 0 ] * 9
        for idx, c in enumerate(card_list):
            pcards[idx] = CARDS[:][c]

        print(i)
        t = multiprocessing.Process(target=do_test, args=(i, rot_matrix, pcards, results, j))
        threads.append(t)
        t.start()

        i += 1
        j += 1

def get_rot_matrix():
    ret = []
    a = [ 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
    i = 0

    try:
        while True:
            ret.append(a[:])
            a[i] += 1
            while True:
                if a[i] == 4:
                    a[i] = 0
                    i += 1
                    a[i] += 1
                    continue
                i = 0
                break
    except:
        pass
    return ret

def rotate_all(m, cs):
    for i, c in enumerate(cs):
        # print("Rotating card[{}] {} times".format(i, m[i]))
        cs[i] = rotate(c, m[i])
    return cs

def test():
    a = [ 1, 2, 3, 4, 5, 6, 7, 8, 9]
    for t in itertools.permutations(a):
        print(t)

# 262144
# print(len(get_rot_matrix()))
# for m in get_rot_matrix():
#     print(m)

main(get_rot_matrix())
