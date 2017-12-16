class Sudoku():
    """A sudoku puzzle"""
    rows = 'ABCDEFGHI'
    cols = '123456789'

    def __init__(self, initial_grid, game_type='standard'):
        """ Initialize the Sudoku puzzle.

            Args:
                - initial_grid (str): string representing the sudoku grid
                  Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
                - game_type (str): the type of game to define rules
                    Choices:
                        1. 'standard': use the normal rules of 1-9 appearing exactly once in each row, col, and square
                        2. 'standard+diagonal': use the 'standard' rules above and also require 1-9 to appear exactly once in each diagonal
        """
        self.build_puzzle(game_type)
        self.game_type = game_type
        self.initial_grid = initial_grid
        self.grid = initial_grid
        self.values = self.grid_to_values(initial_grid)

    def build_puzzle(self, game_type):
        """ Build helpful attributes about the sudoku puzzle for a given type of rules.

            Args:
                - game_type (str): the type of game to define rules
        """
        self.boxes = [r + c for r in self.rows for c in self.cols]
        self.row_units = [self.cross(r, self.cols) for r in self.rows]
        self.column_units = [self.cross(self.rows, c) for c in self.cols]
        self.square_units = [self.cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
        self.diagonal_units = []
        self.unitlist = self.row_units + self.column_units + self.square_units

        if game_type == 'standard+diagonal':
            self.diagonal_units = [
                [self.rows[position] + self.cols[position] for position in range(0, len(self.rows))],
                [self.rows[position] + self.cols[-(position + 1)] for position in range(0, len(self.rows))]
            ]
            self.unitlist += self.diagonal_units

        self.units = dict((s, [u for u in self.unitlist if s in u]) for s in self.boxes)
        self.peers = dict((s, set(sum(self.units[s],[]))-set([s])) for s in self.boxes)

    @staticmethod
    def cross(A, B):
        """Cross product of elements in A and elements in B """
        return [x+y for x in A for y in B]

    def values_to_grid(self, values=None):
        """ Convert the dictionary board representation to as string.

            Args:
                - values (dict): boxes map to their values strings (i.e. 'A1' => '135')
            Returns:
                - grid (str): string representing the sudoku grid
                  Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
        """
        if values is None:
            values = self.values

        res = []
        for r in self.rows:
            for c in self.cols:
                v = values[r + c]
                res.append(v if len(v) == 1 else '.')
        return ''.join(res)

    def grid_to_values(self, grid=None):
        """ Convert grid into a dict of {square: char} with '123456789' for empties.

            Args:
                - grid (str): string representing the sudoku grid
                  Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
            Returns:
                - values (dict): boxes map to their values strings (i.e. 'A1' => '135')
                                 Empty values will be set to '123456789'
        """
        if grid is None:
            grid = self.grid

        sudoku_grid = {}
        for val, key in zip(grid, self.boxes):
            if val == '.':
                sudoku_grid[key] = '123456789'
            else:
                sudoku_grid[key] = val
        return sudoku_grid

    def remove_digit(self, box, digit):
        """ Remove a digit from the possible values of a box.

            Args:
                - box (str): the box to remove the digit from
                - digit (str): the digit to remove from the box
            Returns:
                - values (dict): updated values dict with the digit removed from the box
        """
        self.values[box] = self.values[box].replace(digit, '')

    def display(self, values=None):
        """ Display the values as a 2-D grid.

            Args:
                - values (dict): boxes map to their values strings (i.e. 'A1' => '135')
        """
        if values is None:
            values = self.values

        width = 1+max(len(values[s]) for s in self.boxes)
        line = '+'.join(['-'*(width*3)]*3)
        for r in self.rows:
            print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                          for c in self.cols))
            if r in 'CF': print(line)
        print()

    def is_solved(self):
        """ Determine if the puzzle has been solved.

            Returns:
                - solved (boolean): whether or not the puzzle is solved
        """
        fully_reduced = all(len(self.values[s]) == 1 for s in self.boxes)
        if not fully_reduced:
            return False

