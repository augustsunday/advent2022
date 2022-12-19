# Name:         Colin Cummins
# Advent of Code 2022 - Day 17
# Pyroclastic flow
# Bit manipulation and cycle detection
from itertools import cycle
from functools import cache
from math import ceil


class Turn:
    def __init__(self, turn_number: int, instruction_num: int, block_type: int, board: int, height: int, next):
        self.turn_number = turn_number
        self.instruction_num = instruction_num
        self.block_type = block_type
        self.board = board
        self.height = height
        self.next = next

    def __eq__(self, other):
        return self.instruction_num == other.instruction_num and self.block_type == other.block_type and self.board == other.board

    def __repr__(self):
        return f"Turn: {self.turn_number}\nInstruction: {self.instruction_num}\nBlock Type: {self.block_type}\nBoard" \
               f":\nCurrent Height:{self.height}{Volcano.render(None, self.board)} "


class Volcano:
    def __init__(self, filename: str):
        self.HORIZONTAL_4 = 125829120
        self.PLUS_SIGN = 17236992
        self.ELL = 58984448
        self.VERTICAL_4 = 8454660
        self.BLOCK_4 = 25362432
        self.FULL_STAGING = 2 ** 28 - 1
        self.STARTING_SIGNATURE = 2 ** 7 - 1
        self.BLOCK_ORDER = [self.HORIZONTAL_4, self.PLUS_SIGN, self.ELL, self.VERTICAL_4, self.BLOCK_4]
        self.ROW_MOD = 2 ** 7 - 1
        self.BLOCK_LEFT = [15, 11, 15, 4, 6]
        self.BLOCK_RIGHT = [120, 49, 113, 2, 65]

        with open(filename, "r") as fo:
            self.INSTRUCTION_SEQ = fo.read().strip("\n")

        self.INSTRUCTION_ITER = cycle(range(len(self.INSTRUCTION_SEQ)))
        self.BLOCK_ITER = cycle(range(len(self.BLOCK_ORDER)))

    def test_pattern(self):
        print("Horizontal 4:")
        self.render(self.HORIZONTAL_4)
        print("Plus:")
        self.render(self.PLUS_SIGN)
        print("Ell:")
        self.render(self.ELL)
        print("Vertical 4:")
        self.render(self.VERTICAL_4)
        print("Block:")
        self.render(self.BLOCK)
        print("Full Staging:")
        self.render(self.FULL_STAGING)

    def render(self, s: int) -> None:
        """
        Render a bit representation in user-readable format
        :param s: Integer representation. Scanning left to right, down every 7 columns. 1 for occupied, 0 for empty.
        :return: None - Renders graphical representation of bitmap to screen
        """
        s = format(s, 'b').strip("-")
        s = s[::-1]
        print("|+++++++|")
        for i in range(0, len(s), 7):
            print("|" + s[i:i + 7].ljust(7, "0").replace("0", ".").replace("1", "#") + "|")
        print("\n")

    def setup_board(self, profile) -> int:
        """
        Sets up board for a new round.
        All params are binary integer representations of board elements
        :param profile: Profile to populate the signature area [int]
        :param block: Block to stage in staging area
        :return: Binary representation of full board. Block in block area, 3 empty lines, then the signature
        """
        return (profile << 49) + (test.STARTING_SIGNATURE << 56)

    def move_block(self, block_type: int, block_bits: int, direction: str, board: int, debug=None) -> [int, bool]:
        """
        Gas jets push the block left or right, unless it will run into a wall. Then the block tries to drop.
        If the block can't drop, it comes to rest.
        :param block_type: Type of block
        :param block_bits: Code for actual block (bitshifted from original)
        :param direction:
        :return: (new block [int], status of block - True: Still falling, False - resting)
        """
        if direction == ">" and ((block_bits % self.ROW_MOD) != self.BLOCK_RIGHT[block_type]) and (
                (block_bits << 1) & board == 0):
            block_bits <<= 1
            if debug:
                self.render(board + block_bits)

        if direction == "<" and ((block_bits % self.ROW_MOD) != self.BLOCK_LEFT[block_type]) and (
                (block_bits >> 1) & board == 0):
            block_bits >>= 1
            if debug:
                self.render(board + block_bits)

        if (block_bits << 7) & board == 0:
            block_bits <<= 7
            if debug:
                self.render(board + block_bits)
            return block_bits, True

        return block_bits, False

    @cache
    def simplify_board(self, board: int) -> int:
        """
        Takes a board and simplifies it by reducing it to the 'shadow' of every possible space the
        :param board:
        :return:
        """
        shadow = 0
        stack = []
        seen = set()
        for block_type in range(5):
            block_bits = self.BLOCK_ORDER[block_type]
            stack.append((block_bits, ">"))
            stack.append((block_bits, "<"))
            while stack:
                block_bits, direction = stack.pop()
                if (block_bits, direction) not in seen:
                    seen.add((block_bits, direction))
                    if direction == ">" and ((block_bits % self.ROW_MOD) != self.BLOCK_RIGHT[block_type]) and (
                            (block_bits << 1) & board == 0):
                        block_bits <<= 1
                        shadow |= block_bits

                    if direction == "<" and ((block_bits % self.ROW_MOD) != self.BLOCK_LEFT[block_type]) and (
                            (block_bits >> 1) & board == 0):
                        block_bits >>= 1
                        shadow |= block_bits

                    if (block_bits << 7) & board == 0:
                        block_bits <<= 7
                        shadow |= block_bits
                        stack.append((block_bits, ">"))
                        stack.append((block_bits, "<"))

        # Chop off top two rows which have artifacts d/t starting positions of shapes
        shadow = shadow >> 14

        # Convert to board format
        length = shadow.bit_length()
        length = length if length % 7 == 0 else length + 7 - length % 7
        mask = 2 ** length - 1
        shadow = shadow ^ mask
        while shadow & self.ROW_MOD == 0:
            shadow >>= 7

        floor_row = ceil(shadow.bit_length() / 7)
        shadow += self.STARTING_SIGNATURE << (7 * floor_row)

        # Push down to make space for staging area and drop region
        shadow = shadow << 49

        return shadow

    def take_turn(self, board: int):
        """
        Takes a board and drops a block until it lands (according to current state of class instruction and block status)
        Returns turn object containing new board, height gained
        :param board:
        :return:
        """
        current_block_num = next(self.BLOCK_ITER)
        current_block = self.BLOCK_ORDER[current_block_num]
        falling = True
        while falling:
            current_instruction = self.INSTRUCTION_SEQ[next(self.INSTRUCTION_ITER)]
            current_block, falling = self.move_block(current_block_num, current_block, current_instruction, board)
        board = board + current_block

        # Get height_adder
        height_adder = 7
        while board & self.ROW_MOD == 0:
            board >>= 7
            height_adder -= 1

        # Push board back to make room for next block to fall
        board <<= 49

        # reduce board to its simplest form
        board = self.simplify_board(board)

        return board, height_adder


tortoise = Volcano("input.txt")
tortoise_board = (tortoise.STARTING_SIGNATURE << 56) + (tortoise.STARTING_SIGNATURE << 49)
tortoise_height = 0

hare = Volcano("input.txt")
hare_board = (hare.STARTING_SIGNATURE << 56) + (hare.STARTING_SIGNATURE << 49)
hare_height = 0
hare_board, adder = hare.take_turn(hare_board)
hare_height += adder

turn = 0


for i in range(3420):
    if tortoise_board == hare_board:
        print("Board match at turn:", turn)
        print("Tortoise Height", tortoise_height)
        print("Height Differential", hare_height - tortoise_height)
        print("Turn Differential", i)
        print()
    tortoise_board, height_adder = tortoise.take_turn(tortoise_board)
    tortoise_height += height_adder

    hare_board, adder = hare.take_turn(hare_board)
    hare_height += adder
    hare_board, adder = hare.take_turn(hare_board)
    hare_height += adder


    turn += 1


turn = 3419


