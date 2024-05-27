import state


# implements a priority queue
# [list of states, total num of states, curr. num. of states, max. num. of states]
def create(s):
    return [[s], 0, 0, 0]


def is_empty(f):
    return f[0] == []


def val(s):
    return state.h_distance(s) + state.path_len(s)


# Uniform Cost: return state.path_len(s)
# Greedy Best First: return state.h_distance(s)

def insert(h, s):
    # inserts state s to the frontier
    f = h[0]
    h[1] += 1
    h[2] += 1
    if h[2] > h[3]:
        h[3] = h[2]
    f.append(s)
    i = len(f) - 1
    while i > 0 and val(f[i]) < val(f[(i - 1) // 2]):
        t = f[i]
        f[i] = f[(i - 1) // 2]
        f[(i - 1) // 2] = t
        i = (i - 1) // 2


def remove(h):
    if is_empty(h):
        return 0
    h[2] -= 1
    f = h[0]
    s = f[0]
    f[0] = f[len(f) - 1]
    del f[-1]
    heapify(f, 0)
    return s


def heapify(f, i):
    min_son = i
    if 2 * i + 1 < len(f) and val(f[2 * i + 1]) < val(f[min_son]):
        min_son = 2 * i + 1
    if 2 * i + 2 < len(f) and val(f[2 * i + 2]) < val(f[min_son]):
        min_son = 2 * i + 2
    if min_son != i:
        t = f[min_son]
        f[min_son] = f[i]
        f[i] = t
        heapify(f, min_son)
