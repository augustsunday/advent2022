# Author: Colin Cummins
# Github Username: augustsunday
# Date: 12/14/2022
# Description:
import re
from itertools import pairwise
from collections import defaultdict


class Solution:
    def __init__(self, filename):
        self.create_grid(filename)
        self.render_grid()

    def create_grid(self, filename):
        # Get dimensions of grid
        strokes = []

        self.min_row = 0
        self.max_row = 0
        self.min_col = float("inf")
        self.max_col = 0
        with open(filename, "r") as fo:
            for line in fo.read().split("\n"):
                stroke = [[int(row), int(col)] for row, col in
                          [pair.split(',') for pair in re.findall("\d+,\d+", line)]]
                strokes.append(stroke)
                for col, row in stroke:
                    self.max_row = max(self.max_row, row)
                    self.max_col = max(self.max_col, col)
                    self.min_col = min(self.min_col, col)

            # Create empty grid
            self.grid = defaultdict(lambda: ".")


            # Draw Lines
            for stroke in strokes:
                for start, end in pairwise(stroke):
                    self.draw_line(start, end)

            print(f"Min Row: {self.min_row}, Max Row: {self.max_row}, Min Col: {self.min_col}, Max Col: {self.max_col}")

    def draw_line(self, start, end):
        if start > end:
            start, end = end, start
        c_delta, r_delta = end[0] - start[0], end[1] - start[1]
        line_length = max(c_delta, r_delta) + 1
        c_delta = min(1, c_delta)
        r_delta = min(1, r_delta)
        while start != end:
            col, row = start
            self.grid[(row,col)] = "#"
            col, row = col + c_delta, row + r_delta
            start = [col, row]
        self.grid[(row,col)] = "#"

    def render_grid(self):
        for row in range(self.min_row,self.max_row):
            for col in range(self.min_col, self.max_col):
                print(self.grid[(row, col)], end="")
            print("\n")

    def drop_sand(self, has_floor = False):
        stack = [[0, 500]]
        grains = 0

        if has_floor:
            self.floor = self.max_row + 2
            self.max_row += 3

        while stack:
            row, col = stack[-1]

            # Falling into the void?
            if row > self.max_row:
                self.render_grid()
                print("Sand is falling into the void!")
                print(f"Total Grains: {grains}")
                return grains

            # Next path
            if has_floor and row + 1 == self.floor:
                self.grid[(row,col)] = "o"
                grains += 1
                stack.pop()
            elif self.grid[(row + 1, col)]== ".":
                stack.append([row+1, col])
            elif self.grid[(row + 1, col - 1)] == ".":
                stack.append([row + 1, col - 1])
            elif self.grid[(row + 1, col + 1)] == ".":
                stack.append([row + 1, col + 1])
            else:
                self.grid[(row,col)] = "o"
                grains += 1
                stack.pop()

        print("The sand has plugged up the hole!")
        print(f"Total Grains: {grains}")

    def prob1(self):
        self.drop_sand()

    def prob2(self):
        self.drop_sand(has_floor=True)
        self.render_grid()


problem = Solution("input.txt")
problem.prob1()

problem = Solution("input.txt")
problem.prob2()

