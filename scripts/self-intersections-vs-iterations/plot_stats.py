import os
import matplotlib
import pandas as pd
import matplotlib.pyplot as plt

####################################################################################################
# @read_file
####################################################################################################
def read_file(file_path):
    f = open(file_path, 'r')
    data = list()
    for l in f:
        _value = l.strip('\n').split(', ')
        _value = _value[1]
        _value = _value.replace('SI[', '')
        _value = _value.replace(']', '')
        _value = int(_value)
        data.append(_value)
    return data

####################################################################################################
# @read_file
####################################################################################################
def read_files(input_directory, extension='.txt'):

    files = list()
    legend = list()
    for file in os.listdir(input_directory):
        if file.endswith(extension):
            files.append('%s/%s' % (input_directory, file))
            legend.append(file.replace('.txt', ''))

    data = list()

    for file in files:
        data.append(read_file(file))

    return data, legend

####################################################################################################
# @plot_data
####################################################################################################
def plot_data(data, legend):

    # Adjusting the matplotlib parameters
    plt.rcParams['axes.grid'] = 'False'
    plt.rcParams['font.family'] = 'Arial'
    plt.rcParams['axes.linewidth'] = 0.0
    plt.rcParams['axes.labelsize'] =  10
    plt.rcParams['axes.labelweight'] = 'regular'
    plt.rcParams['xtick.labelsize'] = 10
    plt.rcParams['ytick.labelsize'] = 10
    plt.rcParams['legend.fontsize'] = 10
    plt.rcParams['axes.titlesize'] = 1.25 * 10
    plt.rcParams['axes.axisbelow'] = True
    plt.rcParams['axes.edgecolor'] = '0.1'

    fig, ax = plt.subplots()
    for d in data:
        ax.plot(d)

    #plt.xlim(40, 50)
    #plt.ylim(0, 50)

    plt.legend(legend, ncol=4, loc='upper right')

    matplotlib.pyplot.show()



stats_directory = '/ssd2/biovis2024-data/nmv-output-aspiny/self-intersections'

_data, _legend = read_files(stats_directory)
plot_data(_data, _legend)
