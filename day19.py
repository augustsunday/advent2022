# Advent of Code 2022 - Day 19 - Not Enough Minerals

class Solution:
    def __init__(self):
        self.best_geodes = 0
        self.best_producer = None

        self.local_best = dict()

    def dfs(self, turn, resources, bots, costs):
        """
        Return max geodes obtainable with available bots, resources, and remaining time
        Resources, bot costs, and things bots produce are all lists or tuples of form - [ore, clay, obsidian, geode]
        :param turn:
        :param geodes:
        :param resources:
        :param bots:
        :param costs:
        :return:
        """
        if turn == 24:
            return geodes

        # Remember to put a nullbot option in too

        # put in pruning conditions
        # Local - Were we able to get to this turn/geode/resource/bot combo locally in less time? Return 0
        #
        # Global - With what we have, how many more geodes do we have to produce to beat the global
        # max? If it's past the theoretical limit (a world with the lowest bot cost of each category), don't bother proceeding -
        # return 0

        for cost in costs:
            pass








