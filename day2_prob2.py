# Author: Colin Cummins
# Github Username: augustsunday
# Date: 12/2/2022
# Description: Calculate winner of rock-paper-scissors tournament

def letter_to_score(letter: str) -> int:
    letter_dict = {"A": 1, "X": 1, "B": 2, "Y": 2, "C": 3, "Z": 3}
    return letter_dict[letter]


def match_score(choices) -> int:
    elf_choice, lose_draw_win = choices
    my_choice = (elf_choice + lose_draw_win) % 3 + 1
    score =(((my_choice % 3 - elf_choice % 3) + 4) % 3) * 3 + my_choice
    return score


def match_total(filename: str) -> list[tuple]:
    with open(filename, "r") as file_obj:
        matches = [tuple([letter_to_score(play) for play in match.split()]) for match in file_obj.read().splitlines()]

    return sum(map(match_score, matches))

print(match_total("input.txt"))
