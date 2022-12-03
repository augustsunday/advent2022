# Split string evenly, put each string in a set, find intersection of sets. Add intersection to priorities list.
# Tally up priorities

def find_priority(rucksack:str)->str:
    return set(rucksack[:len(rucksack)//2]).intersection(set(rucksack[len(rucksack)//2:])).pop()

def priority_score(priority:str)->int:
    if priority.islower():
        return ord(priority) - ord("a") + 1

    return ord(priority) - ord("A") + 27

def rucksack_reorg(filename: str) -> int:
    priorities = []
    with open(filename, "r") as file_obj:
        solution = [rucksack for rucksack in file_obj.read().split("\n")]
        solution = map(find_priority, solution)
        solution = map(priority_score, solution)
        solution = sum(solution)
        return solution


print(rucksack_reorg("test_input.txt"))
print(rucksack_reorg("input.txt"))