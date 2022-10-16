import numpy as np
from src.Utilities import neighbours, check_fold


def redu_diamond(a_matrix: np.ndarray, v: int, neigh_s: set, V: np.ndarray, I:np.ndarray, folds: np.ndarray):
    delete = False
    all_neigh = np.empty(0, set)
    i = 0
    dim = len(neigh_s)
    while i < dim and not delete:
        j = i+1
        if i == 0:  # first passage search for neighbours
            all_neigh = np.append(all_neigh, set(neighbours(a_matrix[i], V)).difference(neigh_s))
        while j < dim and not delete:
            if i == 0:  # first passage search for neighbours
                all_neigh = np.append(all_neigh, set(neighbours(a_matrix[j], V)).difference(neigh_s))
            # check condition N(u_1)\N(S) = N(u_2)\N(S) = [v_1, v_2]
            if all_neigh[i] == all_neigh[j] and len(all_neigh[i]) == 2:
                I, folds, V = check_fold(v, False, I, folds, V)
                delete = True
            j += 1
        i += 1
    return V, I, folds
