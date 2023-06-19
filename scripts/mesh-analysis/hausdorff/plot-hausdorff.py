####################################################################################################
# Copyright (c) 2020, EPFL / Blue Brain Project
# Author(s): Marwan Abdellah <marwan.abdellah@epfl.ch>
#
# This file is part of NeuroMorphoVis <https://github.com/BlueBrain/NeuroMorphoVis>
#
# This program is free software: you can redistribute it and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation, version 3 of the License.
#
# This Blender-based tool is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.
# If not, see <http://www.gnu.org/licenses/>.
####################################################################################################

import sys
import numpy
import os
import argparse
import pandas
import seaborn
import matplotlib.pyplot as pyplot
import matplotlib.font_manager as font_manager


font_size = 25
seaborn.set_style("whitegrid")
pyplot.rcParams['axes.grid'] = 'True'
pyplot.rcParams['grid.linestyle'] = '--'
pyplot.rcParams['grid.linewidth'] = 1.0
pyplot.rcParams['grid.color'] = 'gray'
pyplot.rcParams['grid.alpha'] = 0.25
pyplot.rcParams['font.family'] = 'Helvetica LT Std'
pyplot.rcParams['font.family'] = 'NimbusSanL'
pyplot.rcParams['font.monospace'] = 'Regular'
pyplot.rcParams['font.style'] = 'normal'
pyplot.rcParams['axes.labelweight'] = 'light'
pyplot.rcParams['axes.linewidth'] = 1.0
pyplot.rcParams['axes.labelsize'] = font_size
pyplot.rcParams['xtick.labelsize'] = font_size
pyplot.rcParams['ytick.labelsize'] = font_size
pyplot.rcParams['legend.fontsize'] = font_size
pyplot.rcParams['figure.titlesize'] = font_size
pyplot.rcParams['axes.titlesize'] = font_size
pyplot.rcParams['xtick.major.pad'] = '10'
pyplot.rcParams['ytick.major.pad'] = '0'
pyplot.rcParams['axes.edgecolor'] = '1'


####################################################################################################
# @verify_plotting_packages
####################################################################################################
def verify_plotting_packages():

    # Import the fonts
    font_dirs = [os.path.dirname(os.path.realpath(__file__)) + '/fonts/']
    font_dirs .extend([os.path.dirname(os.path.realpath(__file__)) + '/../fonts/'])
    font_files = font_manager.findSystemFonts(fontpaths=font_dirs)
    for font_file in font_files:
        font_manager.fontManager.addfont(font_file)


####################################################################################################
# @ get_hausdorff_distance_value
####################################################################################################
def get_hausdorff_distance_value(log_file):

    # Initial value
    value = -1

    # Open the log file
    f = open(log_file)

    # Search for the RMS value
    for line in f:

        # If the value is found, return it
        if 'RMS' in line:
            line = line.split('RMS :')
            value = float(line[1])
            break

    # Close the file
    f.close()

    # Return the value
    return value


####################################################################################################
# @parse_command_line_arguments
####################################################################################################
def parse_command_line_arguments():

    # Add all the options
    description = 'Plots the Hausdorff distance'
    parser = argparse.ArgumentParser(description=description)

    arg_help = 'Input directory that contains all the log files'
    parser.add_argument('--input-directory', action='store', help=arg_help)

    arg_help = 'Output directory, where the final results will be written'
    parser.add_argument('--output-directory', action='store', help=arg_help)

    # Parse the arguments
    return parser.parse_args()


####################################################################################################
# @ Main
####################################################################################################
if __name__ == "__main__":

    # Parse the command line arguments
    args = parse_command_line_arguments()

    # Create the output directory if it does not exist
    if not os.path.exists(args.output_directory):
        os.mkdir(args.output_directory)

    # Plotting
    verify_plotting_packages()

    # Collection
    array = numpy.zeros((10, 10))

    # Iterations
    for itr in range(1, 10 + 1):

        # Iterations directory
        directory_name = 'hausdorff-%d-itr' % itr
        directory_path = '%s/%s' % (args.input_directory, directory_name)

        # Voxels per micron
        for vpm in range(1, 10 + 1):

            # Files
            file_name = '%d-vpm-watertight.hausdorff' % vpm
            file_path = '%s/%s' % (directory_path, file_name)

            # Fill the array
            array[itr - 1][vpm - 1] = get_hausdorff_distance_value(log_file=file_path)

    # Axes
    iterations = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
    vpms = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']

    # Construct the dataframe
    df = pandas.DataFrame(array, index=iterations, columns=vpms)

    # Clear figure, getting ready for a new figure
    pyplot.clf()

    # A new figure with the given dimensions size
    pyplot.figure(figsize=(10, 10))
    pyplot.tight_layout()

    # Create a new frame for the plot to combine both
    frame = pyplot.gca()

    # Compute the ticks
    major_ticks = numpy.linspace(array.min(), array.max(), 3)

    # Plot the dataframe
    ax = seaborn.heatmap(df, cmap='Spectral', annot=False, square=True,
                         linewidths=0.01, linecolor='white',
                         cbar_kws={"orientation": "horizontal",
                                   'pad': 0.2, "shrink": .65,
                                   'ticks': major_ticks,
                                   'label': 'Hausdorff Distance'})

    # Axis
    pyplot.yticks(rotation=0)

    ax.set_ylabel("Optimization Iterations")
    ax.set_xlabel("Voxels per Micron")

    # Save SVG
    pyplot.savefig('%s/%s.png' % (args.output_directory, 'hausdorff'),
                   dpi=300, bbox_inches='tight')

