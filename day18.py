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

        self.lower_bound, self.upper_bound = -1, max(self.max_x, self.max_y, self.max_z) + 1


    def is_in_bounds(self, coord, lower_bound, upper_bound):
        x, y, z = coord
        return lower_bound <= x <= upper_bound and lower_bound <= y <= upper_bound and lower_bound <= z <= upper_bound

    def flood_fill(self):

        visited = set()
        queue = deque()
        queue.append((-1, -1, -1))
        visited.add((-1, -1, -1))
        while queue:
            coord = queue.popleft()
            visited.add(coord)
            x, y, z = coord
            for neighbor in [(x + 1, y, z), (x -1, y, z), (x, y+1, z), (x, y-1, z), (x, y, z+1), (x, y, z -1)]:
                if neighbor not in visited and neighbor not in self.drop_set and self.is_in_bounds(neighbor, self.lower_bound, self.upper_bound):
                    queue.append(neighbor)

        return visited

    def surface_area(self):
        water = self.flood_fill()
        surface_area = 0
        for cube in self.drop_set:
            x, y, z = cube
            for neighbor in [(x + 1, y, z), (x -1, y, z), (x, y+1, z), (x, y-1, z), (x, y, z+1), (x, y, z -1)]:
                if neighbor in water:
                    surface_area += 1

        return surface_area


# testing
lava = Droplet("simple_input.txt")
assert len(lava.flood_fill()) == 123
assert lava.surface_area() == 10

drop = Droplet("test_input.txt")
drop.flood_fill()
# assert lava.surface_area() == 64
#
# # Prob 1
# lava = Droplet("input.txt")
# lava.flood_fill()
# print("Prob 1 - Surface Area of Lava Droplet is:",lava.surface_area())
