import numpy as np
from src.Utilities import neighbours, check_fold
from src.Reductions.Diamond import redu_diamond


def redu_unconfined(matrix: np.ndarray, V: np.ndarray, I: np.ndarray, folds: np.ndarray):
    s_set = set()
    for v in V:
        # S = {v}
        s_set.add(v)
        unconf = False
        repeat = True
        while repeat:     # simulates do while
            # search N(S)
            neigh_s_open = set()
            for x in s_set:
                neigh_s_open.update(neighbours(matrix[x], V))
            temp_s = set()
            # check u ∈ N(S) such that |N(u) ∩ S| = 1
            for u in neigh_s_open:
                neigh_u_open = set()
                neigh_u_open.update(neighbours(matrix[u], V))
                if len(s_set.intersection(neigh_u_open)) == 1:
                    neigh_s_closed = neigh_s_open.union(s_set)
                    u_minus_s = neigh_u_open.difference(neigh_s_closed)
                    cardinality = len(u_minus_s)
                    if cardinality == 0:
                        unconf = True
                        repeat = False
                        break   # optimization
                    elif cardinality == 1:
                        temp_s.add(u_minus_s.pop())
                    neigh_s_closed.clear()
                    u_minus_s.clear()
            if unconf:  # v is unconfined
                I, folds, V = check_fold(v, False, I, folds, V)
                s_set.clear()
            elif repeat and len(temp_s) > 0:    # nature of v unclear
                s_set.update(temp_s)
            else:   # v is confined
                if len(s_set) >= 2:
                    V, I, folds = redu_diamond(matrix, v, neigh_s_open, V, I, folds)
                repeat = False
                s_set.clear()
    return matrix, V, I, folds
