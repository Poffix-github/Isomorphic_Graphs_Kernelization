import numpy as np
from src.Utilities import neighbours


def redu_vertex_folding(matrix: np.ndarray, V: np.ndarray, folds: np.ndarray):
    for v in V:
        # search for neighbours
        neigh_v = np.array([], int)
        leng = 0  # optimization: the search stops when 3 neighbours are found
        for w in V:
            if matrix[v, w] == 1:
                neigh_v = np.append(neigh_v, w)
                leng += 1
            if leng >= 3:
                break
        # Vertex Folding condition
        if leng == 2 and matrix[neigh_v[0], neigh_v[1]] == 0:
            # delete the two neighbours from V
            for u in neigh_v:
                V = V[V != u]
            # save contraction information for future resolution
            folds = np.append(folds, [[0, v, neigh_v[0], neigh_v[1], 0, 0]], axis=0)
            # update adjacency for contracted node
            matrix[v] = matrix[v] + matrix[neigh_v[0]] + matrix[neigh_v[1]]
            matrix[v] = [min(x, 1) for x in matrix[v]]
            matrix[v, v] = 0  # ensure edge (v, v) does not exists
            # update adjacency for two-neighbours of v, now adjacent to v'
            neigh_u1_u2 = np.array(neighbours(matrix[neigh_v[0]], V), int)
            neigh_u1_u2 = np.append(neigh_u1_u2, neighbours(matrix[neigh_v[1]], V))
            # delete v from neighbours
            indexes = np.where(neigh_u1_u2 == v)
            neigh_u1_u2 = np.delete(neigh_u1_u2, indexes)
            for u in neigh_u1_u2:
                matrix[u, v] = 1
    return matrix, V, folds
