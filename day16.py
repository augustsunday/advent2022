# Author: Colin Cummins
# Github Username: augustsunday
# Date: 12/16/2022
# Description: Advent of Code 2022, Day 16
# Switch on pressure valves in volcano
import re

from dijkstar import Graph, find_path
from re import search, compile
from functools import cache


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
                self.graph.add_edge("AA","AA",0)
        self.total_nodes = len(self.nodes)


        # Build valve state bitmask
        self.valve_state = 0
        for idx, flow_rate in enumerate(self.flow_rates):
            if flow_rate != 0:
                self.valve_state |= (1 << idx)
        print(f"Initial Valve State: {self.valve_state:>08b}")

        self.start_valve = self.nodes.index("AA")

    @ cache
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
            dist_to_valve = find_path(self.graph, self.valve_dict[current_valve], self.valve_dict[try_valve]).total_cost + 1
            if is_closed(valve_state, try_valve) and dist_to_valve <= remaining_time:
                possible_gain = self.flow_rates[try_valve] * (remaining_time - dist_to_valve)
                next_time = remaining_time - dist_to_valve
                valve_state = flip_valve(valve_state, try_valve)
                best_pressure = max(best_pressure, possible_gain + self.get_best_pressure(try_valve, next_time, valve_state))
                # backtrack
                valve_state = flip_valve(valve_state, try_valve)

        return best_pressure




solution = Volcano("input.txt")
print(solution.get_best_pressure(solution.start_valve, 30, solution.valve_state))

assert flip_valve(0b1111, 0) == 0b1110
assert is_closed(0b0100, 2) is True
assert is_closed(0b1000, 2) is False
