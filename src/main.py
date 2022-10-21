import numpy as np
import time
from Reductions import LinearTime, VertexFolding, Twin, Unconfined
from GraphInput import graph_creator, graph_reader, graph_generator, graph_writer
from Utilities import neighbours
from src.Complement import complement
from src.Extra import RandomGraphs
from src.Extra.retry import retest
from src.Isomorphism import check_isomorphism, association_matrix
from src.Outputs import draw_plots, archive_results
from os.path import exists as file_exists
from multiprocessing import Process, Lock


def main():
    # adj = retest()
    # adj = am.translator()
    # adj = Extra.RandomGraphs.free_graph(length, probability)
    # adj = Extra.RandomGraphs.new_graph(length, probability)
    print('start')

    length = 100
    probability = [0.01, 0.03, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.97, 0.99]
    path = '../data/'
    rep = 100
    time_all = []
    size_all = []
    accuracy_all = []

    for p in probability:
        print('Probability: ' + str(p))
        time_p = []
        size_p = []
        acc_p = []

        file_path = path + 'graph_p_' + str(p) + '.txt'
        file_path_a = path + str(p) + '_graph_a' + '.txt'
        file_path_b = path + str(p) + '_graph_b' + '.txt'
        # if not file_exists(file_path_a):
        #    graph_creator(length, p, file_path_a, rep)
        for ass_matrix, isomorphism in graph_reader(file_path, rep):
        # with open(file_path_a, 'w') as f:
        #    f.close()
        # with open(file_path_b, 'w') as f:
        #     f.close()
        # for adj, iso in graph_generator(length, p, rep):
            # ass_matrix, isomorphism = association_matrix(adj, iso)
            # save isomorphic graphs on files in parallel
            # Process(target=graph_writer, args=(file_path_a, adj)).start()
            # Process(target=graph_writer, args=(file_path_b, iso)).start()

            V = np.arange(0, ass_matrix.shape[0])
            c_matrix = complement(ass_matrix)
            folds = np.empty((0, 6), int)   # saved folding history from Vertex Folding and Twin reductions
            mis = np.empty(0, int)    # Maximum Independent Set

            reduction = True
            start_time = time.time()
            while reduction:
                old_length = V.size

                # print('Start Linear Time')
                c_matrix, _, mis, folds = LinearTime.redu_linear_time(c_matrix, V, mis, folds)
                for i in mis:
                    V = V[V != i]

                # print('Start Vertex Folding')
                c_matrix, V, folds = VertexFolding.redu_vertex_folding(c_matrix, V, folds)

                # print('Start Twin')
                c_matrix, V, mis, folds = Twin.redu_twin(c_matrix, V, mis, folds)

                # print("Start Unconfined")
                c_matrix, V, mis, folds = Unconfined.redu_unconfined(c_matrix, V, mis, folds)

                if old_length == V.size or V.size == 0:
                    reduction = False

            finish_time = time.time()
            time_p.append(finish_time - start_time)
            size_p.append(V.size)
            num_correct_mis = check_isomorphism(mis, isomorphism, V.size)   # returns -1 if kernel is not empty
            acc_p.append(num_correct_mis/length)

        time_all.append(time_p)
        size_all.append(size_p)
        accuracy_all.append(acc_p)

    archive_results(probability, size_all, time_all, accuracy_all)

    draw_plots(probability, rep)

    print('finish')

# TODO: cancella
def debug():
    length = 12
    probability = 0.1
    # for i in range(100):
    # adj = RandomGraphs.new_graph(length, probability)
    adj = retest()

    V = np.arange(0, adj.shape[0])
    c_matrix = complement(adj)
    folds = np.empty((0, 6), int)  # saved folding history from Vertex Folding and Twin reductions
    mis = np.empty(0, int)  # Maximum Independent Set

    reduction = True
    while reduction:
        old_length = V.size
        c_matrix, V, folds = VertexFolding.redu_vertex_folding(c_matrix, V, folds)
        c_matrix, V, mis, folds = Twin.redu_twin(c_matrix, V, mis, folds)
        c_matrix, V, mis, folds = Unconfined.redu_unconfined(c_matrix, V, mis, folds)

        if old_length == V.size or V.size == 0:
            reduction = False

    print('finish')


if __name__ == '__main__':
    main()
