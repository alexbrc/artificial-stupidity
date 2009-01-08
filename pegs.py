"""
The state is a tuple of sixteen boolean values.
"""

#: define a graphical template to help draw the image
g_template = """
....x....
...x.x...
..x.x.x..
.x.x.x.x.
x.x.x.x.x
"""

#: define half of the possible jumps
g_forward_triples = [
        (0, 2, 5),
        (2, 5, 9),
        (5, 9, 14),
        (1, 4, 8),
        (4, 8, 13),
        (3, 7, 12),
        (0, 1, 3),
        (1, 3, 6),
        (3, 6, 10),
        (2, 4, 7),
        (4, 7, 11),
        (5, 8, 12),
        (3, 4, 5),
        (6, 7, 8),
        (7, 8, 9),
        (10, 11, 12),
        (11, 12, 13),
        (12, 13, 14)]

#: by symmetry define the other half of the possible jumps
g_backward_triples = [tuple(reversed(triple)) for triple in g_forward_triples]


# The following functions are required by the solver


def get_initial_state():
    arr = [True]*15
    arr[4] = False
    return tuple(arr)

def get_state_string(state):
    """
    @return: a multi-line string
    """
    s = g_template.strip()
    arr = []
    i = 0
    for c_in in s:
        c_out = c_in
        if c_in == '.':
            c_out = ' '
        elif c_in == 'x':
            if state[i]:
                c_out = 'o'
            else:
                c_out = '.'
            i += 1
        arr.append(c_out)
    return ''.join(arr)

def is_goal_state(state):
    ntrue = sum(1 for v in state if v)
    return ntrue == 1

def gen_next_steps(state):
    """
    Yield successor states from a state.
    """
    step_distance = 1
    for a, b, c in g_forward_triples + g_backward_triples:
        if state[a] and state[b] and (not state[c]):
            next = list(state)
            next[a] = False
            next[b] = False
            next[c] = True
            yield (tuple(next), step_distance)

def get_hint(state):
    """
    @param: an admissible estimate of the remaining distance to a goal state
    """
    return 0

