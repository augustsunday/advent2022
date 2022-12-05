# Author: Colin Cummins
# Github Username: augustsunday
# Date: 12/5/2022
# Description: Crate stacking - part 1
def parse_move_instruction(instruction: str) -> list[int, int, int]:
    import re
    template = re.compile("move (\d+) from (\d+) to (\d+)")
    match = template.search(instruction)
    return [int(inst) for inst in match.groups()]


def process_input(filename):
    with open(filename, "r") as file_obj:
        # Build stacks of boxes
        DIVIDER = " 1   2   3   4   5   6   7   8   9"
        line = next(file_obj)
        stacks = [[] for _ in range(9)]
        while line[1] != "1":
            for index, box in enumerate(line[1::4]):
                if box.isalpha():
                    stacks[index].append(box)
            line = next(file_obj)
        stacks = [list(reversed(stack)) for stack in stacks]

        next(file_obj)
        move_instructions = []
        for line in file_obj.readlines():
            move_instructions.append(parse_move_instruction(line))

    return stacks, move_instructions


def problem1(filename):
    stacks, move_instructions = process_input(filename)
    for num_boxes, from_stack, to_stack in move_instructions:
        from_stack -= 1
        to_stack -= 1
        for _ in range(num_boxes):
            stacks[to_stack].append(stacks[from_stack].pop())
    print("".join([stack[-1] for stack in stacks]))


def problem2(filename):
    stacks, move_instructions = process_input(filename)
    for num_boxes, from_stack, to_stack in move_instructions:
        crane = []
        from_stack -= 1
        to_stack -= 1
        for _ in range(num_boxes):
            crane.append(stacks[from_stack].pop())
        for _ in range(num_boxes):
            stacks[to_stack].append(crane.pop())
    print("".join([stack[-1] for stack in stacks]))


problem1("input.txt")
problem2("input.txt")
