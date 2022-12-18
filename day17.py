# Name:         Colin Cummins
# Advent of Code 2022 - Day 17
# Pyroclastic flow
# Bit manipulation and cycle detection

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
        print(s)
        s = s[::-1]
        print(s)
        for i in range(0, len(s), 7):
            print("|" + s[i:i + 7].ljust(7, "0").replace("0", ".").replace("1", "#") + "|")

    def setup_board(self, signature: int, block: int) -> int:
        """
        Sets up board for a new round.
        All params are binary integer representations of board elements
        :param signature: Signature to populate the signature area [int]
        :param block: Block to stage in staging area
        :return: Binary representation of full board. Block in block area, 3 empty lines, then the signature
        """
        return signature + (block << 49)

    def move_block(self, block: int, direction: str) -> [int, bool] :
        """
        Gas jets push the block left or right, unless it will run into a wall. Then the block tries to drop.
        If the block can't drop, it comes to rest.
        :param block:
        :param direction:
        :return: Binary representation of new block, boolean if block has come to rest
        """
        pass






test = Volcano()
# test.render((test.BLOCK - test.FULL_STAGING))
# test.render((test.ELL - test.FULL_STAGING))
# test.render(test.board)
# test.render(test.STARTING_SIGNATURE)
# test.render(test.setup_board(test.STARTING_SIGNATURE, test.HORIZONTAL_4))

vert = test.VERTICAL_4 << 5
for i in range(10):
    print(i)
    print(vert >> i)
    print((vert >> i) % (2**7 -1))
    test.render(vert >> i)

test.render(test.setup_board(test.VERTICAL_4, test.STARTING_SIGNATURE))