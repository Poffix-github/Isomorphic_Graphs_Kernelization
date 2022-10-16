import numpy as np


def neighbours(adjacencies: np.ndarray, V: np.ndarray):
    """returns the open neighbourhood of the given row of an adjacency matrix"""
    return np.array([x for x in V if adjacencies[x] == 1], int)


def check_fold(node: int, mis: bool, ind, folds: np.ndarray, V: np.ndarray):
    """Call this function if a node is deleted, or it is added to the MIS.\n
    Checks if the node in question has been folded and applies the right propriety"""
    j = len(folds) - 1
    found = False
    while j >= 0 and not found:
        t, v, u, w, x, y = folds[j]
        if v == node:
            found = True
            folds = np.delete(folds, j, 0)
            if t == 0:
                # Vertex Folding
                if mis:
                    ind, folds, V = check_fold(v, False, ind, folds, V)
                    ind, folds, V = check_fold(u, True, ind, folds, V)
                    ind, folds, V = check_fold(w, True, ind, folds, V)
                    ind = np.append(ind, (u, w))
                else:
                    ind, folds, V = check_fold(v, True, ind, folds, V)
                    ind, folds, V = check_fold(u, False, ind, folds, V)
                    ind, folds, V = check_fold(w, False, ind, folds, V)
                    ind = np.append(ind, v)
            else:
                # Twin
                if mis:
                    ind, folds, V = check_fold(v, False, ind, folds, V)
                    ind, folds, V = check_fold(u, False, ind, folds, V)
                    ind, folds, V = check_fold(w, True, ind, folds, V)
                    ind, folds, V = check_fold(x, True, ind, folds, V)
                    ind, folds, V = check_fold(y, True, ind, folds, V)
                    ind = np.append(ind, [w, x, y])
                else:
                    ind, folds, V = check_fold(v, True, ind, folds, V)
                    ind, folds, V = check_fold(u, True, ind, folds, V)
                    ind, folds, V = check_fold(w, False, ind, folds, V)
                    ind, folds, V = check_fold(x, False, ind, folds, V)
                    ind, folds, V = check_fold(y, False, ind, folds, V)
                    ind = np.append(ind, [v, u])
        else:
            j -= 1
    if not found and mis:
        ind = np.append(ind, node)
    V = V[V != node]
    return ind, folds, V

def deg(row: np.ndarray):
    d = 0
    for i in row:
        d += i
    return d

# TODO: cancella
def max_neighbours(adjacencies: np.ndarray, V: np.ndarray, max_length: int):
    """The search stops when max_length+1 neighbours are found.\n
    Returns neighbours if they are less or equal to max_length, returns None otherwise."""
    neigh_v = np.array([], int)
    leng = 0
    for w in V:
        if adjacencies[w] == 1:
            neigh_v = np.append(neigh_v, w)
            leng += 1
        if leng >= max_length:
            break
    return neigh_v if leng <= max_length else None
