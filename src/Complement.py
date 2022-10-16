import numpy as np

def complement(matrix: np.ndarray):
    """Returns complement of one given adjacency matrix"""
    ones_matrix = np.ones(matrix.shape, int)
    np.fill_diagonal(ones_matrix, 0)
    return ones_matrix - matrix
