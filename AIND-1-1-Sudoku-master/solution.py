rows = 'ABCDEFGHI'
cols = '123456789'

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a+b for a in A for b in B]

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]

"Set up diagonals"
diagonal_1 = [[a[0]+a[1] for a in zip(rows,cols)]]
diagonal_2 = [[a[0]+a[1] for a in zip(rows,cols[::-1])]]
diagonal_units = diagonal_1 + diagonal_2

unitlist = row_units + column_units + square_units + diagonal_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args: values(dict): a dictionary of the form {'box_name': '123456789', ...}
    Returns: the values dictionary with the naked twins eliminated from peers.
    """   
    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
    # How to find the naked twins
   
    pre_naked_twins = [box for box in values.keys() if len(values[box]) == 2]
    for pre_naked_twin in pre_naked_twins:
        box_values = values[pre_naked_twin]
        same_peers = [peer for peer in peers[pre_naked_twins] if values[peer] == box_values]
        
        if len(same_peers) == 1:
            peers_pre   = peers[pre_naked_twins]
            peers_copy  = peers[same_peers[0]]
            naked_twins = [peer_copy for peer_copy in peers_copy if peer_copy in peers_pre]
            
            for naked_twin in naked_twins:
                if len(values[naked_twin]) > 1:
                    for value in box_values:
                        if value in values[naked_twin]:
                            values[box_value] = values[naked_twins].replace(digit,'')
                   
    return values
    
def grid_values(grid):
    values = []
    all_digits = '123456789'
    for c in grid:
        if c == '.':
              values.append(all_digits)
        elif c in all_digits:
              values.append(c)
    assert len(values) == 81                                  
    return dict(zip(boxes, values))
                                             
def display(values):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    """
    Go through all the boxes, and whenever there is a box with a value, eliminate this value from the values of all its peers.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'')
    return values

def only_choice(values):
    """
    Go through all the units, and whenever there is a unit with a value that only fits in one box, assign the value to this box.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values

def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    values = reduce_puzzle(values)
    if values is False:
        return False
    if all(len(values[s])== 1 for s in boxes):
        return values
    n,s = min((len(values[s]), s)for s in boxes if len(values[s]) >1)
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt                                          
     
    def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """

if __name__ == '__main__':
      for i in range(len(rows)):
    diagonal_units[0].append(rows[i] + cols[i])
    diagonal_units[1].append(rows[i] + cols[-1-i])                                                                     
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))
    solve(diag_sudoku_grid)                                     
    print('Finished!')
    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
