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

font_dirs = [os.path.dirname(os.path.realpath(__file__)) + '/fonts/']
font_dirs.extend([os.path.dirname(os.path.realpath(__file__)) + '/../fonts/'])

font_path = os.path.dirname(os.path.realpath(__file__)) + '/fonts/' + 'HelveticaLtObl.ttf'
font_manager.fontManager.addfont(font_path)
prop = font_manager.FontProperties(fname=font_path)

font_size = 30
seaborn.set_style("whitegrid")
pyplot.rcParams['axes.grid'] = 'True'
pyplot.rcParams['grid.linestyle'] = '-'
pyplot.rcParams['grid.linewidth'] = 1.0
pyplot.rcParams['grid.color'] = 'black'
pyplot.rcParams['grid.alpha'] = 0.1
pyplot.rcParams['font.family'] = prop.get_family()
# pyplot.rcParams['font.family'] = 'NimbusSanL'
pyplot.rcParams['font.style'] = 'normal'
pyplot.rcParams['axes.labelweight'] = 'light'
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
    font_dirs.extend([os.path.dirname(os.path.realpath(__file__)) + '/../fonts/'])
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
# @plot_back2back_histograms_normalized
####################################################################################################
def plot_histograms_normalized(dists_directory,
                               hist,
                               output_directory,
                               output_prefix,
                               title=None,
                               invert=False,
                               figure_width=2,
                               figure_height=10,
                               bins=50,
                               color_1='red',
                               color_2='blue',
                               axvline_color='black',
                               bin_width=0.95,
                               save_pdf=False,
                               save_svg=False,
                               dpi=150,
                               edge_gap=0.05):
    # Title
    if title is not None:
        print('\t* Plotting [%s]' % title)

    # Read the distributions
    data = read_dist_file('%s/%s' % (dists_directory, hist), invert=invert)

    # Compute the ranges
    min_value = min(data)
    max_value = max(data)

    print(min_value, max_value)

    # Clear figure, getting ready for a new figure
    pyplot.clf()

    # A new figure with the given dimensions size
    pyplot.figure(figsize=(figure_width, figure_height))
    pyplot.tight_layout()

    # Create a new frame for the plot to combine both
    frame = pyplot.gca()

    ry, rx = numpy.histogram(data, bins=bins, range=(min_value, max_value))

    ry = ry / max(ry)

    x_min = min(rx)
    x_max = max(rx)
    delta = x_max - x_min
    step = delta / bins
    bins = numpy.arange(x_min, x_max, step)

    # Right histogram
    pyplot.barh(bins, ry, color=color_1, height=step * bin_width)

    # Right box plot
    rvalue = 1.25
    bpr = pyplot.boxplot(data, positions=[rvalue], showfliers=True,
                         flierprops=dict(marker='o', markersize=5, alpha=0.5,
                                         markerfacecolor=color_1, markeredgecolor=color_1))

    for box in bpr['boxes']:
        box.set(color=color_1, linewidth=1)
    for whisker in bpr['whiskers']:
        whisker.set(color=color_1, linewidth=1)
    for cap in bpr['caps']:
        cap.set(color=color_1, linewidth=1, xdata=cap.get_xdata() + (-0.025, 0.025))
    for median in bpr['medians']:
        median.set(color=axvline_color, linewidth=1)

    # Only plot the Y-axis
    frame.axes.get_xaxis().set_visible(False)
    frame.axes.get_yaxis().set_visible(True)

    # Remove any labels
    pyplot.xlabel('')
    if title is not None:
        pyplot.ylabel(title, labelpad=20)
    else:
        pyplot.ylabel('')
    pyplot.gca().yaxis.set_major_locator(pyplot.MaxNLocator(10))

    # The central line
    pyplot.axvline(0.0)
    pyplot.axvline(linewidth=2, color=axvline_color)

    # Save PNG by default
    pyplot.savefig('%s/%s.png' % (output_directory, output_prefix),
                   dpi=dpi, bbox_inches='tight')

    # Save PDF
    pyplot.savefig('%s/%s.pdf' % (output_directory, output_prefix),
                   dpi=dpi, bbox_inches='tight') if save_pdf else None

    # Save SVG
    pyplot.savefig('%s/%s.svg' % (output_directory, output_prefix),
                   dpi=dpi, bbox_inches='tight') if save_svg else None

    # Close figure to reset
    pyplot.clf()
    pyplot.cla()
    pyplot.close()

    # Return a reference to the PNG image
    return output_prefix + '.png'

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
    ax = seaborn.histplot(np_data, color=color, bins=50, alpha=0.95, stat="count", log_scale=False, zorder=3)
    #ax.set_xticks([1.0, 10, 100, 1000])
    # Formatters
    # pyplot.gca().xaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:2.2f}'.format(y)))

    # No label
    pyplot.ylabel('')

    # Only plot the Y-axis
    ax.axes.get_xaxis().set_visible(True)
    ax.axes.get_yaxis().set_visible(True)
    ax.spines['bottom'].set_color('black')
    ax.grid(zorder=0)

    # Adjust the Y-axis format
    # ax.set_xticks(major_ticks)

    #pyplot.gca().xaxis.set_major_locator(pyplot.MaxNLocator(3))
    # pyplot.gca().yaxis.set_major_locator(pyplot.MaxNLocator(4))

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
def plot_distributions(keyword,
                       distributions,
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
    colors = seaborn.color_palette("flare", 6)

    print('  * Plotting Distributions')

    # A list of all the distributions in .png format
    distributions_pngs = list()
    for distribution in distributions:

        if keyword in distribution:

            if 'number-samples-per-section' in distribution:
                c = colors[0]
                distributions_pngs.append(plot_histograms_normalized(
                    input_directory, distribution, output_directory,
                    output_prefix='number-samples-per-section',
                    title='Number of Samples per Section', color_1=c))

            if 'samples-radii' in distribution:
                c = colors[1]
                distributions_pngs.append(plot_histograms_normalized(
                    input_directory, distribution, output_directory,
                    output_prefix='samples-radii',
                    title='Samples Radii (μm)', color_1=c))

            if 'section-average-radius' in distribution:
                c = colors[2]
                distributions_pngs.append(plot_histograms_normalized(
                    input_directory, distribution, output_directory,
                    output_prefix='section-average-radius',
                    title='Sections Average Radii (μm)', color_1=c))

            if 'sections-length' in distribution:
                c = colors[3]
                distributions_pngs.append(plot_histograms_normalized(
                    input_directory, distribution, output_directory,
                    output_prefix='sections-length',
                    title='Sections Lengths (μm)', color_1=c))

            if 'segments-length' in distribution:
                c = colors[4]
                distributions_pngs.append(plot_histograms_normalized(
                    input_directory, distribution, output_directory,
                    output_prefix='segments-length',
                    title='Segments Length (μm)', color_1=c))

            if 'sections-surface-area' in distribution:
                c = colors[4]
                distributions_pngs.append(plot_histograms_normalized(
                    input_directory, distribution, output_directory,
                    output_prefix='sections-surface-area',
                    title='Sections Surface Area', color_1=c))

            if 'sections-volume' in distribution:
                c = colors[4]
                distributions_pngs.append(plot_histograms_normalized(
                    input_directory, distribution, output_directory,
                    output_prefix='sections-volume',
                    title='Section Volume', color_1=c))

            if 'segments-surface-area' in distribution:
                c = colors[4]
                distributions_pngs.append(plot_histograms_normalized(
                    input_directory, distribution, output_directory,
                    output_prefix='segments-surface-area',
                    title='Segments Surface Area', color_1=c))

            if 'segments-volume' in distribution:
                c = colors[4]
                distributions_pngs.append(plot_histograms_normalized(
                    input_directory, distribution, output_directory,
                    output_prefix='segments-volume',
                    title='Segments Volume', color_1=c))

    # Return a reference to the images
    return distributions_pngs


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
    distributions_pngs = plot_distributions(
        keyword='.dist', distributions=distributions, input_directory=args.input_directory,
        output_directory=args.output_directory, plot_titles=True, use_kde=False)


