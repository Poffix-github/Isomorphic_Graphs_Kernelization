import random
import numpy as np
from networkx import relabel_nodes, Graph, DiGraph

from src.Utilities import deg


def association_matrix(a_matrix: np.ndarray, b_matrix: np.ndarray):
    vertices = dict()
    n = 0   # number of vertices
    b_all_deg = list()
    ab_n = a_matrix.shape[0]
    # create vertices
    # V = {(i, h) ∈ V' x V": deg(i) = deg(h)}
    for i in range(ab_n):
        a_deg = deg(a_matrix[i])
        for h in range(i, ab_n):
            if i == 0:
                b_all_deg.append(deg(b_matrix[h]))
            if a_deg == b_all_deg[h]:
                vertices.update({n: (i, h)})
                n += 1
    # create association matrix
    # E={((i, h), (j, k)) ∈ V x V: i ≠ j, h ≠ k and (i, j) ∈ E' ⟺ (h, k) ∈ E"}
    ass_matrix = np.zeros((n, n), int)
    for x in range(n):
        i, h = vertices.get(x)
        for y in range(n):
            j, k = vertices.get(y)
            if i != j and h != k and not bool(a_matrix[i, j] - b_matrix[h, k]):
                ass_matrix[x, y] = 1
    return ass_matrix, vertices


def isomorphic_graph(g: DiGraph | Graph):
    """Creates an isomorphic graph of the one given"""
    random.seed()
    mapping = dict()
    iso_list = list(range(len(g)))
    n = random.randint(int(len(g)/2), len(g))
    for i in range(n):
        x = random.randrange(0, len(g))
        y = random.randrange(0, len(g))
        iso_list[x], iso_list[y] = iso_list[y], iso_list[x]
    for k, e in zip(range(len(g)), iso_list):
        mapping.update({k: e})
    h = relabel_nodes(g, mapping)
    return h


def check_isomorphism(mis: np.ndarray, isomorphism: dict, kernel_size: int):
    if kernel_size == 0:
        V = [isomorphism[x][0] for x in mis]   # vertices of one graph present in the found mis
        V = set(V)
        return len(V)
    else:
        return -1
