####################################################################################################
# Copyright (c) 2020 - 2021, EPFL / Blue Brain Project
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

# Blender imports
import bpy

# Internal imports
import nmv.scene
import nmv.interface

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

import utilities

####################################################################################################
# Per-adjust all the plotting configuration
####################################################################################################
font_size = 20
seaborn.set_style("whitegrid")
pyplot.rcParams['axes.grid'] = 'True'
pyplot.rcParams['grid.linestyle'] = '--'
pyplot.rcParams['grid.linewidth'] = 1.0
pyplot.rcParams['grid.color'] = 'gray'
pyplot.rcParams['grid.alpha'] = 0.25
pyplot.rcParams['font.family'] = 'Helvetica LT Std'
# pyplot.rcParams['font.family'] = 'NimbusSanL'
pyplot.rcParams['font.monospace'] = 'Regular'
pyplot.rcParams['font.style'] = 'normal'
pyplot.rcParams['axes.labelweight'] = 'bold'
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
# @plot_back2back_histograms
####################################################################################################
def plot_back2back_histograms(dists_directory,
                              output_directory,
                              hist_left,
                              hist_right,
                              output_prefix,
                              title=None,
                              invert=False,
                              figure_width=5,
                              figure_height=10,
                              bins=40,
                              color_1='red',
                              color_2='blue',
                              axvline_color='black',
                              bin_width=0.9,
                              save_pdf=False,
                              save_svg=False,
                              save_png=False,
                              dpi=150,
                              edge_gap=0.05):

    # Title
    if title is not None:
        print('\t* Plotting [%s]' % title)

    # Read the distributions
    data_left = utilities.read_dist_file('%s/%s' % (dists_directory, hist_left), invert=invert)
    data_right = utilities.read_dist_file('%s/%s' % (dists_directory, hist_right), invert=invert)

    # Clear figure, getting ready for a new figure
    pyplot.clf()

    # A new figure with the given dimensions size
    pyplot.figure(figsize=(figure_width, figure_height))
    pyplot.tight_layout()

    # Create a new frame for the plot to combine both
    frame = pyplot.gca()

    # Draw the histograms
    h1 = pyplot.hist(data_right, density=True,
                     bins=bins, orientation='horizontal', color=color_1, rwidth=bin_width)
    h2 = pyplot.hist(data_left, density=True,
                     bins=bins, orientation='horizontal', color=color_2, rwidth=bin_width)

    # Only plot the Y-axis
    frame.axes.get_xaxis().set_visible(True)
    frame.axes.get_yaxis().set_visible(True)

    # Remove any labels
    pyplot.xlabel('')
    pyplot.ylabel('')

    # Add the title if not None
    if title is not None:
        pyplot.title(title)

    # Adjust the patches
    for patch in h2[2]:
        patch.set_width(-patch.get_width())
    
    # Get the min and maximum values along the x-axis
    x_min = min([min(w.get_width() for w in h2[2]), min([w.get_width() for w in h1[2]])])
    x_max = max([max(w.get_width() for w in h2[2]), max([w.get_width() for w in h1[2]])])

    # Set the limits based on a given edge gap
    delta = edge_gap * (x_max - x_min)
    pyplot.xlim([x_min - delta, x_max + delta])

    # The central line
    pyplot.axvline(0.0)
    pyplot.axvline(linewidth=1, color=axvline_color)

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
# @plot_back2back_histograms
####################################################################################################
def plot_back2back_histograms_normalized(dists_directory,
                                         output_directory,
                                         hist_left,
                                         hist_right,
                                         output_prefix,
                                         title=None,
                                         invert=False,
                                         figure_width=5,
                                         figure_height=10,
                                         bins=40,
                                         color_1='red',
                                         color_2='blue',
                                         axvline_color='black',
                                         bin_width=0.9,
                                         save_pdf=False,
                                         save_svg=False,
                                         save_png=False,
                                         dpi=150,
                                         edge_gap=0.05):
    # Title
    if title is not None:
        print('\t* Plotting [%s]' % title)

    # Read the distributions
    data_left = utilities.read_dist_file('%s/%s' % (dists_directory, hist_left), invert=invert)
    data_right = utilities.read_dist_file('%s/%s' % (dists_directory, hist_right), invert=invert)

    # Clear figure, getting ready for a new figure
    pyplot.clf()

    # A new figure with the given dimensions size
    pyplot.figure(figsize=(figure_width, figure_height))
    pyplot.tight_layout()

    # Create a new frame for the plot to combine both
    frame = pyplot.gca()

    ry, rx = numpy.histogram(data_right, bins=bins)
    ly, lx = numpy.histogram(data_left, bins=bins)

    ry = ry / max(ry)
    ly = ly / max(ly)

    x_min = min(min(rx), min(lx))
    x_max = max(max(rx), max(lx))
    delta = x_max - x_min
    step = delta / bins
    bins = numpy.arange(x_min, x_max, step)

    # Right histogram
    pyplot.barh(bins, ry, color=color_1, height=step * bin_width)

    # Left histogram
    pyplot.barh(bins, -ly, color=color_2, height=step * bin_width)

    # Only plot the Y-axis
    frame.axes.get_xaxis().set_visible(False)
    frame.axes.get_yaxis().set_visible(True)

    # Remove any labels
    pyplot.xlabel('')
    pyplot.ylabel('')

    # Add the title if not None
    if title is not None:
        pyplot.title(title)

    # The central line
    pyplot.axvline(0.0)
    pyplot.axvline(linewidth=1, color=axvline_color)

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
# @plot_back2back_histograms
####################################################################################################
def plot_distributions(mesh_name,
                       dists_directory,
                       intermediate_directory):

    # Verify the packages
    utilities.verify_plotting_packages()

    # Loading the fonts
    nmv.interface.load_fonts()

    # The color palette
    palette = seaborn.color_palette("flare", n_colors=10)

    # List all the distributions in the file
    files = os.listdir(dists_directory)
    dists = list()
    for f in files:
        if '.dist' in f:
            dists.append(f)

    # Search strings
    strings = [['min-angle', 'Min. Dihedral Angle$^\circ$', False],
               ['max-angle', 'Max. Dihedral Angle$^\circ$', False],
               ['triangle-shape', 'Shape', False],
               ['radius-ratio', 'Radius Ratio', True],
               ['edge-ratio', 'Edge Ratio', True],
               ['radius-to-edge-ratio', 'Radius to Edge Ratio', True]]

    # Plot the distributions and store the images
    dists_pngs = list()
    for string in strings:
        dists_pngs.append(plot_back2back_histograms_normalized(
            dists_directory=dists_directory,
            output_directory=intermediate_directory,
            hist_left=utilities.search_for_dist(dists, 'input', string[0]),
            hist_right=utilities.search_for_dist(dists, 'watertight', string[0]),
            output_prefix=string[0],
            invert=string[2],
            title=string[1],
            color_1=palette[0], color_2=palette[5], axvline_color=palette[9],
            save_png=True))

    # Adjust the sizes to look nice
    utilities.create_adjusted_plot_images(
        input_directory=intermediate_directory, list_images=dists_pngs,
        output_directory=intermediate_directory)

    stats_image = utilities.montage_distributions_horizontally(
        name=mesh_name, input_directory=intermediate_directory, distribution_images=dists_pngs,
        output_directory=intermediate_directory)

    return stats_image













