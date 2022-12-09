# Author: Colin Cummins
# Github Username: augustsunday
# Date: 12/9/2022
# Description: Follow the tail of a rope

def move_tail(head_pos, tail_pos):
    """
    Get new position of tail based on present coordinates of both
    :param head_pos: (int, int)
    :param tail_pos: (int, int)
    :return:  New tail position (int, int)
    """
    delta_r, delta_c = head_pos[0] - tail_pos[0], head_pos[1] - tail_pos[1]

    if abs(delta_r) == 2 or abs(delta_c) == 2:
        delta_r, delta_c = sorted([-1, delta_r, 1])[1], sorted([-1, delta_c, 1])[1]
        return tail_pos[0] + delta_r, tail_pos[1] + delta_c

    return tail_pos


def move_head(head_pos, heading):
    """
    Move head based on current position and heading
    :param head_pos: Starting position
    :param heading: Up/Down/Left/Right
    :return: New position
    """
    deltas = {"U": (1, 0), "D": (-1, 0), "L": (0, -1), "R": (0, 1)}
    row, col = head_pos
    delta_r, delta_c = deltas[heading]
    row, col = row + delta_r, col + delta_c
    return row, col


def prob1(filename: str) -> int:
    visited = set()
    head_pos, tail_pos = (0, 0), (0, 0)

    with open(filename, "r") as fo:
        for heading, steps in [line.split() for line in fo.read().split("\n")]:
            for _ in range(int(steps)):
                visited.add(tail_pos)
                head_pos = move_head(head_pos, heading)
                tail_pos = move_tail(head_pos, tail_pos)
        visited.add(tail_pos)

    print("Positions visited: ", len(visited))


def prob2(filename: str) -> int:
    visited = set()
    knots = [(0, 0)] * 10

    with open(filename, "r") as fo:
        for heading, steps in [line.split() for line in fo.read().split("\n")]:
            for _ in range(int(steps)):
                visited.add(knots[-1])
                knots[0] = move_head(knots[0], heading)
                for i in range(1, 10):
                    knots[i] = move_tail(knots[i-1], knots[i])
        visited.add(knots[-1])

    print("Positions visited: ", len(visited))


prob1("input.txt")
prob2("input.txt")
