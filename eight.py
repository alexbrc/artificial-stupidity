"""
The state is a three by three matrix plus a redundant location for the blank.
"""

#: define the target matrix
g_target_matrix = (
        (1, 2, 3),
        (4, 5, 6),
        (7, 8, 0))

def get_row_string(row):
    arr = []
    for v in row:
        if v:
            arr.append('%d' % v)
        else:
            arr.append('.')
    return '.'.join(arr)

def get_target_location(v):
    for row_index, row in enumerate(g_target_matrix):
        for col_index, value in enumerate(row):
            if value == v:
                return (row_index, col_index)

#: cache the target location of each square
g_target_location = dict((v, get_target_location(v)) for v in range(1, 9))


# The following functions are required by the solver


def get_initial_state():
    """
    This initial state is arbitrary.
    """
    matrix = (
            (8, 7, 6),
            (5, 4, 3),
            (2, 1, 0))
    blank_location = (2, 2)
    return (matrix, blank_location)

def get_state_string(state):
    """
    @return: a multi-line string
    """
    matrix, location = state
    sep = '\n.....\n'
    return sep.join(get_row_string(row) for row in matrix)

def is_goal_state(state):
    matrix, location = state
    return matrix == g_target_matrix

def gen_next_steps(state):
    """
    Yield successor states from a state.
    """
    #print get_state_string(state)
    #print
    step_distance = 1
    matrix, (crow, ccol) = state
    offsets = ((0, -1), (0, 1), (-1, 0), (1, 0))
    for drow, dcol in offsets:
        nrow = drow + crow
        ncol = dcol + ccol
        if nrow < 0 or ncol < 0:
            continue
        if nrow > 2 or ncol > 2:
            continue
        m = [list(row) for row in matrix]
        m[crow][ccol] = m[nrow][ncol]
        m[nrow][ncol] = 0
        next_matrix = tuple(tuple(row) for row in m)
        next_location = (nrow, ncol)
        next_state = (next_matrix, next_location)
        yield (next_state, step_distance)

def get_hint(state):
    """
    @param: an admissible estimate of the remaining distance to a goal state
    """
    matrix, blank_location = state
    min_distance_to_goal = 0
    for row_index, row in enumerate(matrix):
        for col_index, v in enumerate(row):
            if v:
                target_row_index, target_col_index = g_target_location[v]
                min_distance_to_goal += abs(target_row_index - row_index)
                min_distance_to_goal += abs(target_col_index - col_index)
    return min_distance_to_goal

