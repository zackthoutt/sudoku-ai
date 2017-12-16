
from sudoku import *


row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diagonal_units = [
    [rows[position] + cols[position] for position in range(0, len(rows))],
    [rows[position] + cols[-(position + 1)] for position in range(0, len(rows))]
]
unitlist = row_units + column_units + square_units + diagonal_units

units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)


def naked_twins(values):
    """ Eliminate values using the naked twins strategy.
        Args:
            - values (dict): boxes map to their values strings (i.e. 'A1' => '135')
        Returns:
            - values (dict): the values dict with naked twins eliminated
    """
    for unit in unitlist:
        twin_values = find_twins(values, unit)
        values = eliminate_twin_values(values, unit, twin_values)
    return values


def eliminate_twin_values(values, unit, twin_values):
    """ Remove the twin values from a unit
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
                values = remove_digit(values, box, digit)
    return values


def find_twins(values, unit):
    """ Find the current twins for a unit (row, column, etc.)
        Args:
            - values (dict): boxes map to their values strings (i.e. 'A1' => '135')
            - unit (list): list of boxes in a unit
        Returns:
            - twin_values (list): the values that are length two and occur exactly twice in the unit
    """
    unit_values = [values[box] for box in unit]
    return [value for value in unit_values if unit_values.count(value) == 2 and len(value) == 2]


def remove_digit(values, box, digit):
    """ Remove a digit from the possible values of a box
        Args:
            - values (dict): boxes map to their values strings (i.e. 'A1' => '135')
            - box (str): the box to remove the digit from
            - digit (str): the digit to remove from the box
        Returns:
            - values (dict): updated values dict with the digit removed from the box
    """
    values[box] = values[box].replace(digit, '')
    return values


def eliminate(values):
    """Apply the eliminate strategy to a Sudoku puzzle

    The eliminate strategy says that if a box has a value assigned, then none
    of the peers of that box can have the same value.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the assigned values eliminated from peers
    """
    for box, value in values.items():
        if len(value) == 1:
            for peer in peers[box]:
                values = remove_digit(values, peer, value)
    return values


def only_choice(values):
    """Apply the only choice strategy to a Sudoku puzzle

    The only choice strategy says that if only one box in a unit allows a certain
    digit, then that box must be assigned that digit.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with all single-valued boxes assigned
    """
    for group in unitlist:
        for digit in '123456789':
            remainder = [box for box in group if digit in values[box]]
            if len(remainder) == 1:
                values[remainder[0]] = digit
    return values


def reduce_puzzle(values):
    """Reduce a Sudoku puzzle by repeatedly applying all constraint strategies

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary after continued application of the constraint strategies
        no longer produces any changes, or False if the puzzle is unsolvable
    """
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        values = eliminate(values)

        # Your code here: Use the Only Choice Strategy
        values = only_choice(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    """Apply depth first search to solve Sudoku puzzles in order to solve puzzles
    that cannot be solved by repeated reduction alone.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary with all boxes assigned or False
    """
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes):
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt


def solve(grid):
    """Find the solution to a Sudoku puzzle using search and constraint propagation

    Parameters
    ----------
    grid(string)
        a string representing a sudoku grid.

        Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    Returns
    -------
    dict or False
        The dictionary representation of the final sudoku grid or False if no solution exists.
    """
    values = grid2values(grid)
    values = search(values)
    return values

