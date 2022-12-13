# Advent of Code 2022 - Day 12
def create_grid(filename: str):
    # Create grid from AoC input
    # return grid and tuples for start/end points
    start, end = None, None
    with open(filename, "r") as fo:
        rows = fo.read().split("\n")
        grid = [[0 for i in range(len(rows[0]))] for _ in range(len(rows))]
    for i in range(len(rows)):
        for j in range(len(rows[0])):
            if rows[i][j] == "S":
                start = i, j
                grid[i][j] = 0
            elif rows[i][j] == "E":
                end = i, j
                grid[i][j] = ord("z") - ord("a")
            else:
                grid[i][j] = ord(rows[i][j]) - ord("a")
    print("Grid created:", grid)
    return grid, start, end


def solve_puzzle(Board, Source, Destination):
    """
    Navigates the maze Board from Source to Destination
    :param Board: Board to navigate list[list[str]]
    :param Source: (Row, Column) of starting point - tuple[int,int]
    :param Destination: (Row, Column) of goal - tuple[int,int]
    :return: List of coordinates of the path to goal, in order. Returns None if no path to goal
    """
    from heapq import heappush, heappop

    print(Board, Source, Destination)

    dist = [[float("inf")] * len(Board[0]) for _ in range(len(Board))]

    prev = [[None] * len(Board[0]) for _ in range(len(Board))]

    dist[Source[0]][Source[1]] = 0
    prev[Source[0]][Source[1]] = Source

    pq = [(0, Source[0], Source[1])]  # tentative_dist, row, col

    path = []
    visited = set()

    # print("Source: ", Source)
    # print("Dest: ", Destination)
    # print(*Board, sep='\n')

    def is_in_bounds(r, c):
        return -1 < r < len(Board) and -1 < c < len(Board[0])

    def is_reachable(row, col, r, c):
        return Board[r][c] - Board[row][col] < 2

    while pq:
        distance, row, col = heappop(pq)
        if (row, col) not in visited:
            # print("visited", row, col)
            visited.add((row, col))
            dist[row][col] = distance
            for neighbor in [(row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1)]:
                r, c = neighbor
                if is_in_bounds(r, c) and is_reachable(row, col, r, c) and dist[row][col] + 1 < dist[r][c]:
                    dist[r][c] = dist[row][col] + 1
                    prev[r][c] = (row, col)
                    heappush(pq, (dist[r][c], r, c))

    # Build up path in reverse
    curr = Destination
    while curr != Source:
        path.append(curr)
        r, c = curr
        curr = prev[r][c]
    path.append(Source)
    path.reverse()

    # Create direction string
    directions = []
    shift_to_direction = {(1, 0): "D", (-1, 0): "U", (0, 1): "R", (0, -1): "L"}
    for i in range(len(path) - 1):
        pr1, pc1 = path[i]
        pr2, pc2 = path[i + 1]
        current_direction = (pr2 - pr1, pc2 - pc1)
        # print(current_direction)
        # print(shift_to_direction[current_direction])
        directions.append(shift_to_direction[current_direction])
    direction_string = "".join(directions)

    return path, direction_string


def prob1(filename):
    board, start, end = create_grid(filename)
    path, directions = solve_puzzle(board, start, end)
    print("Board: ", board)
    print(f"Start: {start}     End: {end}")
    print("Path: ", path)
    print("Steps: ", len(path) - 1)
    print("Directions: ", directions)


def prob2(filename):
    # Notes: find dist from end to each a, but keep the distance map from search to search?

prob1("input.txt")
