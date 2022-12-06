# Author: Colin Cummins
# Github Username: augustsunday
# Date: 12/6/2022
# Description: Find first subsequence of 4 unique characters

def find_marker(sequence: str, marker_len: int) -> int:
    """
    Find first occurence of 'marker' of specified length - the marker is a sequence of unique characters
    :param sequence: Full message sequence [str]
    :param marker_len: Length of marker to search for
    :return: Index of marker end
    """
    from collections import defaultdict
    freq = defaultdict(int)
    for signal in sequence[:marker_len]:
        freq[signal] += 1
    head = marker_len

    while head < len(sequence):
        if max(freq.values()) == 1:
            return head
        freq[sequence[head - marker_len]] -= 1
        freq[sequence[head]] += 1
        head += 1

with open("input.txt", "r") as file_obj:
    print("Part 1: ", find_marker(file_obj.read(), 4))
with open("input.txt", "r") as file_obj:
    print("Part 2: ", find_marker(file_obj.read(), 14))

