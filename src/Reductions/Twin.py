import numpy as np
from src.Utilities import check_fold, neighbours


def redu_twin(matrix: np.ndarray, V: np.ndarray, I: np.ndarray, folds: np.ndarray):
    for u in V:
        # search neighbours of u
        neigh_u, l1 = max_neighbours(matrix[u], V, 4)
        if l1 == 3:
            for v in V:     # V might change so iterating all of it is necessary
                if u != v:
                    neigh_v, l2 = max_neighbours(matrix[v], V, 4)
                    if l2 == 3 and np.array_equal(np.sort(neigh_u), np.sort(neigh_v)):    # N(u)=N(v)
                        if matrix[neigh_u[0], neigh_u[1]] == 1 or matrix[neigh_u[0], neigh_u[2]] == 1 or matrix[neigh_u[1], neigh_u[2]] == 1:  # if G[N(u)] has at least one edge
                            # add u and v to I (and delete them from V)
                            I, folds, V = check_fold(u, True, I, folds, V)
                            I, folds, V = check_fold(v, True, I, folds, V)
                            # delete N(u) and N(v) from V
                            for x in neigh_u:
                                I, folds, V = check_fold(x, False, I, folds, V)
                        else:   # G[N(u)] has no edges
                            # contract u, v, N(u), N(v) in w
                            # delete v, N(u), N(v) (u becomes w)
                            V = V[V != v]
                            for x in neigh_u:
                                V = V[V != x]
                            # save contraction information for future resolution
                            folds = np.append(folds, [[1, u, v, neigh_u[0], neigh_u[1], neigh_u[2]]], axis=0)
                            # update adjacency for contracted node (w)
                            matrix[u] = matrix[u] + matrix[neigh_u[0]] + matrix[neigh_u[1]] + matrix[neigh_u[2]]
                            matrix[u] = [min(x, 1) for x in matrix[u]]
                            matrix[u, u] = 0    # ensure edge (u, u) does not exists
                            # update adjacency for two-neighbours of u, now adjacent to w
                            neigh_nu = np.array(neighbours(matrix[neigh_u[0]], V), int)
                            neigh_nu = np.append(neigh_nu, neighbours(matrix[neigh_u[1]], V))
                            neigh_nu = np.append(neigh_nu, neighbours(matrix[neigh_u[2]], V))
                            # delete u from neighbours
                            indexes = np.where(neigh_nu == u)
                            neigh_nu = np.delete(neigh_nu, indexes)
                            for x in neigh_nu:
                                matrix[x, u] = 1
    return matrix, V, I, folds


def max_neighbours(adjacencies: np.ndarray, V: np.ndarray, max_length: int):
    """Stops if the amount of neighbours reaches max_length+1. Returns the neighbours found and their number"""
    neigh = np.array([], int)
    leng = 0
    for w in V:
        if adjacencies[w] == 1:
            neigh = np.append(neigh, w)
            leng += 1
        if leng >= max_length+1:
            break
    return neigh, leng
