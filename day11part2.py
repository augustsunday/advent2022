# Description: Monkeys playing keep-away with your items
from collections import deque


class Monkey():
    def __init__(self, block: str) -> None:
        self.inspected_count = 0
        self.neighbors = None
        print("Initializing monkey...")
        lines = block.split('\n')

        self.items = deque([int(item) for item in lines[1].lstrip("  Starting items: ").split(", ")])
        print("Starting Items: ", self.items)

        operation, operand = lines[2].lstrip("  Operation: new = old ").split(" ")
        if operand == "old":
            self.operation = lambda x: x ** 2
        elif operation == "*":
            self.operation = lambda x: x * int(operand)
        elif operation == "+":
            self.operation = lambda x: x + int(operand)
        elif operation == "-":
            self.operation = lambda x: x - int(operand)
        print("Inspection : ", self.operation)

        self.test_divisor = int(lines[3].lstrip("  Test: divisible by "))
        print("Test Divisor", self.test_divisor)

        self.true_recipient = int(lines[4].lstrip("    If true: throw to monkey "))
        self.false_recipient = int(lines[5].lstrip("    If false: throw to monkey "))
        print("Throw to monkey", self.true_recipient, "if true")
        print("Throw to monkey", self.false_recipient, "if false")
        print()

    def catch_item(self, item: int):
        self.items.append(item)

    def store_neighbors(self, neighbors):
        self.neighbors = neighbors

    def inspect_next(self):
        self.inspected_count += 1
        curr_item = self.items.popleft()
        curr_item = self.operation(curr_item)
        # Perform reduction
        curr_item = curr_item % (2 * 7 * 13 * 3 * 19 * 5 * 11 * 17)
        recipient = self.true_recipient if curr_item % self.test_divisor == 0 else self.false_recipient
        self.neighbors[recipient].catch_item(curr_item)

    def take_turn(self):
        while self.items:
            self.inspect_next()

    def __repr__(self):
        return ", ".join([str(item) for item in list(self.items)])

    def get_inspect_count(self):
        return self.inspected_count


class Solution():
    def __init__(self, filename):
        self.round = 1
        self.monkeys = []

        with open(filename, "r") as fo:
            for monkey_block in fo.read().split("\n\n"):
                self.monkeys.append(Monkey(monkey_block))

        for monkey in self.monkeys:
            monkey.store_neighbors(self.monkeys)

        print("Init Complete\nStarting Items:")
        for monkey in self.monkeys:
            print(monkey)

    def execute_round(self):
        for monkey in self.monkeys:
            monkey.take_turn()
        print(f"Status after Round {self.round}")
        for idx, monkey in enumerate(self.monkeys):
            print(f"Monkey {idx}: {monkey}")

        self.round += 1

    def get_final_counts(self):
        return [monkey.inspected_count for monkey in self.monkeys]

    def get_monkey_business(self):
        counts = list(reversed(sorted(self.get_final_counts())))
        return counts[0] * counts[1]


def prob1(filename, rounds):
    scenario = Solution(filename)
    for i in range(rounds):
        scenario.execute_round()
    print("Items Inspected: ",scenario.get_final_counts())
    print("Monkey Business: ", scenario.get_monkey_business())


prob1("input.txt", 10000)
