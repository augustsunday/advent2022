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

def get_scenic_factor(heights):
    """
    Get scenic factor of one line of trees in one direction
    :param trees: Heights of trees in line
    :return: List of scenic factors, in order of trees. How many trees can a tree see to its left?
    """
    tree_stack = [0] #index of a tree in heights
    scenic = [0] * len(heights)
    for i in range(len(heights)):
        if not tree_stack:
            scenic[i] = i
            tree_stack.append(i)
        elif heights[i] <= heights[tree_stack[-1]]:
            scenic[i] = i - tree_stack[-1]
            tree_stack.append(i)
        else:
            while tree_stack and heights[i] > heights[tree_stack[-1]]:

            tree_stack.append(i)



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
    forest = input_to_dict(filename)
    side_length = int(len(forest) ** 0.5)
    scenic_factor = [[1] * side_length for _ in range(side_length)]
    for i in range(side_length):
        trees = [(i, j) for j in range(side_length)]
        trees.reverse()

        trees = [(j, i) for j in range(side_length)]
        trees.reverse()


# prob2("input.txt")
test_list = [1, 2, 3, 4, 5]
get_scenic_factor(test_list)