def check_assignments(filename: str) -> list[int]:
    from re import split
    with open(filename, "r") as file_obj:
        # assignments = [int(assignment) for assignment in split("[^0-9]", file_obj.read())]
        pairs = [pair for pair in file_obj.read().split("\n")]
        assignments = [split("[^0-9]", pair) for pair in pairs]

    total_overlaps = 0

    assignments = [(int(a), int(b), int(c), int(d)) for a, b, c, d in assignments]

    for lo1, hi1, lo2, hi2 in assignments:
        if (lo1 <= lo2 <= hi1) or (lo1 <= hi2 <= hi1) or (lo2 <= lo1 <= hi2) or (lo2 <= hi1 <= hi2):
            total_overlaps += 1

    return total_overlaps


print(check_assignments("test_input.txt"))
print(check_assignments("input.txt"))
