import numpy as np
from src.Utilities import neighbours, check_fold


def redu_linear_time(matrix: np.ndarray, V: np.ndarray, ind: np.ndarray, folds: np.ndarray):
    original_V = V.copy()
    ind, V1, V2, V3, degree, folds, V = initialization(matrix, V, ind, folds)
    S = list()  # used as a stack
    c1 = len(V1)
    c2 = len(V2)
    while c1 != 0 or c2 != 0 or len(V3) != 0:
        if c1 != 0:
            V, ind, folds = degree_one_redu(matrix, V, V1, degree, ind, V2, V3, folds)
        elif c2 != 0:
            V, matrix, ind, folds = degree_two_path_redu(V2, S, matrix, V, degree, ind, V1, V3, folds)
        else:
            V, ind, folds = inexact_redu(degree, V3, V, matrix, ind, V1, V2, folds)
        c1 = len(V1)
        c2 = len(V2)

    while len(S) != 0:
        u = S.pop()
        insert = True
        if len(neighbours(matrix[u], ind)) > 0:
            insert = False
        if insert:
            # ind = np.append(ind, u)
            ind, folds, V = check_fold(u, True, ind, folds, V)

    for node in ind:
        original_V = original_V[original_V != node]
        neigh = neighbours(matrix[node], original_V)
        for n in neigh:
            original_V = original_V[original_V != n]

    return matrix, original_V, ind, folds


def initialization(matrix: np.ndarray, V: np.ndarray, ind, folds: np.ndarray):
    V1 = set()
    V2 = set()
    V3 = set()
    degree = {}
    for n in V:
        d = len(neighbours(matrix[n], V))
        degree[n] = d
        if d == 0:
            ind, folds, V = check_fold(n, True, ind, folds, V)
        elif d == 1:
            V1.add(n)
        elif d == 2:
            V2.add(n)
        else:
            V3.add(n)
    return ind, V1, V2, V3, degree, folds, V


def degree_one_redu(matrix: np.ndarray, V: np.ndarray, V1: set, degree: dict, ind, V2: set, V3: set, folds: np.ndarray):
    u = V1.pop()
    V1.add(u)
    q = neighbours(matrix[u], V)
    V, ind, folds = delete_vertex(q[0], V, matrix, degree, ind, V1, V2, V3, folds)
    return V, ind, folds


def degree_two_path_redu(V2: set, S: list, matrix: np.ndarray, V: np.ndarray, degree: dict, ind, V1: set, V3: set, folds: np.ndarray):
    u = V2.pop()
    V2.add(u)
    edges = list()
    P, cycle = find_path(u, matrix, V, edges)
    if cycle:
        V, ind, folds = delete_vertex(u, V, matrix, degree, ind, V1, V2, V3, folds)
    else:
        # v, w ∉ P neighbours of v1, vl respectively, already in variable 'edges'
        v = edges.pop()
        w = edges.pop()
        if v == w:
            V, ind, folds = delete_vertex(v, V, matrix, degree, ind, V1, V2, V3, folds)
        elif len(P) % 2 == 1:
            if matrix[v, w] == 1:
                V, ind, folds = delete_vertex(v, V, matrix, degree, ind, V1, V2, V3, folds)
                V, ind, folds = delete_vertex(w, V, matrix, degree, ind, V1, V2, V3, folds)
            else:
                for j in P[1:]:
                    ind, folds, V = check_fold(j, False, ind, folds, V)
                for i in P:
                    V2.discard(i)
                matrix[P[0], w] = 1
                matrix[w, P[0]] = 1
                matrix[P[0], v] = 1
                matrix[v, P[0]] = 1
                P.pop(0)
                for i in reversed(P):
                    S.append(i)
        else:
            for j in P:
                V = V[V != j]
                V2.discard(j)
            if matrix[v, w] != 1:
                matrix[v, w] = 1
                matrix[w, v] = 1
            else:
                degree[v] -= 1
                degree[w] -= 1
                if degree[w] == 2:
                    V3.remove(w)
                    V2.add(w)
                if degree[v] == 2:
                    V3.remove(v)
                    V2.add(v)

            for i in reversed(P):
                S.append(i)
    return V, matrix, ind, folds


def find_path(u: int, matrix: np.ndarray, V: np.ndarray, edges: list):
    neigh_u = neighbours(matrix[u], V)
    path = [u]
    cycle = aux(True, path, u, neigh_u, matrix, V, edges)
    if not cycle:
        cycle = aux(False, path, path[0], neigh_u, matrix, V, edges)
    return path, cycle


def aux(left, path, u, neigh_u, matrix, V, edges):
    cycle = False
    if left:
        i = 0
        j = 1
    else:
        i = 1
        j = -2
    # first check outside of while loop because the loop requires two elements in path
    vert = neigh_u[i]
    neigh = neighbours(matrix[vert], V)
    if not cycle and len(neigh) == 2:
        if left:
            path.insert(0, vert)
        else:
            path.append(vert)
        if neigh[0] != path[j]:
            vert = neigh[0]
        else:
            vert = neigh[1]
        neigh = neighbours(matrix[vert], V)
        while not cycle and len(neigh) == 2:
            # add vertex to path
            if left:
                path.insert(0, vert)
            else:
                path.append(vert)
            # check if path is a cycle
            if (neigh[0] == path[j] and neigh[1] == u) or (neigh[1] == path[j] and neigh[0] == u):
                cycle = True
            else:
                # update vert and neigh with next vertex to check
                if neigh[0] != path[j]:
                    vert = neigh[0]
                    neigh = neighbours(matrix[vert], V)
                else:
                    vert = neigh[1]
                    neigh = neighbours(matrix[vert], V)
        if not cycle:
            edges.append(vert)
    elif not cycle:
        edges.append(vert)
    return cycle


def path_edge(v_edge: int, v_ne: int, matrix: np.ndarray, V: np.ndarray):
    n1 = neighbours(matrix[v_edge], V)
    if n1[0] != v_ne:
        return n1[0]
    else:
        return n1[1]


def inexact_redu(degree: dict, V3: set, V: np.ndarray, matrix: np.ndarray, ind, V1: set, V2: set, folds: np.ndarray):
    u = V3.pop()
    V3.add(u)
    max_d = degree[u]
    for i in V3:
        if degree[i] > max_d:
            max_d = degree[i]
            u = i
    V, ind, folds = delete_vertex(u, V, matrix, degree, ind, V1, V2, V3, folds)
    return V, ind, folds


def delete_vertex(vertex: int, V: np.ndarray, matrix: np.ndarray, degree: dict, ind, V1: set, V2: set, V3: set, folds: np.ndarray):
    for w in neighbours(matrix[vertex], V):
        degree[w] -= 1
        if degree[w] == 2:
            V3.remove(w)
            V2.add(w)
        elif degree[w] == 1:
            V2.discard(w)
            V1.add(w)
        elif degree[w] == 0:
            V1.remove(w)
            # ind = np.append(ind, [w])
            ind, folds, V = check_fold(w, True, ind, folds, V)
    ind, folds, V = check_fold(vertex, False, ind, folds, V)
    V1.discard(vertex)
    V2.discard(vertex)
    V3.discard(vertex)
    return V, ind, folds
