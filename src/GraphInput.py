import ast
import numpy
import numpy as np
from networkx import erdos_renyi_graph
from src.Isomorphism import isomorphic_graph, association_matrix


def graph_creator(l: int, p: float, file_path: str, n: int):
    with open(file_path, 'w') as f:
        f.close()

    for adj_matrix, iso_matrix in graph_generator(l, p, n):
        ass_matrix, vertices = association_matrix(adj_matrix, iso_matrix)
        with open(file_path, 'a') as f:
            f.write(str(vertices) + '\n')
            for row in ass_matrix:
                for cell in row:
                    f.write(str(cell))
                f.write('\n')
            f.write('EOM\n')


def graph_writer(file_path: str, matrix: np.ndarray):
    with open(file_path, 'a') as f:
        for row in matrix:
            for cell in row:
                f.write(str(cell))
            f.write('\n')
        f.write('EOM\n')


def graph_generator(l: int, p: float, n: int):
    for i in range(n):
        g = erdos_renyi_graph(l, p)     # TODO: ottimizza, solo per la probabilità 0.01 usa questa funzione, https://networkx.org/documentation/networkx-1.10/reference/generated/networkx.generators.random_graphs.fast_gnp_random_graph.html#fast-gnp-random-graph
        h = isomorphic_graph(g)
        a_matrix = numpy.zeros((l, l), int)
        iso_matrix = numpy.zeros((l, l), int)

        for x, ly in g.adjacency():
            for y in iter(ly):
                a_matrix[x][y] = 1

        for x, ly in h.adjacency():
            for y in iter(ly):
                iso_matrix[x][y] = 1

        yield a_matrix, iso_matrix


def graph_reader(path: str, n: int):
    with open(path, 'r') as f:
        for i in range(n):
            data = f.readline()
            if data == 'EOM\n':
                data = f.readline()
            isomorphism = ast.literal_eval(data)
            data = f.readline()

            dim = len(data) - 1
            matrix = numpy.zeros((dim, dim), int)

            matrix[0] = [x for x in data if x != '\n']
            i = 1
            while i < dim:
                data = f.readline()
                matrix[i] = [x for x in data if x != '\n']
                i += 1
            yield matrix, isomorphism
