# Author: Colin Cummins
# Github Username: augustsunday
# Date: 12/1/2022
# Description:
# Wrap Advent of Code input files for easy parsing

class InputParser():
    def __init__(self, input_filename):
        self.input_filename = input_filename

    def parse_to_list(self):
        with open(self.input_filename, "r") as file_obj:
            file_data = file_obj.read()
            return file_data.splitlines()
