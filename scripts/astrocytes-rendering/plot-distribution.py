#!/usr/bin/python

# System imports
import sys, os, re, math
import subprocess
import argparse
import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager
from matplotlib.ticker import PercentFormatter
from matplotlib.ticker import FormatStrFormatter

FILE_TYPES = ['.png']
FILE_TYPE = '.png'



####################################################################################################
# @verify_plotting_packages
####################################################################################################
def verify_plotting_packages():
    """Verifies that all the plotting packages are installed. Otherwise, install the missing one.
    """
    
    import matplotlib
    from matplotlib import font_manager

    # Import the fonts
    font_dirs = [os.getcwd() + '/fonts/' ]
    font_files = font_manager.findSystemFonts(fontpaths=font_dirs)
    font_list = font_manager.createFontList(font_files)
    font_manager.fontManager.ttflist.extend(font_list)


####################################################################################################
# @parse_command_line_arguments
####################################################################################################
def parse_command_line_arguments(arguments=None):

    # Add all the options
    description = 'Plotting'
    parser = argparse.ArgumentParser(description=description)

    arg_help = 'Input file'
    parser.add_argument('--input', action='store', dest='input', help=arg_help)

    arg_help = 'Output directory where output written'
    parser.add_argument('--output', action='store', dest='output', help=arg_help)
                        
    # Parse the arguments
    return parser.parse_args()


####################################################################################################
# @read_dist_file
####################################################################################################
def read_dist_file(file_path):

    data = list()
    file = open(file_path, 'r')
    for line in file:
        content = line.strip(' ').split(' ')
        index = int(content[0])
        value = float(content[1])
        data.append(1.0 / value)
    file.close()
    return data


####################################################################################################
# @ plot_dist_file
####################################################################################################
def plot_dist_file(dist_file,
                   output_directory,
                   title='Stats',
                   plot_titles=True,
                   xmax=100,
                   decimals=1,
                   kde=False,
                   color='b'):

    print('\t* ' + title)                   

    # Clear figure 
    plt.clf()
    
    # Get the data list 
    data = read_dist_file(dist_file)
    
    max_value = max(data)
    min_value = min(data)
    print('Min. %f, Max. %f' % (min_value, max_value))

    sns.set(color_codes=True)

    sns.set_style("whitegrid")
    plt.rcParams['axes.grid'] = 'False'
    plt.rcParams['font.family'] = 'NimbusSanL'
    plt.rcParams['font.monospace'] = 'Regular'
    plt.rcParams['font.style'] = 'normal'

    plt.rcParams['axes.linewidth'] = 0.0
    plt.rcParams['axes.labelsize'] = 10
    plt.rcParams['axes.labelweight'] = 'bold'
    plt.rcParams['xtick.labelsize'] = 20
    plt.rcParams['ytick.labelsize'] = 20
    plt.rcParams['legend.fontsize'] = 20
    plt.rcParams['figure.titlesize'] = 18
    plt.rcParams['axes.titlesize'] = 16

    # Convert the data to numpy array 
    np_data = np.array(data)

    # Adjust the Y-axis format 
    plt.gca().yaxis.set_major_formatter(PercentFormatter(xmax=xmax, decimals=decimals, symbol=' %'))

    # Set the title
    if plot_titles:
        plt.title(title)

    # Plot the histogram 
    sns.distplot(np_data, color='r', hist=True, kde=kde, norm_hist=True, bins=50,
        hist_kws={"color": color, "lw": 0.75},
        kde_kws={"color": color, "lw": 0.75})

    # Save the figure
    import ntpath
    file_name = ntpath.basename(dist_file).replace('.dist', '.png')
    plt.savefig('%s/%s' % (output_directory, file_name), dpi=300)    

    # Close figure to reset
    plt.close()

    
####################################################################################################
# @ Main
####################################################################################################
if __name__ == "__main__":

    # Parse the command line arguments
    args = parse_command_line_arguments()
    
    verify_plotting_packages()

    plot_titles = False
    use_kde = True
    
    plot_dist_file(args.input, args.output, kde=use_kde)