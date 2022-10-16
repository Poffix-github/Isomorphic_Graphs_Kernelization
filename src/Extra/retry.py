import numpy


def retest(file = 'C:/Users/gcmil/Desktop/tests/retry.txt'):

    with open(file, 'r') as f:
        data = f.readline()
        dim = len(data) - 1
        matrix = numpy.zeros((dim, dim), int)
        matrix[0] = [x for x in data if x != '\n']
        i = 1
        while i < dim:
            data = f.readline()
            matrix[i] = [x for x in data if x != '\n']
            i += 1

    return matrix

def retest_all():
    file = 'C:/Users/gcmil/Desktop/tests/AdjacencyMatrices.txt'


