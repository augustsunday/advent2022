# Author: Colin Cummins
# Github Username: augustsunday
# Date: 12/8/2022
# Description:
# Prob 1 - Find visible trees in forest

def input_to_dict(filename: str) -> dict[int]:
    forest = dict()
    with open(filename, "r") as fo:
        for row_idx, row in enumerate(fo.read().split("\n")):
            for col_idx, num in enumerate(row):
                forest[(row_idx, col_idx)] = int(num)

    return forest


def find_visible(forest, trees):
    # Take input list of trees and return only those trees visible when looking from left
    visible_trees = [trees[0]]
    for tree in trees:
        if forest[tree] > forest[visible_trees[-1]]:
            visible_trees.append(tree)

    return visible_trees


def get_scenic_factor(coords, forest):
    """
    Get scenic factor of one line of trees in one direction
    :param trees: Heights of trees in line
    :return: List of scenic factors, in order of trees. How many trees can a tree see to its left in the sequence?
    """
    heights = [forest[coord] for coord in list(coords)]
    tree_stack = [0]  # index of a tree in heights
    scenic = [0] * len(heights)
    for i in range(len(heights)):
        while tree_stack and heights[i] > heights[tree_stack[-1]]:
            tree_stack.pop()
        if not tree_stack:
            scenic[i] = i
            tree_stack.append(i)
        else:
            scenic[i] = i - tree_stack[-1]
            tree_stack.append(i)

    return scenic


def update_scenic_factor(coords, scenics, all_scenics):
    for coord, scenic in zip(coords, scenics):
        all_scenics[coord] *= scenic


def prob1(filename: str) -> int:
    visible = set()
    forest = input_to_dict(filename)
    side_length = int(len(forest) ** 0.5)
    print('Forest Side Length: ', side_length)
    for i in range(side_length):
        trees = [(i, j) for j in range(side_length)]
        visible.update(find_visible(forest, trees))
        trees.reverse()
        visible.update(find_visible(forest, trees))

        trees = [(j, i) for j in range(side_length)]
        visible.update(find_visible(forest, trees))
        trees.reverse()
        visible.update(find_visible(forest, trees))

    print("Number of trees visible:", len(visible))


def prob2(filename: str) -> int:
    from collections import defaultdict
    forest = input_to_dict(filename)
    side_length = int(len(forest) ** 0.5)
    scenic_factor = defaultdict(lambda:1)

    for i in range(side_length):
        # Row, Looking left
        trees = [(i, j) for j in range(side_length)]
        row = get_scenic_factor(trees, forest)
        update_scenic_factor(trees, row, scenic_factor)

        # Row, looking right
        row = get_scenic_factor(reversed(trees), forest)
        row.reverse()
        update_scenic_factor(trees, row, scenic_factor)

        # Column, Looking down
        trees = [(j, i) for j in range(side_length)]
        row = get_scenic_factor(trees, forest)
        update_scenic_factor(trees, row, scenic_factor)

        # Column, looking up
        row = get_scenic_factor(reversed(trees), forest)
        row.reverse()
        update_scenic_factor(trees, row, scenic_factor)

    print("Highest Scenic Factor: ", max(scenic_factor.values()))


prob1("input.txt")
prob2("input.txt")
