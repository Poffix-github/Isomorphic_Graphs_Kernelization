import numpy
from networkx.generators.random_graphs import erdos_renyi_graph


def new_graph(nodes: int, probability: float):
    a_matrix = free_graph(nodes, probability)

    file = 'C:/Users/gcmil/Desktop/tests/AdjacencyMatrices.txt'

    with open(file, 'a') as f:
        for row in a_matrix:
            for cell in row:
                f.write(str(cell))
            f.write('\n')
        f.write('EOM\n')

    return a_matrix


def free_graph(nodes, probability):
    g = erdos_renyi_graph(nodes, probability)
    a_matrix = numpy.zeros((nodes, nodes), int)

    for x, ly in g.adjacency():
        for y in iter(ly):
            a_matrix[x][y] = 1

    return a_matrix
