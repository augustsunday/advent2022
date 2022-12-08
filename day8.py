# Author: Colin Cummins
# Github Username: augustsunday
# Date: 12/8/2022
# Description:
# Prob 1 - Find visible trees in forest

def input_to_dict(filename: str)->dict[int]:
    forest = dict()
    with open(filename, "r") as fo:
        for row_idx, row in enumerate(fo.read().split("\n")):
            for col_idx, num in enumerate(row):
                forest[(row_idx, col_idx)] = int(num)

    return forest



def prob1(filename: str) -> int:
    forest = input_to_dict(filename)
    print('Forest: ', forest)

prob1("input.txt")
