from statistics import variance, mean
import matplotlib.pyplot as plt
import numpy as np
from decimal import getcontext, Decimal

path = '../results/'
# path = 'C:/Users/gcmil/Desktop/Corsi/Tesi/Evaluation/n=100/'
file_prefix = 'graph_p_'
txt_type = '.txt'


def draw_plots(probability: list, rep: int):
    times, sizes, acc = get_avg_var(probability, rep)

    getcontext().prec = 4
    # CPU time
    times[0] = [Decimal(i) for i in times[0]]
    aux(probability, times[0])
    plt.ylabel('Average CPU time (seconds)')
    for i, label in enumerate(times[1]):
        plt.annotate('±({:5.4f})'.format(label), (i*0.07, times[0][i]))
    plt.savefig(path + 'avg_CPU_time.png')
    plt.clf()
    # Kernel size
    aux(probability, sizes[0])
    plt.ylabel('Average Kernel size')
    plt.ylim(bottom=-0.001)
    for i, label in enumerate(sizes[1]):
        plt.annotate('±({:5.3f})'.format(label), (i * 0.07, sizes[0][i]))
    plt.savefig(path + 'avg_Kernel_size.png')
    plt.clf()
    # Accuracy
    acc[0] = [int(a * 100) for a in acc[0]]
    aux(probability, acc[0])
    plt.ylabel('Average Accuracy (percentage)')
    plt.ylim(bottom=0, top=105)
    for i, label in enumerate(acc[1]):
        plt.annotate('±({:5.3f})'.format(label), (i * 0.07, acc[0][i]))
    plt.savefig(path + 'avg_Accuracy.png')
    plt.clf()


def aux(x, y):
    xaxis = np.arange(0., 1.05, 0.07)
    plt.plot(xaxis, y, color='black', marker='D', linewidth=1, markersize=6)
    plt.xticks(xaxis, labels=x)
    plt.xlabel('expected connectivity')


def archive_results(probabilities, sizes, times, accuracies):
    for p, p_size, p_time, p_acc in zip(probabilities, sizes, times, accuracies):
        # file format:
        # Graph#  Reduction Time  Kern.Size  Accuracy
        #      1;     0.512421;           2;     1.00
        with open(path+file_prefix+str(p)+txt_type, 'w') as f:
            f.write('Graph#  Reduction Time  Kern.Size  Accuracy\n')
            for i, z in enumerate(zip(p_size, p_time, p_acc)):
                s, t, a = z
                if a == -1:
                    f.write('{:6}'.format(i)+';'+'{:14.6f}'.format(t)+';'+'{:12}'.format(s)+';'+'        -\n')
                else:
                    f.write('{:6}'.format(i)+';'+'{:14.6f}'.format(t)+';'+'{:12}'.format(s)+';'+'{:9.2f}'.format(a)+'\n')


def get_avg_var(probabilities, rep):
    """returns (list_of_avg_times, list_of_avg_sizes)"""
    time_all_avg = []
    time_all_var = []
    size_all_avg = []
    size_all_var = []
    acc_all_avg = []
    acc_all_var = []
    for p in probabilities:
        times = []
        sizes = []
        accu = []
        time_size_acc = get_data(p, rep)
        for t, s, a in time_size_acc:
            times.append(t)
            sizes.append(s)
            if a > 0:
                accu.append(a)
        time_all_avg.append(mean(times))
        time_all_var.append(variance(times)/100)
        size_all_avg.append(mean(sizes))
        size_all_var.append(variance(sizes))
        acc_all_avg.append(mean(accu))
        if len(accu) >= 2:
            acc_all_var.append(variance(accu))
        else:
            acc_all_var.append(0.)
    return [time_all_avg, time_all_var], [size_all_avg, size_all_var], [acc_all_avg, acc_all_var]


def get_data(file_number, rep):
    file_data = []
    with open(path + file_prefix + str(file_number) + txt_type, 'r') as f:
        f.readline()  # discard legend
        for i in range(rep):
            line = f.readline()
            data = line.split(';')
            acc = data[3].strip()
            if acc != '-':
                file_data.append([float(data[1].strip()), int(data[2].strip()), float(acc)])
            else:
                file_data.append([float(data[1].strip()), int(data[2].strip()), -1.])
    return file_data
