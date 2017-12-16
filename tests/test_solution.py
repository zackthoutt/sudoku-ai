"""This test suite includes a few basic test cases to verify your solution. However, passing these
tests does not guarantee that your solution is correct. The Project Asssistant test suite contains
many additional test cases that you must also pass to complete the project. You should write your
own additional test cases to cover any failed tests shown in the Project Assistant feedback.
"""
import unittest
from solver import SudokuSolver
from sudoku import Sudoku


# Examples of solvable Sudoku puzzles
#         |        |        |        |        |        |        |        |        |        |
grid_1 = '8..........36......7..9.2...5...7.......457.....1...3...1....68..85...1..9....4..'
grid_2 = '79...3..2.6.51.........2..6...8.1.4.......1.35...2...........74..1....65..8.97...'
grid_3 = '...34....6....1.4.7.4..51..8...6..15.2....4.75.......3...9.......7.53......41.52.'
grid_4 = '49.....8...3...........62..5...8..9.....4.61.6.1.2.5..256...3..1....2........78..'
grid_5 = '7...48....5.....24.....9..1.2.....5.3.9.5...6...47..3.....1..4.18....69.2..7.....'

# Examples of solvable Sudoku puzzles with special diagonal rules
diagonal_grid_1 = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'


class TestSudokuSolver(unittest.TestCase):

    def test_solve_puzzle_1(self):
        puzzle = Sudoku(grid_1)
        solver = SudokuSolver()
        solver.solve(puzzle, display_solution=False)
        self.assertTrue(puzzle.is_solved())

    def test_solve_puzzle_2(self):
        puzzle = Sudoku(grid_2)
        solver = SudokuSolver()
        solver.solve(puzzle, display_solution=False)
        self.assertTrue(puzzle.is_solved())

    def test_solve_puzzle_3(self):
        puzzle = Sudoku(grid_3)
        solver = SudokuSolver()
        solver.solve(puzzle, display_solution=False)
        self.assertTrue(puzzle.is_solved())

    def test_solve_puzzle_4(self):
        puzzle = Sudoku(grid_4)
        solver = SudokuSolver()
        solver.solve(puzzle, display_solution=False)
        self.assertTrue(puzzle.is_solved())

    def test_solve_puzzle_5(self):
        puzzle = Sudoku(grid_5)
        solver = SudokuSolver()
        solver.solve(puzzle, display_solution=False)
        self.assertTrue(puzzle.is_solved())

    def test_solve_puzzle_diagonal_1(self):
        puzzle = Sudoku(diagonal_grid_1, game_type='standard+diagonal')
        solver = SudokuSolver()
        solver.solve(puzzle, display_solution=False)
        self.assertTrue(puzzle.is_solved())


if __name__ == '__main__':
    unittest.main()
