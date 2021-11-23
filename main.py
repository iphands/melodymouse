import random
import hashlib

BU = 1
BD = -1
RU = 2
RD = -2
GU = 4
GD = -3
PD = 4
PU = -4

sums = []

cards = [
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

def rotate(c):
    return [ c[3], c[0], c[1], c[2] ]

def get_rand():
    for card_i, c in enumerate(cards):
        n = random.randint(0, 3)
        # print("Rotating card {} ({}) {} times:".format(card_i, card, n))
        for i in range(0, n):
            cards[card_i] = rotate([c[0], c[1], c[2], c[3]])
            # print(cards[card_i])

    random.shuffle(cards)

def validate():
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

def print_row(num):
    print("""
   {}       {}       {}
{} + {}  {} + {}  {} + {}
   {}       {}       {}
    """.format(
        get_card_ascii(cards[num + 0][0]),
        get_card_ascii(cards[num + 1][0]),
        get_card_ascii(cards[num + 2][0]),

        get_card_ascii(cards[num + 0][3]),
        get_card_ascii(cards[num + 0][1]),
        get_card_ascii(cards[num + 1][3]),
        get_card_ascii(cards[num + 1][1]),
        get_card_ascii(cards[num + 2][3]),
        get_card_ascii(cards[num + 2][1]),

        get_card_ascii(cards[num + 0][2]),
        get_card_ascii(cards[num + 1][2]),
        get_card_ascii(cards[num + 2][2]),
    ))

def print_cards():
    print_row(0)
    print_row(1)
    print_row(2)

def main():
    while(True):
        get_rand()
        #sum_str = hashlib.md5(str(cards).encode('utf-8')).hexdigest()
        #if not sum_str in sums:
        #    sums.append(sum_str)
        # print("{}: {}".format(len(sums), sum_str))
        if validate():
            print_cards()
            break

main()
