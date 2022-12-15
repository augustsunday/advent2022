# Author: Colin Cummins
# Github Username: augustsunday
# Date: 12/15/2022
# Description: Beacon Exclusion Zone
from parse import *


def sweep_zone(sensor_x, sensor_y, beacon_x, beacon_y, row=None):
    # Returns the zone swept by a sensor to its nearest beacon
    # Returned as a list of tuple crosssections of the zone by row
    # Format (row_y, start_x, end_x)
    slices = []
    dist = abs(sensor_x - beacon_x) + abs(sensor_y - beacon_y)
    # y_delta = sensor_y - row
    # if y_delta > dist:
    #     return []
    # y_delta = abs(y_delta)
    # return [(row, sensor_x - (dist - y_delta), sensor_x + (dist - y_delta))y_delta]
    for i in range(dist):
        offset = (dist - i)
        interval = (sensor_y + i, sensor_x - offset, sensor_x + offset)
        if row is None or row == interval[0]:
            slices.append(interval)
        interval = (sensor_y - i, sensor_x - offset, sensor_x + offset)
        if row is None or row == interval[0]:
            slices.append(interval)

    return slices


def parse_input(filename):
    input = []
    with open(filename, "r") as fo:
        for line in fo.read().split("\n"):
            sensor_x, sensor_y, beacon_x, beacon_y = parse("Sensor at x={}, y={}: closest beacon is at x={}, y={}",
                                                           line)
            input.append([int(sensor_x), int(sensor_y), int(beacon_x), int(beacon_y)])

    return input


def get_intervals(filename, row = None):
    intervals = []
    input = parse_input(filename)
    for coords in input:
        intervals.extend(sweep_zone(*coords, row))

    return intervals


def merge_intervals(intervals):
    stack = []
    intervals.sort()
    for interval in intervals:
        if not stack or interval[1] > stack[-1][2]:
            stack.append(interval)
        else:
            old_row, old_start, old_end = stack.pop()
            stack.append((old_row, old_start, max(old_end, interval[2])))

    return (stack)


def prob1(filename, row):
    intervals = merge_intervals(get_intervals(filename, row))
    total_covered = sum(end - start for _, start, end in intervals)
    print(total_covered)


def prob2(filename):
    from collections import defaultdict
    row_dict = defaultdict(list)
    intervals = get_intervals(filename)
    for interval in intervals:
        row_dict[interval[0]].append(interval)
    for row in row_dict.values():
        if 0 <= row[0][0] <= 4000000:
            merged = merge_intervals(row)
            if len(merged) > 1:
                print("Distress Signal Located between intervals",merged)
                x, y = merged[0][2] + 1, merged[0][0]
                print("Coords: ", x, y)
                print("Tuning Frequency: ", x*4_000_000 +  y)



prob1("input.txt", 2000000)
prob2("input.txt")