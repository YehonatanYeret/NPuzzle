import frontier
import state


def search(s):
    print(s)
    f = frontier.create(s)
    while not frontier.is_empty(f):
        print(s)
        s = frontier.remove(f)
        if state.is_target(s):
            return [s, f[1], f[3]]
        ns = state.get_next(s)
        for i in ns:
            frontier.insert(f, i)
    return 0
