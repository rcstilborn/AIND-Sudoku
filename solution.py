import logging
import collections

from utils import *

logging.basicConfig(level=logging.ERROR)


def eliminate(values):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after eliminating values.
    """
    for key, value in values.items():
        if len(value) == 1:
            for peer in peers[key]:
                assign_value(values,peer,values[peer].replace(value,""))
    return values


def naked_twins(values):
    """Eliminate values using the naked twins strategy.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
    for unit in unitlist:
        for loc in unit:
            if len(values[loc]) == 2: # only consider cells with two options in them
                for loc1 in unit:
                    if loc!=loc1 and values[loc] == values[loc1]: # Found twins
                        for loc2 in unit:
                            if len(values[loc2]) > 2: # Only consider cells in the unit with more than two possibilities
                                for c in values[loc1]: # Remove the twins from the cell
                                    assign_value(values, loc2, values[loc2].replace(c,""))
    return values

def naked_twins_new(values):
    """Eliminate values using the naked twins strategy.

    This was supposed to be a more optiomal version using list comprehensions instead of 
    nested for loops but some (limited testing) showed no improvement!
    Probably becuase the units are so small.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
    for unit in unitlist:
        # find all the two value locations
        pairs = [values[loc] for loc in unit if len(values[loc]) == 2]
        # Now find any twins
        twins = [item for item, count in collections.Counter(pairs).items() if count > 1]
        # find all the more than two value locations
        more_than_twos = [loc for loc in unit if len(values[loc]) > 2]

        # For each twin remove them from the locations with more than two options
        for twin in twins:
            for loc in more_than_twos:
                for c in twin: # Remove the twins from the cell
                    assign_value(values, loc, values[loc].replace(c,""))
    return values


def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    for unit in unitlist:
        for loc in unit:
            if len(values[loc]) > 1:
                possibles = values[loc]
                for loc1 in unit:
                    if loc!=loc1:
                        for c in values[loc1]:
                            possibles = possibles.replace(c,"")
                if len(possibles) == 1:
                    assign_value(values,loc,possibles)
    return values


def reduce_puzzle(values):
    """Apply the eliminate, only choice and naked twins constraints repeatedly until no further progress can be made

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after reduction or False if an error occurs
    """
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Use the Eliminate Strategy
        values = eliminate(values)
        # Use the Only Choice Strategy
        values = only_choice(values)
        # Use the Naked Twins
        values = naked_twins(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            logging.error('Something went wrong!')
            return False
    return values


def search(values):
    """ Use depth first search and propagation to find the solution

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after reduction or False if an error occurs
    """

    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False
    #display(values)
    
    # Check if we have a complate solution
    if len([box for box in values.keys() if len(values[box]) == 1]) == len(values):
        return values
    
    # Choose one of the unfilled squares with the fewest possibilities
    guesses = [(len(v),k) for k,v in values.items() if len(v) > 1]
    guesses.sort()
    
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for c in values[guesses[0][1]]:
        new_values = values.copy()
        new_values[guesses[0][1]] = c
        #print("Choosing", c, "for", guesses[0][1])
        new_values = search(new_values)
        if new_values:
            return new_values


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    return search(grid_values(grid))


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
