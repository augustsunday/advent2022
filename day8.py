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
    from_left, from_right, from_top, from_bottom = set(), set(), set(), set()
    forest = input_to_dict(filename)
    side_length = int(len(forest) ** 0.5)
    print('Forest Side Length: ', side_length)
    for i in range(side_length):
        trees = [(i, j) for j in range(side_length)]
        from_left.update(find_visible(forest, trees))
        trees.reverse()
        from_right.update(find_visible(forest, trees))

        trees = [(j, i) for j in range(side_length)]
        from_top.update(find_visible(forest, trees))
        trees.reverse()
        from_bottom.update(find_visible(forest, trees))

    # Find all intersections, then add edges back in
    visible_all = from_bottom & from_top & from_left & from_right
    visible_all.update([(0, j) for j in range(side_length)])
    visible_all.update([(j, 0) for j in range(side_length)])

    print("Visible from left: ", from_left)
    print("Visible from right: ", from_right)
    print("Visible from top: ", from_top)
    print("Visible from bottom: ", from_bottom)
    print("Visible from all directions", visible_all)
    print("Number of trees visible from all directions:", len(visible_all))

prob1("input.txt")
