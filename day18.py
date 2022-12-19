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

    def get_surface_area(self):
        longest_dimension = max(self.max_x, self.max_y, self.max_z)
        seen = set()
        queue = deque()
        # SHould be x, y, 0 and x, y, longest in different permutations
        for i in range(longest_dimension + 1):
            for j in range(longest_dimension + 1):
                    queue.append((i, j, 0))
                    seen.add((i, j, 0))
        surface_area = 0
        while queue:
            coord = queue.popleft()
            x, y, z = coord
            for xshift, yshift, zshift in itertools.product([-1, 0, 1], repeat=3):
                new_coord = (x + xshift, y + yshift, z + zshift)
                ax, ay, az = new_coord[0] - coord[0], new_coord[1] - coord[1], new_coord[2] - coord[2]
                dist = sqrt( ax ** 2 + ay ** 2 + az ** 2)
                if new_coord in self.drop_set and dist == 1:
                        surface_area += 1
                elif self.is_in_bounds(new_coord, longest_dimension + 2) and new_coord not in seen and new_coord not in self.drop_set:
                    seen.add(new_coord)
                    queue.append(new_coord)
        return surface_area


drop = Droplet("test_input.txt")
print(drop.get_surface_area())



