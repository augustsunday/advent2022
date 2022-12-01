"""
Day 1-2
Find total calories of top 3 elves
"""


def get_calories():
    from input_parser import InputParser
    input = InputParser("input.txt")

    calories_per_elf = []
    current_calories = 0

    for elf_cal in input.parse_to_list():
        if elf_cal == "":
            calories_per_elf.append(current_calories)
            current_calories = 0
        else:
            current_calories += int(elf_cal)
    calories_per_elf.append(current_calories)

    calories_per_elf.sort(reverse=True)
    print(calories_per_elf)

    return sum(calories_per_elf[0:3])


print(get_calories())
