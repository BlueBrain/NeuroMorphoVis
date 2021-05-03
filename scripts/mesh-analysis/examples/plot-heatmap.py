#!/usr/bin/python3

# System imports
import os
import re
import numpy
import seaborn
import pandas
import argparse
import matplotlib
import matplotlib.pyplot as pyplot
import matplotlib.font_manager as font_manager
import matplotlib.ticker
import colorsys
from matplotlib.ticker import PercentFormatter
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

####################################################################################################
# Per-adjust all the plotting configuration
####################################################################################################
font_size = 30
seaborn.set_style("whitegrid")
pyplot.rcParams['axes.grid'] = 'True'
pyplot.rcParams['grid.linestyle'] = '-'
pyplot.rcParams['grid.linewidth'] = 2
pyplot.rcParams['font.family'] = 'Helvetica LT Std' # 'NimbusSanL'
pyplot.rcParams['font.monospace'] = 'Bold'
pyplot.rcParams['font.style'] = 'normal'
pyplot.rcParams['axes.linewidth'] = 0.0
pyplot.rcParams['axes.labelsize'] = font_size
pyplot.rcParams['axes.labelweight'] = 'bold'
pyplot.rcParams['xtick.labelsize'] = font_size
pyplot.rcParams['ytick.labelsize'] = font_size
pyplot.rcParams['legend.fontsize'] = font_size
pyplot.rcParams['figure.titlesize'] = font_size
pyplot.rcParams['axes.titlesize'] = font_size
pyplot.rcParams['xtick.major.pad'] = '20'
pyplot.rcParams['ytick.major.pad'] = '12'
pyplot.rcParams['axes.edgecolor'] = '1'


####################################################################################################
# @Data
####################################################################################################
class Data:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.v = 0


####################################################################################################
# @verify_plotting_packages
####################################################################################################
def verify_plotting_packages():
    """Verifies that all the plotting packages are installed. Otherwise, install the missing one.
    """

    # Import the fonts
    font_dirs = [os.path.dirname(os.path.realpath(__file__)) + '/fonts/']
    font_files = font_manager.findSystemFonts(fontpaths=font_dirs)
    for font_file in font_files:
        font_manager.fontManager.addfont(font_file)


####################################################################################################
# @verify_plotting_packages
####################################################################################################
def draw_heatmap(input_data, x_label, y_label, title, output_path):

    # Lists
    x_axis_data = list()
    y_axis_data = list()
    values_data = list()
    for i in range(len(input_data)):
        x_axis_data.append(int(input_data[i].x))
        y_axis_data.append(int(input_data[i].y))
        values_data.append(input_data[i].v)

    # Dictionary
    data_dictionary = {'x': x_axis_data,
                       'y': y_axis_data,
                       'v': values_data}

    # Build the data frame
    data_frame = pandas.DataFrame(data_dictionary)

    # Data ready to be plot
    data_pivot = data_frame.pivot(index='x', columns='y', values='v')

    # Adjust the font
    seaborn.set_theme()
    pyplot.figure(figsize=(11, 10))
    seaborn.set(font='Helvetica LT Std')
    pyplot.legend(fontsize=font_size)

    # Draw the heatmap
    map_ax = seaborn.heatmap(data_pivot, annot=False, linewidths=.5)

    # Invert the axis
    map_ax.invert_yaxis()

    # Adjust the color-bar font
    color_bar = map_ax.collections[0].colorbar
    color_bar.ax.tick_params(labelsize=int(0.75 * font_size))

    pyplot.title(title, y=1.025, fontsize=font_size)
    pyplot.xlabel(x_label, fontsize=font_size)
    pyplot.ylabel(y_label, fontsize=font_size)

    # Font adjustments
    map_ax.set_xticklabels(map_ax.get_xmajorticklabels(), fontsize=font_size)
    map_ax.set_yticklabels(map_ax.get_ymajorticklabels(), fontsize=font_size)

    pyplot.tight_layout()
    # Save the figure
    pyplot.savefig('%s.png' % output_path)


####################################################################################################
# @load_triangles_info
####################################################################################################
def load_triangles_info(stats_file_path):

    file_name = os.path.basename(stats_file_path)
    re_result = re.findall('[0-9]+', file_name)

    optimization_iterations = re_result[0]
    decimation_factor = re_result[1]
    file_data = Data()
    file_data.x = optimization_iterations
    file_data.y = decimation_factor

    file_handler = open(stats_file_path, 'r')
    for line in file_handler:
        if 'Number Triangles' in line:
            line = line.split('| ')[1]
            if 'k' in line:
                line = line.split(' ')
                value = float(line[0]) * 1e3
            elif 'M' in line:
                line = line.split(' ')
                value = float(line[0]) * 1e6
            elif 'G' in line:
                line = line.split(' ')
                value = float(line[0]) * 1e9
            else:
                value = float(line[0])
            file_data.v = value
    return file_data


####################################################################################################
# @load_vertices_info
####################################################################################################
def load_vertices_info(stats_file_path):

    file_name = os.path.basename(stats_file_path)
    re_result = re.findall('[0-9]+', file_name)

    optimization_iterations = re_result[0]
    decimation_factor = re_result[1]
    file_data = Data()
    file_data.x = optimization_iterations
    file_data.y = decimation_factor

    file_handler = open(stats_file_path, 'r')
    for line in file_handler:
        if 'Number Vertices' in line:
            line = line.split('| ')[1]
            if 'k' in line:
                line = line.split(' ')
                value = float(line[0]) * 1e3
            elif 'M' in line:
                line = line.split(' ')
                value = float(line[0]) * 1e6
            elif 'G' in line:
                line = line.split(' ')
                value = float(line[0]) * 1e9
            else:
                value = float(line[0])
            file_data.v = value
    return file_data


####################################################################################################
# @load_volume_info
####################################################################################################
def load_volume_info(stats_file_path):

    file_name = os.path.basename(stats_file_path)
    re_result = re.findall('[0-9]+', file_name)

    optimization_iterations = re_result[0]
    decimation_factor = re_result[1]
    file_data = Data()
    file_data.x = optimization_iterations
    file_data.y = decimation_factor

    file_handler = open(stats_file_path, 'r')
    for line in file_handler:
        if 'Volume' in line:
            line = line.replace('³', '').split('| ')
            file_data.v = float(line[1])
    return file_data


####################################################################################################
# @load_volume_info
####################################################################################################
def load_surface_area_info(stats_file_path):

    file_name = os.path.basename(stats_file_path)
    re_result = re.findall('[0-9]+', file_name)

    optimization_iterations = re_result[0]
    decimation_factor = re_result[1]
    file_data = Data()
    file_data.x = optimization_iterations
    file_data.y = decimation_factor

    file_handler = open(stats_file_path, 'r')
    for line in file_handler:
        if 'Surface Area' in line:
            line = line.replace('²', '').split('| ')
            file_data.v = float(line[1])
    return file_data


####################################################################################################
# @parse_command_line_arguments
####################################################################################################
def parse_command_line_arguments(arguments=None):
    """Parses the input arguments.

    :param arguments:
        Command line arguments.
    :return:
        Arguments list.
    """

    # add all the options
    description = 'Plotting data into heatmaps '
    parser = argparse.ArgumentParser(description=description)

    arg_help = 'The input directory where the stats. files are.'
    parser.add_argument('--input-directory', action='store', help=arg_help)

    arg_help = 'Output directory, where the final images will be stored'
    parser.add_argument('--output-directory', action='store', help=arg_help)

    arg_help = 'Render the artistic version with high quality rendering'
    parser.add_argument('--artistic', action='store_true', default=False, help=arg_help)

    arg_help = 'The keyword that will pick the value, [input, dmc, optimized, watertight]'
    parser.add_argument('--keyword', action='store', help=arg_help)

    # Parse the arguments
    return parser.parse_args()


####################################################################################################
# @input_path
####################################################################################################
def load_files(input_path, keyword):

    # Search for the files, locate the.minfo file
    stats_files = list()
    for file in os.listdir(input_path):
        if file.endswith('.minfo'):
            if keyword in file:

                stats_files.append(file)
    return stats_files


####################################################################################################
# @parse_command_line_arguments
####################################################################################################
if __name__ == "__main__":

    # Parse the command line arguments
    args = parse_command_line_arguments()

    # Stats. files
    stats_files = load_files(args.input_directory, args.keyword)

    # Packages
    verify_plotting_packages()

    # Read the data
    data = list()
    for stats_file in stats_files:
        data.append(load_volume_info(args.input_directory + '/' + stats_file))
    draw_heatmap(input_data=data,
                 x_label='Optimization Iterations', y_label='Decimation Factor',
                 title='Total Volume', output_path='%s/volume-%s' % (os.getcwd(), args.keyword))

    data = list()
    for stats_file in stats_files:
        data.append(load_surface_area_info(args.input_directory + '/' + stats_file))
    draw_heatmap(input_data=data,
                 x_label='Optimization Iterations', y_label='Decimation Factor',
                 title='Surface Area',
                 output_path='%s/surface-area-%s' % (os.getcwd(), args.keyword))

    data = list()
    for stats_file in stats_files:
        data.append(load_vertices_info(args.input_directory + '/' + stats_file))
    draw_heatmap(input_data=data,
                 x_label='Optimization Iterations', y_label='Decimation Factor',
                 title='Number of Vertices',
                 output_path='%s/number-vertices-%s' % (os.getcwd(), args.keyword))

    data = list()
    for stats_file in stats_files:
        data.append(load_triangles_info(args.input_directory + '/' + stats_file))
    draw_heatmap(input_data=data,
                 x_label='Optimization Iterations', y_label='Decimation Factor',
                 title='Number of Triangles',
                 output_path='%s/number-triangles-%s' % (os.getcwd(), args.keyword))
