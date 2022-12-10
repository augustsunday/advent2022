# Day 10 - Signal Strengths
def get_adders(filename: str) -> list[int]:
    """
    Returns an array of the amount to add to signal strength at the _start_ of the cycle
    :param filename:
    :return:
    """
    with open(filename, "r") as fo:
        adders = [0]
        for line in fo.readlines():
            instruction, *amount = line.split()
            adders.append(0)
            if amount:
                adders.append(int(amount[0]))
    return adders


def get_registers(adders):
    register = 1
    registers = []
    for idx, adder in enumerate(adders):
        register += adder
        registers.append(register)

    return registers


def get_signal_strengths(registers):
    strengths = []
    for cycle, register in enumerate(registers):
        strengths.append((cycle + 1) * register)
    return strengths


def filter_signal_strengths(strengths):
    # Take list of signal strengths and only return target strengths
    from itertools import count
    filtered = []
    target = 20
    while target < len(strengths):
        idx = target - 1
        filtered.append(strengths[idx])
        target += 40
    return filtered


def render(registers):
    row = []
    for idx, register in enumerate(registers):
        if idx % 40 == 0:
            print("")
        if abs(idx % 40 - register) <= 1:
            print("#", end="")
        else:
            print(" ", end="")


def prob1(filename: str) -> int:
    """
    Find the signal strength during the 20th, 60th, 100th, 140th, 180th, and 220th cycles.
    What is the sum of these six signal strengths?
    :param filename: input file
    :return: Sum of signal strengths at target cycles
    """
    print("Prob 1:")
    print(sum(filter_signal_strengths(get_signal_strengths(get_registers(get_adders(filename))))))
    print()


def prob2(filename: str) -> int:
    """
    Render image from registers
    """
    print("Prob 2:")
    render(get_registers(get_adders(filename)))


prob1("input.txt")
prob2("input.txt")
