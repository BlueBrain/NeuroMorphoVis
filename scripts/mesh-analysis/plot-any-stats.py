####################################################################################################
# Copyright (c) 2020, EPFL / Blue Brain Project
#               Marwan Abdellah <marwan.abdellah@epfl.ch>
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

# System imports
import os
import numpy
import seaborn
import argparse
import matplotlib
import matplotlib.pyplot as pyplot
import matplotlib.font_manager as font_manager
import matplotlib.ticker
import colorsys
from matplotlib.ticker import PercentFormatter
from matplotlib.ticker import FuncFormatter
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


font_size = 40
#seaborn.set_style("whitegrid")
pyplot.rcParams['axes.grid'] = 'True'
pyplot.rcParams['grid.linestyle'] = '--'
pyplot.rcParams['grid.linewidth'] = 1.0
pyplot.rcParams['grid.color'] = 'black'
pyplot.rcParams['grid.alpha'] = 0.5
pyplot.rcParams['font.family'] = 'Helvetica LT Std'
# pyplot.rcParams['font.family'] = 'NimbusSanL'
pyplot.rcParams['font.monospace'] = 'Regular'
pyplot.rcParams['font.style'] = 'normal'
pyplot.rcParams['axes.labelweight'] = 'bold'
pyplot.rcParams['axes.linewidth'] = 1.0
pyplot.rcParams['axes.labelsize'] = font_size
pyplot.rcParams['xtick.labelsize'] = font_size * 1
pyplot.rcParams['ytick.labelsize'] = font_size * 1
pyplot.rcParams['legend.fontsize'] = font_size
pyplot.rcParams['figure.titlesize'] = font_size
pyplot.rcParams['axes.titlesize'] = font_size
pyplot.rcParams['xtick.major.pad'] = '10'
pyplot.rcParams['ytick.major.pad'] = '10'
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
# @read_dist_file
####################################################################################################
def read_dist_file(file_path,
                   invert=False):
    """Reads the distribution file into a list.

    :param file_path:
        The path to the input file.
    :param invert:
        If set to True, invert the read values.
    :return:
    """

    # Data list
    data = list()

    # Open the file
    f = open(file_path, 'r')
    for line in f:
        if 'inf' in line:
            continue
        content = line.strip(' ').split(' ')
        value = float(content[1])
        if invert:
            value = 1.0 / value
        data.append(value)
    f.close()

    # Return a list of the data read from the file
    return data


####################################################################################################
# @plot_distribution
####################################################################################################
def plot_distribution(input_directory,
                      dist_file,
                      output_directory,
                      title,
                      plot_titles=True,
                      xmax=100,
                      decimals=2,
                      kde=False,
                      color='b',
                      invert=False,
                      save_pdf=False,
                      save_svg=False,
                      dpi=150):
    """Plots a given distribution file into an image.

    :param input_directory:
        The directory where the file exists.
    :param dist_file:
        The distribution file.
    :param output_directory:
        The directory where the image will be written.
    :param title:
        Figure title.
    :param plot_titles:
        Flag to plot the titles or not.
    :param xmax:
        X-value maximum.
    :param decimals:
        Decimals
    :param kde:
        Add the KDE curve.
    :param color:
        Curve color.
    :param invert:
        If set invert the curve.
    :param save_pdf:
        If set to True, save the figure into a PDF file.
    :param save_svg:
        If set to True, save the figure into an SVG image.
    :param dpi:
        Dot per inch to define the resolution
    :return:
        Returns a reference to the resulting png image
    """

    print('\t* Plotting [%s]' % title)

    # Clear figure
    pyplot.clf()

    # Get the data list
    data = read_dist_file('%s/%s' % (input_directory, dist_file), invert=invert)


    # Min and max values
    min_value = min(data)
    max_value = max(data)
    major_ticks = numpy.linspace(min_value, max_value, 4)



    # Convert the data to numpy array
    np_data = numpy.array(data)

    # Create a new frame for the plot to combine both
    frame = pyplot.gca()

    # Adjusting the figure size
    pyplot.figure(figsize=(10, 5))
    pyplot.tight_layout()

    # Set the title inside the figure to save some space
    if plot_titles:
        pyplot.title(title, y=1.05)

    # Plot the histogram
    ax = seaborn.histplot(np_data, color=color, bins=50, alpha=0.95)

    # No label
    pyplot.ylabel('')

    # Only plot the Y-axis
    ax.axes.get_xaxis().set_visible(True)
    ax.axes.get_yaxis().set_visible(True)
    ax.spines['bottom'].set_color('black')
    ax.grid(zorder=0)

    # Image prefix
    image_prefix = '%s/%s' % (output_directory, dist_file.replace('.dist', ''))

    # By default, save the figure into a PNG image
    pyplot.savefig(image_prefix + '.png', dpi=dpi, bbox_inches='tight')

    # Save PDF
    if save_pdf:
        pyplot.savefig(image_prefix + '.pdf', dpi=dpi, bbox_inches='tight')

    # Save SVG
    if save_svg:
        pyplot.savefig(image_prefix + '.svg', dpi=dpi, bbox_inches='tight')

    # Close figure to reset
    pyplot.clf()
    pyplot.cla()
    pyplot.close()

    # Return a reference to the png image
    return dist_file.replace('.dist', '.png')


####################################################################################################
# @parse_command_line_arguments
####################################################################################################
def parse_command_line_arguments():

    # Add all the options
    description = 'Plots the Data distance'
    parser = argparse.ArgumentParser(description=description)

    arg_help = 'Input directory that contains all the log files'
    parser.add_argument('--input-directory', action='store', help=arg_help)

    arg_help = 'Output directory, where the final results will be written'
    parser.add_argument('--output-directory', action='store', help=arg_help)

    # Parse the arguments
    return parser.parse_args()


####################################################################################################
# @plot_group
####################################################################################################
def plot_distributions(distributions,
                       input_directory,
                       output_directory,
                       plot_titles=False,
                       use_kde=False,
                       color='tab:blue'):
    """Plots the different distributions of the mesh.

    :param keyword:
        Searching keyword for locating the file.
    :param distributions:
        All the distributions found in a directory.
    :param input_directory:
        The directory that contains all the distributions.
    :param output_directory:
        The directory where the results will be written.
    :param plot_titles:
        If True, the title will be added.
    :param use_kde:
        Use KDE for the distributions/
    :param color:
        Distributions color.
    :return:
        A list of PNGs corresponding to the distributions colors.
    """

    # Get the colormap
    colors = seaborn.color_palette("flare", 10)

    print('  * Plotting Distributions')

    # A list of all the distributions in .png format
    for distribution in distributions:
        print(distribution)
        plot_distribution(
            input_directory, distribution, output_directory,
            title='X', color=colors[0],
            kde=use_kde, plot_titles=plot_titles)


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

    # Get all the files in the distributions directory
    all_files = os.listdir(args.input_directory)

    # List all the distributions
    distributions = list()
    for f in all_files:
        if '.dist' in f:
            distributions.append(f)

    # Plot the distributions
    plot_distributions(distributions=distributions, input_directory=args.input_directory,
                       output_directory=args.output_directory)


