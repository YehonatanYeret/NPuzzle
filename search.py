import state
import frontier


def search(s):
    print(s)
    f = frontier.create(s)
    while not frontier.is_empty(f):

        #print(s)
        s = frontier.remove(f)
        if state.is_target(s):
            print(s)
            return s
        ns = state.get_next(s)
        for i in ns:
            frontier.insert(f, i)
    return 0
