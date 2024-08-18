####################################################################################################
# Copyright (c) 2020 - 2024, EPFL / Blue Brain Project
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

# System imports
import os
import numpy
import seaborn
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


####################################################################################################
# Per-adjust all the plotting configuration
####################################################################################################
font_size = 30
seaborn.set_style("whitegrid")
pyplot.rcParams['axes.grid'] = 'True'
pyplot.rcParams['grid.linestyle'] = '-'
pyplot.rcParams['grid.linewidth'] = 2.0
pyplot.rcParams['grid.color'] = 'gray'
pyplot.rcParams['grid.alpha'] = 0.5
pyplot.rcParams['font.family'] = 'Helvetica LT Std'
# pyplot.rcParams['font.family'] = 'NimbusSanL'
pyplot.rcParams['font.monospace'] = 'Regular'
pyplot.rcParams['font.style'] = 'normal'
pyplot.rcParams['axes.linewidth'] = 1.0
pyplot.rcParams['axes.labelsize'] = font_size
pyplot.rcParams['axes.labelweight'] = 'bold'
pyplot.rcParams['xtick.labelsize'] = font_size
pyplot.rcParams['ytick.labelsize'] = font_size
pyplot.rcParams['legend.fontsize'] = font_size
pyplot.rcParams['figure.titlesize'] = font_size
pyplot.rcParams['axes.titlesize'] = font_size
pyplot.rcParams['xtick.major.pad'] = '10'
pyplot.rcParams['ytick.major.pad'] = '0'
pyplot.rcParams['axes.edgecolor'] = '1'


####################################################################################################
# @plot_group
####################################################################################################
def lighten_color(color,
                  amount=1.0):
    """Lightens the given color by multiplying (1-luminosity) by the given amount.
    Input can be matplotlib color string, hex string, or RGB tuple.

    :param color:
        A given color.
    :param amount:
        The illuminating amount.
    :return:
        The new color.
    """

    try:
        actual_color = matplotlib.colors.cnames[color]
    except ArithmeticError:
        actual_color = color
    actual_color = colorsys.rgb_to_hls(*matplotlib.colors.to_rgb(actual_color))
    return colorsys.hls_to_rgb(actual_color[0], 1 - amount * (1 - actual_color[1]), actual_color[2])


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

    # Convert the data to numpy array
    np_data = numpy.array(data)

    # Adjusting the figure size
    pyplot.figure(figsize=(10, 5))
    pyplot.tight_layout()

    # Min and max values
    min_value = min(data) * 0.95
    max_value = max(data) * 1.05
    major_ticks = numpy.linspace(min_value, max_value, 5)

    # Set the title inside the figure to save some space
    if plot_titles:
        pyplot.title(title, y=1.05)

    # Plot the histogram
    ax = seaborn.histplot(np_data, color=color, bins=40, alpha=0.95, stat="probability")

    # Percent formatter
    pyplot.gca().yaxis.set_major_formatter(
        PercentFormatter(xmax=xmax, decimals=decimals, symbol='%'))

    # Nothing
    pyplot.ylabel('')

    pyplot.gca().xaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:2.2f}'.format(y)))
    ax.set_xticks(major_ticks)

    # Adjust the Y-axis format
    # pyplot.gca().xaxis.set_major_locator(pyplot.MaxNLocator(5))
    pyplot.gca().yaxis.set_major_locator(pyplot.MaxNLocator(4))

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


colors = seaborn.color_palette("deep", 8)
verify_plotting_packages()
input_file = '1-input-max-angle.dist'
distribution = read_dist_file(input_file)
plot_distribution(input_directory=os.getcwd(), dist_file=input_file, output_directory=os.getcwd(),
                  title='Sample', color=colors[0])

