# Author: Colin Cummins
# Github Username: augustsunday
# Date: 12/16/2022
# Description: Advent of Code 2022, Day 16
# Switch on pressure valves in volcano
import re

from dijkstar import Graph, find_path
import re
from functools import cache, reduce
from itertools import combinations


def parse_line(line: str):
    node_pattern = re.compile("[A-Z]{2}")
    num_pattern = re.compile("[0-9]+")
    origin, *neighbors = re.findall(node_pattern, line)
    flow_rate = int(re.search(num_pattern, line)[0])
    print(origin, flow_rate, neighbors)
    return origin, flow_rate, neighbors


def flip_valve(valve_state: int, valvenum: int) -> int:
    # Flip state of valve at valvenum
    return valve_state ^ (1 << valvenum)


def is_closed(valve_state: int, valvenum: int) -> bool:
    # Returns true if valve is currently closed (0)
    return valve_state & (1 << valvenum) != 0


class Volcano:
    def __init__(self, filename):
        self.graph = Graph()
        self.flow_rates = []
        self.nodes = []
        self.valve_dict = dict()
        self.best_pressure = 0
        with open(filename, "r") as fo:
            for idx, line in enumerate(fo.read().split("\n")):
                origin, flow_rate, neighbors = parse_line(line)
                self.nodes.append(origin)
                self.valve_dict[idx] = origin
                self.flow_rates.append(flow_rate)
                for neighbor in neighbors:
                    self.graph.add_edge(origin, neighbor, 1)
                self.graph.add_edge("AA", "AA", 0)
        self.total_nodes = len(self.nodes)

        # Build valve state bitmask
        self.valve_state = 0
        for idx, flow_rate in enumerate(self.flow_rates):
            if flow_rate != 0:
                self.valve_state |= (1 << idx)

        self.start_valve = self.nodes.index("AA")

        self.partitions = set()

    def generate_partitions(self):
        # Generate all possible partitions of the valves that need to be turned on
        # Return a list of pairs of valve states. These are the 'marching orders' for you and the elephant. Each of you
        # will attempt to maximize pressure output for their own assigned valves

        partitions = []
        result = []
        print("Generating Partitions:")
        valves_to_open = list(filter(lambda x: self.flow_rates[x] > 0, range(self.total_nodes)))
        all_open_set = set(valves_to_open)
        print("You need to open valves:", list(valves_to_open))
        print("Partition Pairs:")
        for i in range(len(valves_to_open) + 1):
            combos = list(combinations(valves_to_open, i))
            partitions.extend(combos)

        valve_set = set(valves_to_open)
        masks_seen = set()
        for combo in partitions:
            first_mask = reduce(lambda x, y: x | 1 << y, combo, 0)
            second_mask = first_mask ^ self.valve_state
            if second_mask not in masks_seen:
                masks_seen.add(first_mask)
                result.append((first_mask, second_mask))

        return result

    @cache
    def get_best_pressure(self, current_valve, remaining_time: int,
                          valve_state):
        """
        Return best possible pressure going forward from given conditions
        :param current_valve:
        :param remaining_time:
        :param current_pressure:
        :param valve_state:
        :return:
        """
        if remaining_time == 0 or valve_state == 0:
            return 0

        # From where we are, can we reach a given closed valve and flip it open before we're out of time?
        # If we can, try that branch
        best_pressure = 0
        for try_valve in range(self.total_nodes):
            dist_to_valve = find_path(self.graph, self.valve_dict[current_valve],
                                      self.valve_dict[try_valve]).total_cost + 1
            if is_closed(valve_state, try_valve) and dist_to_valve <= remaining_time:
                possible_gain = self.flow_rates[try_valve] * (remaining_time - dist_to_valve)
                next_time = remaining_time - dist_to_valve
                valve_state = flip_valve(valve_state, try_valve)
                best_pressure = max(best_pressure,
                                    possible_gain + self.get_best_pressure(try_valve, next_time, valve_state))
                # backtrack
                valve_state = flip_valve(valve_state, try_valve)

        return best_pressure


assert flip_valve(0b1111, 0) == 0b1110
assert is_closed(0b0100, 2) is True
assert is_closed(0b1000, 2) is False

solution = Volcano("test_input.txt")
assert solution.get_best_pressure(solution.start_valve, 30, solution.valve_state) == 1651
print(solution.generate_partitions())

print("Problem 1:")
# solution = Volcano("test_input.txt")
# print(solution.get_best_pressure(solution.start_valve, 30, solution.valve_state))

print("Problem 2")
# Remember to start at time 26
solution = Volcano("input.txt")
prob2_best = 0
print("Marching orders:")
for first_mask, second_mask in solution.generate_partitions():
    prob2_best = max(prob2_best,
                     solution.get_best_pressure(solution.start_valve, 26, first_mask) + solution.get_best_pressure(
                         solution.start_valve, 26, second_mask))
    print(f"{first_mask:0b}, {second_mask:0b}, {prob2_best}")
print(prob2_best)
