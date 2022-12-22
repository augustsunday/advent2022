# Author: Colin Cummins
# Github Username: augustsunday
# Date: 12/22/2022
# Description: Advent of Code 2022 - Day 20

from collections import deque

def mixing(nums: list[int]) -> list[int]:
    encrypted = queue(nums)
    to_do = nums
    for num in nums:
        encrypted.
