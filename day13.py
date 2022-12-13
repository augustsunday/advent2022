# Author: Colin Cummins
# Github Username: augustsunday
# Date: 12/13/2022
# Description: Custom comparison of distress signal packets
from itertools import zip_longest
from ast import literal_eval
from re import split


def get_packets(filename: str):
    with open(filename, "r") as fo:
        packets = split("\n+", fo.read())
        packets = [literal_eval(packet) for packet in packets]
        return packets


def compare_packets(pair) -> bool:
    left, right = pair
    # print(f"Comparing {left} and {right}")right
    if left is None and right is None:
        return True

    if left is None and right is not None:
        # Left list ran out first
        return True

    if left is not None and right is None:
        # Right list ran out first
        return False

    if type(left) is int and type(right) is int:
        # Both ints
        return left <= right

    if type(left) is list and type(right) is list:
        return all(map(compare_packets, zip_longest(left, right)))

    if type(left) is list:
        return compare_packets(([left[0]], [right]))

    if type(right) is list:
        pair = ([left], [right[0]])
        return compare_packets(pair)

    print("You shouldn't be here")




def prob1(filename):
    good_pairs = []
    packets = get_packets(filename)
    for idx, pair in enumerate(zip(packets[0::2], packets[1::2])):
        if compare_packets(pair):
            good_pairs.append(idx + 1)

    print("Good pairs: ", good_pairs)
    print("Total: ", sum(good_pairs))


prob1("test_input.txt")
# print(compare_packets(([[1], [2, 3, 4]], [[1], 4])))
