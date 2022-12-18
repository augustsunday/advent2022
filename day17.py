# Name:         Colin Cummins
# Advent of Code 2022 - Day 17
# Pyroclastic flow
# Bit manipulation and cycle detection
class Turn:
    def __init__(self, turn_number: int, instruction_num: int, block_type: int, board: int, next):
        self.turn_number = turn_number
        self.instruction_num = instruction_num
        self.block_type = block_type
        self.board = board
        self.next = next

    def __eq__(self, other):
        return self.instruction_num == other.instruction_num and self.block_type == other.block_type and self.board == other.board

    def __repr__(self):
        return f"Turn: {self.turn_number}\nInstruction: {self.instruction_num}\nBlock Type: {self.block_type}\nBoard:\n{Volcano.render(None,self.board)}"


class Volcano:
    def __init__(self):
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

    def move_block(self, block_type: int, block_bits: int, direction: str, board: int) -> [int, bool]:
        """
        Gas jets push the block left or right, unless it will run into a wall. Then the block tries to drop.
        If the block can't drop, it comes to rest.
        :param block_type: Type of block
        :param block_bits: Code for actual block (bitshifted from original)
        :param direction:
        :return: (new block [int], status of block - True: Still falling, False - resting)
        """
        if direction == ">" and ((block_bits) % self.ROW_MOD) != self.BLOCK_RIGHT[block_type]:
            block_bits <<= 1

        if direction == "<" and ((block_bits) % self.ROW_MOD) != self.BLOCK_LEFT[block_type]:
            block_bits >>= 1

        if (block_bits << 7) & board == 0:
            block_bits <<= 7
            return block_bits, True

        return block_bits, False


test = Volcano()

# Drop test code
# for blocknum in range(5):
#     for direction in "<>":
#         my_board = test.setup_board(test.STARTING_SIGNATURE) << 49
#
#         test.render(my_board)
#
#         falling = True
#         my_block = test.BLOCK_ORDER[blocknum]
#         while falling:
#             print("Pre-push block mod: ", my_block % test.ROW_MOD)
#             test.render(my_block + my_board)
#             my_block, falling = test.move_block(blocknum, my_block, direction, my_board)
#         test.render(my_block + my_board)

for blocknum in range(5):
    my_board = test.setup_board(test.STARTING_SIGNATURE) << 49
    for direction in "<>":

        test.render(my_board)

        falling = True
        my_block = test.BLOCK_ORDER[blocknum]
        while falling:
            print("Pre-push block mod: ", my_block % test.ROW_MOD)
            test.render(my_block + my_board)
            my_block, falling = test.move_block(blocknum, my_block, direction, my_board)
        my_board = my_board + my_block
        test.render(my_board)
        print('Board height: ', my_board.bit_length() / 7)

# ====Test Code====

my_turn = Turn(27, 36, 3, test.STARTING_SIGNATURE, None)
other_turn = Turn(300, 36, 3, test.STARTING_SIGNATURE, None)
assert my_turn == other_turn
"Print: turn equality works"
print(my_turn)
"Print: Turn printing works"
