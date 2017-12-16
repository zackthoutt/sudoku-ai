from sudoku import Sudoku


class SudokuSolver():
    """Class that solves sudoku puzzles"""
    rows = 'ABCDEFGHI'
    cols = '123456789'

    def configure_solver(self, game_type):
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

    def naked_twins(self, values):
        """ Eliminate values using the naked twins strategy.

            Args:
                - values (dict): boxes map to their values strings (i.e. 'A1' => '135')
            Returns:
                - values (dict): the values dict with naked twins eliminated
        """
        for unit in self.unitlist:
            twin_values = self.find_twins(values, unit)
            values = self.eliminate_twin_values(values, unit, twin_values)
        return values

    def eliminate_twin_values(self, values, unit, twin_values):
        """ Remove the twin values from a unit.

            Args:
                - values (dict): boxes map to their values strings (i.e. 'A1' => '135')
                - unit (list): list of boxes in a unit
                - twin_values (list): list of twin values to eliminate from unit
            Returns:
                - values (dict): updated values dict with twins eliminated from the unit
        """
        for box in unit:
            if values[box] in twin_values:
                continue
            for twin in twin_values:
                for digit in twin:
                    values = self.remove_digit(values, box, digit)
        return values

    def find_twins(self, values, unit):
        """ Find the current twins for a unit (row, column, etc.).

            Args:
                - values (dict): boxes map to their values strings (i.e. 'A1' => '135')
                - unit (list): list of boxes in a unit
            Returns:
                - twin_values (list): the values that are length two and occur exactly twice in the unit
        """
        unit_values = [values[box] for box in unit]
        return [value for value in unit_values if unit_values.count(value) == 2 and len(value) == 2]

    @staticmethod
    def remove_digit(values, box, digit):
        """ Remove a digit from the possible values of a box.

            Args:
                - values (dict): boxes map to their values strings (i.e. 'A1' => '135')
                - box (str): the box to remove the digit from
                - digit (str): the digit to remove from the box
            Returns:
                - values (dict): updated values dict with the digit removed from the box
        """
        values[box] = values[box].replace(digit, '')
        return values


    def eliminate(self, values):
        """ Apply the eliminate strategy to a Sudoku puzzle.

            The eliminate strategy says that if a box has a value assigned, then none
            of the peers of that box can have the same value.

            Args:
                - values (dict): boxes map to their values strings (i.e. 'A1' => '135')
            Returns:
                - values (dict): the values dict with solved values eliminated from peers
        """
        for box, value in values.items():
            if len(value) == 1:
                for peer in self.peers[box]:
                    values = self.remove_digit(values, peer, value)
        return values


    def only_choice(self, values):
        """ Apply the only choice strategy to a Sudoku puzzle.

            The only choice strategy says that if only one box in a unit allows a certain
            digit, then that box must be assigned that digit.

            Args:
                - values (dict): boxes map to their values strings (i.e. 'A1' => '135')
            Returns:
                - values (dict): the values dict with only choice values solved
        """
        for group in self.unitlist:
            for digit in '123456789':
                remainder = [box for box in group if digit in values[box]]
                if len(remainder) == 1:
                    values[remainder[0]] = digit
        return values


    def reduce_puzzle(self, values):
        """ Reduce a Sudoku puzzle by repeatedly applying all constraint strategies.

            Args:
                - values (dict): boxes map to their values strings (i.e. 'A1' => '135')
            Returns:
                - values (dict/False): The values dictionary after continued application of
                  the constraint strategies no longer produces any changes, or False if the
                  puzzle is unsolvable
        """
        stalled = False
        while not stalled:
            solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

            values = self.eliminate(values)

            values = self.naked_twins(values)

            values = self.only_choice(values)

            # Check how many boxes have a determined value, to compare
            solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
            # If no new values were added, stop the loop.
            stalled = solved_values_before == solved_values_after
            # Sanity check, return False if there is a box with zero available values:
            if len([box for box in values.keys() if len(values[box]) == 0]):
                return False
        return values

    def search(self, values):
        """ Apply depth first search to solve Sudoku puzzles in order to solve puzzles
            that cannot be solved by repeated reduction alone.

            Args:
                - values (dict): boxes map to their values strings (i.e. 'A1' => '135')
            Returns:
                - values (dict/False): The values dictionary after continued application of
                  the constraint strategies no longer produces any changes, or False if the
                  puzzle is unsolvable
        """
        values = self.reduce_puzzle(values)
        if values is False:
            return False ## Failed earlier
        if all(len(values[s]) == 1 for s in self.boxes):
            return values ## Solved!
        # Choose one of the unfilled squares with the fewest possibilities
        n,s = min((len(values[s]), s) for s in self.boxes if len(values[s]) > 1)
        # Now use recurrence to solve each one of the resulting sudokus, and
        for value in values[s]:
            new_sudoku = values.copy()
            new_sudoku[s] = value
            attempt = self.search(new_sudoku)
            if attempt:
                return attempt

    def solve(self, puzzle, display_solution=True):
        """Find the solution to a Sudoku puzzle using search and constraint propagation.

            Args:
                - puzzle (obj): an instance of a Sudoku
                - display_solution (boolean): whether or not to print the solution to sdout
        """
        if not isinstance(puzzle, Sudoku):
            raise Exception("The puzzle needs to be an instance of Sudoku")

        self.configure_solver(puzzle.game_type)
        puzzle.values = self.search(puzzle.values)

        if puzzle.is_solved():
            print("The puzzle was solved!")
            if display_solution:
                puzzle.display()


puzzle = Sudoku('2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3', game_type='standard+diagonal')
puzzle.display()
solver = SudokuSolver()
solver.solve(puzzle)


