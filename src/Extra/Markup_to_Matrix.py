import numpy as np


def translator():
    markup_path = 'C:/Users/gcmil/Desktop/Running_Matrix.html'

    with open(markup_path, 'r') as f:
        file = f.readline()
    _, nodes = file.split('nodes=')
    nodes, edges = nodes.split('edges=')

    nodes_number = len(nodes.split('label')) - 1
    matrix = np.zeros((nodes_number, nodes_number), np.int8)

    edges = edges.split('},')
    for ed in edges:
        src, trg = ed.split(',')
        src = int(src[src.find(':') + 1:])
        if not trg.find('}]}') == -1:
            trg = int(trg[trg.find(':') + 1:trg.find('}')])
        else:
            trg = int(trg[trg.find(':') + 1:])
        matrix[src][trg] = 1
        matrix[trg][src] = 1

    print('Nodes: '+str(nodes_number)+'; Edges: '+str(len(edges)))
    return matrix
