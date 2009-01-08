
g_use_big_steps = True

B_BIG = 0
B_SMALL = 1
B_WIDE = 2
B_TALL = 3

blocktype_to_dimension = {
    B_BIG: (2, 2),
    B_SMALL: (1, 1),
    B_WIDE: (1, 2),
    B_TALL: (2, 1)}

def gen_filled_locations(block):
    """
    @param block: something like (B_BIG, (3, 0))
    """
    # define the number of rows and columns
    # occupied by each block
    blocktype, upper_left = block
    row, col = upper_left
    dimension = blocktype_to_dimension[blocktype]
    blockrows, blockcols = dimension
    for drow in range(blockrows):
        for dcol in range(blockcols):
            yield (row + drow, col + dcol)

def flatten(substate):
    """
    @param substate: a set of some number of (type, location) pairs
    @return: a set of locations that are filled
    """
    all_filled_locations = set()
    for block in substate:
        all_filled_locations.update(gen_filled_locations(block))
    return all_filled_locations

def check_overlap(block, flattened_state):
    """
    @param block: a moved block that might be out of bounds
    @param flattened_state: a set of occupied squares
    @return: False if the block fails the check
    """
    return not (flattened_state & set(gen_filled_locations(block)))

def check_bounds(block):
    """
    @param block: a moved block that might be out of bounds
    @return: False if the block fails the check
    """
    for row, col in gen_filled_locations(block):
        if row < 0 or col < 0:
            return False
        if row > 4 or col > 3:
            return False
    return True

def gen_block_successors(substate, block, flattened_state):
    """
    Yield successor states from a state.
    @param state: a frozenset of nine (type, location) pairs
    """
    blocktype, (row, col) = block
    valid_moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    if g_use_big_steps:
        if blocktype == B_WIDE:
            valid_moves.extend([(0, 2), (0, -2)])
        elif blocktype == B_TALL:
            valid_moves.extend([(2, 0), (-2, 0)])
        elif blocktype == B_SMALL:
            if (row+1, col) not in flattened_state:
                valid_moves.extend([(2, 0), (1, -1), (1, 1)])
            if (row-1, col) not in flattened_state:
                valid_moves.extend([(-2, 0), (-1, -1), (-1, 1)])
            if (row, col+1) not in flattened_state:
                valid_moves.extend([(0, 2), (-1, 1), (1, 1)])
            if (row, col-1) not in flattened_state:
                valid_moves.extend([(0, -2), (-1, -1), (1, -1)])
    for drow, dcol in valid_moves:
        # move the block to the new location
        moved_block = (blocktype, (row + drow, col + dcol))
        if not check_bounds(moved_block):
            continue
        if not check_overlap(moved_block, flattened_state):
            continue
        # the move is valid so yield the new state
        new_state = frozenset(substate | set([moved_block]))
        yield new_state


# The following functions are required by the solver


def get_initial_state():
    initial_state = frozenset([
            (B_BIG, (0, 0)),
            (B_WIDE, (0, 2)),
            (B_WIDE, (1, 2)),
            (B_SMALL, (2, 0)),
            (B_SMALL, (2, 1)),
            (B_TALL, (3, 0)),
            (B_TALL, (3, 1)),
            (B_WIDE, (3, 2)),
            (B_WIDE, (4, 2))])
    return initial_state

def get_state_string(state):
    """
    @return: a multi-line string
    """
    # make a dictionary mapping location to ascii
    # that will be turned into a string
    blocktype_to_ascii = {
        B_SMALL: 'o',
        B_WIDE: '-',
        B_TALL: '|',
        B_BIG: '+'}
    d = {}
    for row in range(5):
        for col in range(4):
            location = (row, col)
            d[location] = '.'
    for block in state:
        blocktype, location = block
        for loc in gen_filled_locations(block):
            d[loc] = blocktype_to_ascii[blocktype]
    # turn the dictionary into a string
    rows = []
    for r in range(5):
        row = [d[(r, c)] for c in range(4)]
        rows.append(''.join(row))
    return '\n'.join(rows)

def is_goal_state(state):
    """
    @param state: a frozenset of nine (type, location) pairs
    """
    return (B_BIG, (3, 0)) in state

def gen_next_steps(state):
    """
    Yield successor states from a state.
    @param state: a frozenset of nine (type, location) pairs
    """
    step_distance = 1
    block_list = list(state)
    for i in range(9):
        substate = set(block_list[j] for j in range(9) if j != i)
        block = block_list[i]
        flattened_state = flatten(substate)
        for successor in gen_block_successors(substate, block, flattened_state):
            yield (successor, step_distance)

def get_hint(state):
    """
    @param: an admissible estimate of the remaining distance to a goal state
    """
    return 0
