
import sys
import heapq

def solve(module):
    """
    @param module: a module with certain required functions
    @return: a path from the initial state to a goal state, and the total distance
    """
    # get the initial state
    initial_state = module.get_initial_state()
    # if the initial state is a goal state then we are done
    if module.is_goal_state(initial_state):
        return [initial_state]
    # each heap element gives (total distance, distance to state, state, parent)
    pq = []
    initial_element = (module.get_hint(initial_state), 0, initial_state, None)
    heapq.heappush(pq, initial_element)
    # the dictionary maps a state to the best (distance to state, parent)
    d = {}
    d[initial_state] = (0, None)
    # no goal state has been found
    goal_state = None
    goal_distance = None
    # look for a good path
    while pq:
        d_total, d_to, state, parent = heapq.heappop(pq)
        # if this is a goal state then we are done
        if module.is_goal_state(state):
            reverse_path = []
            while state:
                reverse_path.append(state)
                cheese, state = d[state]
            return list(reversed(reverse_path)), d_total
        # add the child elements if they are appropriate
        for child, step_distance in module.gen_next_steps(state):
            # get the distance to this proposed node
            d_to_child = d_to + step_distance
            # if the child state has been pushed to the queue
            # with a distance at least as small
            # then skip it
            skip_flag = False
            known_result = d.get(child, None)
            if known_result:
                known_d_to_child, known_parent = known_result
                if known_d_to_child <= d_to_child:
                    skip_flag = True
            if not skip_flag:
                # add the element to the queue
                d_total_child = d_to_child + module.get_hint(child)
                element = (d_total_child, d_to_child, child, state)
                heapq.heappush(pq, element)
                # update the info about states that have been pushed to the queue
                info = (d_to_child, state)
                d[child] = info
    raise Exception('no path was found')

if __name__ == '__main__':
    if len(sys.argv) == 2:
        module_name = sys.argv[1]
        module = __import__(module_name)
        path, d_total = solve(module)
        print 'a path was found with length %d:' % d_total
        print
        state_strings = [module.get_state_string(state) for state in path]
        print '\n\n'.join(state_strings)
    else:
        print 'Usage: python %s <module-name>' % sys.argv[0]

