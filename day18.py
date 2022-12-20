# Author: Colin Cummins
# Github Username: augustsunday
# Date: 12/19/2022
# Description:
from collections import deque
import itertools
from math import sqrt


class Droplet:
    def __init__(self, filename):
        self.drop_set = set()
        with open(filename, "r") as fo:
            coords = [(int(x), int(y), int(z)) for x, y, z in [triple.split(",") for triple in fo.read().split("\n")]]

        max_x, max_y, max_z = float("-inf"), float("-inf"), float("-inf")
        min_x, min_y, min_z = float("inf"), float("inf"), float("inf")

        for x, y, z in coords:
            self.drop_set.add((x, y, z))
            max_x, max_y, max_z = max(max_x, x), max(max_y, y), max(max_z, z)
            min_x, min_y, min_z = min(min_x, x), min(min_y, y), min(min_z, z)

        self.max_x, self.max_y, self.max_z = x, y, z
        print(self.drop_set)
        print(min_x, min_y, min_z)
        print(max_x, max_y, max_z)

    def is_in_bounds(self, coord, bound):
        x, y, z = coord
        return 0 <= x <= bound and 0 <= y <= bound and 0 <= z <= bound




