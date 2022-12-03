# Similar to day 1, but need to split into groups of 3 lines

def find_shared_badge(elf1, elf2, elf3) -> str:
    return (set(elf1) & set(elf2) & set(elf3)).pop()


def priority_score(priority: str) -> int:
    if priority.islower():
        return ord(priority) - ord("a") + 1

    return ord(priority) - ord("A") + 27


def badge_reorg(filename: str) -> int:
    with open(filename, "r") as file_obj:
        solution = 0
        elves = [elf for elf in file_obj.read().split("\n")]
        while elves:
            elf1, elf2, elf3 = elves.pop(), elves.pop(), elves.pop()
            solution += priority_score(find_shared_badge(elf1, elf2, elf3))

        return solution


print(badge_reorg("test_input.txt"))
print(badge_reorg("input.txt"))
