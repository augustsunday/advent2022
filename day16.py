# Author: Colin Cummins
# Github Username: augustsunday
# Date: 12/16/2022
# Description: Advent of Code 2022, Day 16
# Switch on pressure valves in volcano
import re

from dijkstra import Graph, DijkstraSPF
from re import search, compile


def parse_line(line: str):
    node_pattern = re.compile("[A-Z]{2}")
    num_pattern = re.compile("[0-9]+")
    origin, *neighbors = re.findall(node_pattern, line)
    flow_rate = int(re.search(num_pattern, line)[0])
    print(origin, flow_rate, neighbors)
    return origin, flow_rate, neighbors


class Volcano:
    def __init__(self, filename):
        self.graph = Graph()
        self.dijkstras = dict()
        self.flow_rates = []
        self.nodes = []
        with open(filename, "r") as fo:
            for line in fo.read().split("\n"):
                origin, flow_rate, neighbors = parse_line(line)
                if flow_rate != 0:
                    self.nodes.append(origin)
                    self.flow_rates.append(flow_rate)
                for neighbor in neighbors:
                    self.graph.add_edge(origin, neighbor, 1)
            for node in self.nodes:
                self.dijkstras[node] = DijkstraSPF(self.graph, node)
        self.valve_state = 0
        for idx, flow_rate in enumerate(self.flow_rates):
            if flow_rate != 0:
                self.valve_state |= (1 << idx)
                print(self.valve_state)
        print(f"Initial Valve State: {self.valve_state:>08b}")



solution = Volcano("input.txt")
