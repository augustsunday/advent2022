# Advent of Code 2022 - Day 19 - Not Enough Minerals
from collections import deque
from functools import cache

class Blueprint():
    def __init__(self, cost_matrix):
        self.triangular = [n * (n + 1) //2 for n in range(26)]
        self.costs = cost_matrix

    def get_triangular(self, num):
        # returns n where n is the side length of the first triangular number greater than or equal to num
        i = 0
        while self.triangular[i] < num:
            i += 1
        return i



    # @todo Convert to stack-based dfs, with visited cache stored in the object, and a priority queue that favors solutions closer to goal
    def can_reduce(self, turns_remaining, resources, bots):
        """
        Can this blueprint reduce 'goal' geodes down to 1 ore-bot and 0 resources in time?
        :param goal:
        :return:
        """
        # Base cases - We've hit our target of no resources and one ore-bot
        # or we're out of time
        if all(x <= 0 for x in resources) and all(x <=0 for x in bots[1:]) and bots[0] >= 1:
            return True

        if turns_remaining == -1:
            return False

        # By necessity we must have at least enough bots to consume all the resources in time
        # So say we actually had more bots!
        # Look at the nth triangular number greater than or equal to each resource. We need at least n bots this turn to
        # reduce that resource to zero in time
        print(turns_remaining, resources, bots)

        resources, bots = list(resources), list(bots)

        for i in range(len(bots)):
            bots[i] = max(bots[i], self.get_triangular(resources[i]))



        # No way we can produce this many bots by this point
        if sum(bots) > self.triangular[turns_remaining]:
            return False

        # (Optional) No way we can consume this many resources by this point
        # @todo tighten this up
        max_consumption_threshold = max([sum(bot_cost) for bot_cost in self.costs]) * turns_remaining
        if sum(resources) > max_consumption_threshold:
            return False

        # @todo some threshhold for negative bots?

        # Try unproducing each kind of bot...
        for idx, cost in enumerate(self.costs):
            temp_resources, temp_bots = resources[:], bots[:]
            temp_bots[idx] -= 1
            temp_resources = [x + y for x, y in zip(temp_resources, cost)]
            temp_resources = [x - y for x, y in zip(temp_resources, temp_bots)]
            if self.can_reduce(turns_remaining - 1, tuple(temp_resources), tuple(temp_bots)):
                return True

        # try without any bot unbuilding
        temp_resources, temp_bots = resources[:], bots[:]
        temp_resources = [x - y for x, y in zip(temp_resources, temp_bots)]
        return self.can_reduce(turns_remaining - 1, tuple(temp_resources), tuple(temp_bots))

specs = ((4, 0, 0, 0), (2, 0, 0, 0), (3, 14, 0, 0), (2, 0, 7, 0))
start_bots = (1, 0, 0, 0)
start_resources = (0, 0, 0, 1)
test_print = Blueprint(specs)
print(test_print.can_reduce(25, start_resources, start_bots))
