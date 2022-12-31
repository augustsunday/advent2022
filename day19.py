# Advent of Code 2022 - Day 19 - Not Enough Minerals
from functools import cache


class Solution:
    def __init__(self):
        self.best_geodes = 0
        self.best_producer = None

        self.local_best = dict()

        self.current_blueprint = None
        self.optimal_blueprint = None

        self.max_cost = None


    @cache
    def dfs(self, turn, resources, bots):
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
        # Step 0 - Initial Update of record and pruning

        # Global - With what we have, how many more geodes do we have to produce to beat the global
        # max? If it's past the theoretical limit (a blueprint with the lowest bot cost of each category), return 0

        # put in pruning conditions
        # Local - Were we able to get to this turn/geode/resource/bot combo locally in less time? Return 0
        print(bots, resources)

        if turn == 25:
            return resources[-1]

        # Step 1 - Produce
        resources = [x + y for x, y in zip(resources, bots)]


        # Step 2 - Try making each kind of bot and recurse. Return best geode production.
        best_production = 0
        could_produce = False

        # If we can make geode bots, we should
        if all(cost <= resource for cost, resource in zip(self.current_blueprint[3], resources)):
            could_produce = True
            tmp_resource = tuple([resource - cost for cost, resource in zip(self.current_blueprint[3], resources)])
            tmp_bots = list(bots)
            tmp_bots[3] += 1
            tmp_bots = tuple(tmp_bots)
            best_production = max(best_production, self.dfs(turn + 1, tmp_resource, tmp_bots))


        # Otherwise try scnearios producing each kind of bot, but only if we need more bots to meet our highest cost
        else:
            for idx, botcost in enumerate(self.current_blueprint):
                if all(cost <= resource for cost, resource in zip(botcost, resources)) and resources[idx] < self.max_cost[idx]:
                    could_produce = True
                    tmp_resource = tuple([resource - cost for cost, resource in zip(botcost, resources)])
                    tmp_bots = list(bots)
                    tmp_bots[idx] += 1
                    tmp_bots = tuple(tmp_bots)
                    best_production = max(best_production, self.dfs(turn + 1, tmp_resource, tmp_bots))

        if not could_produce:
            best_production = max(best_production, self.dfs(turn + 1, tuple(resources), bots))

        return best_production


# Test DFS
test = Solution()
resource = (0, 0, 0, 0)
bots = (1, 0, 0, 0)
test.current_blueprint = ((4, 0, 0, 0), (2, 0, 0, 0), (3, 14, 0, 0), (2, 0, 17, 0))
test.max_cost = (4, 14, 17, 0)
print(test.dfs(1, resource, bots))
