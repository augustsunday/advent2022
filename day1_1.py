"""
Day 1-1
Find elf w/ most calories in food
"""


def get_calories():
    from input_parser import InputParser
    input = InputParser("input.txt")

    most_calories = 0
    current_calories = 0

    for elf in input.parse_to_list():
        if elf == "":
            most_calories = max(most_calories, current_calories)
            current_calories = 0
        else:
            current_calories += int(elf)

    return most_calories


print(get_calories())
