# Author: Colin Cummins
# Github Username: augustsunday
# Date: 12/13/2022
# Description: Custom comparison of distress signal packets
from itertools import zip_longest
from ast import literal_eval
from re import split
from functools import cmp_to_key


def get_packets(filename: str):
    with open(filename, "r") as fo:
        packets = split("\n+", fo.read())
        packets = [literal_eval(packet) for packet in packets]
        return packets


def compare_packets(pair) -> bool:
    left, right = pair
    print(f"Comparing {left} and {right}")

    if type(left) is int and type(right) is int:
        # Both ints
        if left == right:
            return 'proceed'
        if left < right:
            return True
        if left > right:
            return False

    if type(left) is list and type(right) is list:
        if len(left) == 0 and len(right) == 0:
            return 'proceed'
        if len(left) == 0:
            return True
        if len(right) == 0:
            return False

        for left, right in zip_longest(left, right):
            if left is None:
                return True
            if right is None:
                return False
            curr = compare_packets((left, right))
            if curr == 'proceed':
                continue
            return curr

        return 'proceed'
        # return all(map(compare_packets, zip_longest(left, right)))

    if type(left) is list:
        return len(left) == 0 or compare_packets((left, [right]))

    if type(right) is list:
        return len(right) != 0 and compare_packets(([left], right))

def compare(l, r):
    pair = (l, r)
    return -1 if compare_packets(pair) else 1



def prob1(filename):
    good_pairs = []
    packets = get_packets(filename)
    for idx, pair in enumerate(zip(packets[0::2], packets[1::2])):
        result = compare_packets(pair)
        if result:
            good_pairs.append(idx + 1)
        print(result)

    print("Good pairs: ", good_pairs)
    print("Total: ", sum(good_pairs))

def prob2(filename):
    packets = get_packets(filename)
    packets.extend([[[2]], [[6]]])
    packets.sort(key=cmp_to_key(compare))
    print(*packets, sep="\n")
    idx1 = packets.index([[2]]) + 1
    idx2 = packets.index([[6]]) + 1
    print("Code Key: ", idx1 * idx2)

    return packets

prob2("input.txt")