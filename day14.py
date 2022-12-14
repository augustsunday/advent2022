# Author: Colin Cummins
# Github Username: augustsunday
# Date: 12/14/2022
# Description:
import re


class Solution:
    def __init__(self, filename):
        self.create_grid(filename)
        self.drop_point = []
        pass

    def create_grid(self, filename):
        with open(filename, "r") as fo:
            file_dump = fo.read()
            numbers = re.findall("\d+", file_dump)
            numbers = [int(num) for num in numbers]
            self.min_row = 0
            self.max_row = max(numbers[1::2]) + 1
            self.min_col = min(numbers[0::2])
            self.max_col = max(numbers[0::2]) + 1
            print(f"Min Row: {self.min_row}, Max Row: {self.max_row}, Min Col: {self.min_col}, Max Col: {self.max_col}")


problem = Solution("test_input.txt")
