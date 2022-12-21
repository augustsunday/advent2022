# Author: Colin Cummins
# Github Username: augustsunday
# Date: 12/19/2022
# Description:
from collections import deque


class Droplet:
    def __init__(self, filename):
        self.drop_set = set()
        with open(filename, "r") as fo:
            coords = [(int(x), int(y), int(z)) for x, y, z in [triple.split(",") for triple in fo.read().split("\n")]]

        self.upper_bound = 0
        self.lower_bound = float("inf")
        for x, y, z in coords:
            self.drop_set.add((x, y, z))
            for coord in [x, y, z]:
                self.upper_bound = max(self.upper_bound, coord)
                self.lower_bound = min(self.lower_bound, coord)
        # Make room for steam to expand
        self.upper_bound += 10
        self.lower_bound -= 10

    def is_in_bounds(self, coord, lower_bound, upper_bound):
        x, y, z = coord
        return (lower_bound <= x <= upper_bound) and (lower_bound <= y <= upper_bound) and (lower_bound <= z <= upper_bound)

    def get_neighbors(self, coord):
        x, y, z = coord
        return []

    def flood_fill(self):
        start = (-1, -1, -1)
        visited = set()
        queue = deque()
        queue.append(start)
        visited.add(start)
        while queue:
            coord = queue.popleft()
            x, y, z = coord
            visited.add(coord)
            for neighbor in [(x + 1, y, z), (x - 1, y, z), (x, y + 1, z), (x, y - 1, z), (x, y, z + 1), (x, y, z - 1)]:
                if neighbor not in visited and neighbor not in self.drop_set and self.is_in_bounds(neighbor, self.lower_bound, self.upper_bound):
                    queue.append(neighbor)
                    visited.add(neighbor)

        return visited

    def surface_area(self):
        water = self.flood_fill()
        area = 0
        for cube in self.drop_set:
            x, y, z = cube
            for neighbor in [(x + 1, y, z), (x - 1, y, z), (x, y + 1, z), (x, y - 1, z), (x, y, z + 1), (x, y, z - 1)]:
                if neighbor not in self.drop_set:
                    area += 1

        return area

    def exterior_surface(self):
        water = self.flood_fill()
        ext_area = 0
        for cube in self.drop_set:
            x, y, z = cube
            for neighbor in [(x + 1, y, z), (x - 1, y, z), (x, y + 1, z), (x, y - 1, z), (x, y, z + 1), (x, y, z - 1)]:
                if neighbor in water:
                    ext_area += 1

        return ext_area






lava = Droplet("test_input.txt")
print("Test Input: ")
print(lava.surface_area())
print(lava.exterior_surface())

print("Prob1, 2: ")
lava = Droplet("input.txt")
print(lava.surface_area())
print(lava.exterior_surface())

