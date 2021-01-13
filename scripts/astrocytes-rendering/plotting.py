####################################################################################################
# Copyright (c) 2021, EPFL / Blue Brain Project
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
import pandas
import matplotlib
import matplotlib.pyplot as pyplot
import matplotlib.font_manager
from matplotlib.ticker import PercentFormatter
from matplotlib.ticker import FormatStrFormatter
from PIL import Image


####################################################################################################
# Per-adjust all the plotting configuration
####################################################################################################
seaborn.set_style("whitegrid")
pyplot.rcParams['axes.grid'] = 'False'
pyplot.rcParams['font.family'] = 'NimbusSanL'
pyplot.rcParams['font.monospace'] = 'Regular'
pyplot.rcParams['font.style'] = 'normal'
pyplot.rcParams['axes.linewidth'] = 0.0
pyplot.rcParams['axes.labelsize'] = 30
pyplot.rcParams['axes.labelweight'] = 'bold'
pyplot.rcParams['xtick.labelsize'] = 30
pyplot.rcParams['ytick.labelsize'] = 30
pyplot.rcParams['legend.fontsize'] = 40
pyplot.rcParams['figure.titlesize'] = 40
pyplot.rcParams['axes.titlesize'] = 40
pyplot.rcParams['axes.edgecolor'] = '0.1'


####################################################################################################
# @get_image
####################################################################################################
def get_image(images,
              measure):
    for file in images:
        if measure in file:
            if '.png' in file:
                return file
    return None


####################################################################################################
# @get_largest_dimensions_of_all_images
####################################################################################################
def get_largest_dimensions_of_all_images(directory, images_list):

    widths = list()
    heights = list()
    for image in images_list:
        im = Image.open('%s/%s' % (directory, image))
        width, height = im.size
        widths.append(width)
        heights.append(height)
    return max(widths), max(heights)


####################################################################################################
# @verify_plotting_packages
####################################################################################################
def verify_plotting_packages():
    """Verifies that all the plotting packages are installed. Otherwise, install the missing one.
    """

    import matplotlib
    from matplotlib import font_manager

    # Import the fonts
    font_dirs = [os.path.dirname(os.path.realpath(__file__)) + '/fonts/']
    font_files = font_manager.findSystemFonts(fontpaths=font_dirs)
    font_list = font_manager.createFontList(font_files)
    font_manager.fontManager.ttflist.extend(font_list)


####################################################################################################
# @create_adjusted_plot_image
####################################################################################################
def create_adjusted_plot_image(image, input_directory, output_directory, new_width, new_height):

    # Get the width and height
    im = Image.open('%s/%s' % (input_directory, image))
    width, height = im.size

    new_size = (new_width, new_height)
    new_im = Image.new("RGB", new_size, (255, 255, 255))
    starting_y = new_height - height
    starting_x = new_width - width
    new_im.paste(im, (starting_x, starting_y))

    new_im.save('%s/%s' % (output_directory, image))


####################################################################################################
# @read_dist_file
####################################################################################################
def read_dist_file(file_path,
                   invert=False):
    """Reads the distribution file into a list.

    :param file_path:
        The path to the input file.
    :param invert:
        If set to True, invert the readed values.
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
# @create_adjusted_plot_images
####################################################################################################
def create_adjusted_plot_images(input_directory, list_images, output_directory):

    # Largest width
    largest_width, largest_height = get_largest_dimensions_of_all_images(input_directory,
                                                                         list_images)
    for image in list_images:
        create_adjusted_plot_image(
            image, input_directory, output_directory, largest_width, largest_height)


####################################################################################################
# @create_adjusted_plot_images
####################################################################################################
def montage_distributions_into_one_image(distribution_images,
                                         input_directory,
                                         output_directory):

    # Split them in two groups
    group_1 = list()
    group_2 = list()

    # Get the images one by one
    group_1.append(get_image(distribution_images, 'condition-number'))
    group_1.append(get_image(distribution_images, 'scaled-jacobian'))
    group_1.append(get_image(distribution_images, 'radius-ratio'))
    group_1.append(get_image(distribution_images, 'edge-ratio'))
    group_1.append(get_image(distribution_images, 'radius-to-edge-ratio'))
    group_2.append(get_image(distribution_images, 'min-angle'))
    group_2.append(get_image(distribution_images, 'max-angle'))
    group_2.append(get_image(distribution_images, 'relative-size'))
    group_2.append(get_image(distribution_images, 'triangle-shape'))
    group_2.append(get_image(distribution_images, 'triangle-shape-size'))

    total_width = 0
    total_height = 0

    # Get the dimensions from any image, all the images must have the same dimensions
    any_image = Image.open('%s/%s' % (input_directory, get_image(distribution_images, 'condition-number')))
    width, height = any_image.size

    total_width = width * 2
    total_height = height * 5

    new_im = Image.new('RGB', (total_width, total_height))
    for i, distribution_image in enumerate(group_1):
        im = Image.open('%s/%s' % (output_directory, distribution_image))
        new_im.paste(im, (0, i * height))

    for i, distribution_image in enumerate(group_2):
        im = Image.open('%s/%s' % (output_directory, distribution_image))
        new_im.paste(im, (width, i * height))

    new_im.save('%s/%s.png' % (output_directory, 'hola-vertical'))

    total_width = width * 5
    total_height = height * 2

    new_im = Image.new('RGB', (total_width, total_height))
    for i, distribution_image in enumerate(group_1):
        im = Image.open('%s/%s' % (output_directory, distribution_image))
        new_im.paste(im, (i * width, 0))

    for i, distribution_image in enumerate(group_2):
        im = Image.open('%s/%s' % (output_directory, distribution_image))
        new_im.paste(im, (i * width, height))

    new_im.save('%s/%s.png' % (output_directory, 'hola-horizontal'))

####################################################################################################
# @plot_distribution
####################################################################################################
def plot_distribution(input_directory,
                      dist_file,
                      output_directory,
                      title,
                      plot_titles=True,
                      xmax=100,
                      decimals=1,
                      kde=False,
                      color='b',
                      invert=False,
                      save_pdf=False,
                      save_svg=False):
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

    # Adjust the Y-axis format
    pyplot.gca().yaxis.set_major_formatter(PercentFormatter(xmax=xmax, decimals=decimals, symbol=' %'))

    # Adjusting the figure size
    pyplot.figure(figsize=(10, 10))

    # Set the title inside the figure to save some space
    if plot_titles:
        pyplot.title(title, y=0.9)

    # Plot the histogram
    seaborn.distplot(np_data, color='r', hist=True, kde=kde, norm_hist=True, bins=40,
                     hist_kws={"color": color, "lw": 0.5},
                     kde_kws={"color": color, "lw": 0.5})

    # Image prefix
    image_prefix = '%s/%s' % (output_directory, dist_file.replace('.dist', ''))

    # By default, save the figure into a PNG image
    pyplot.savefig(image_prefix + '.png', dpi=300, bbox_inches='tight')

    # Save PDF
    if save_pdf:
        pyplot.savefig(image_prefix + '.pdf', dpi=300, bbox_inches='tight')

    # Save SVG
    if save_svg:
        pyplot.savefig(image_prefix + '.svg', dpi=300, bbox_inches='tight')

    # Close figure to reset
    pyplot.close()

    # Return a reference to the png image
    return dist_file.replace('.dist', '.png')


####################################################################################################
# @plot_group
####################################################################################################
def plot_distributions(keyword,
                       distributions,
                       input_directory,
                       output_directory,
                       plot_titles=False,
                       use_kde=False):

    # Get the colormap
    colors = seaborn.color_palette("icefire", 10)

    # A list of all the distributions in .png format
    distributions_pngs = list()

    for distribution in distributions:
        if keyword in distribution:

            if 'condition-number' in distribution:
                distributions_pngs.append(plot_distribution(
                    input_directory, distribution, output_directory,
                    title='Condition Number', color=colors[0], kde=use_kde,
                    plot_titles=plot_titles))

            if 'radius-ratio' in distribution:
                distributions_pngs.append(plot_distribution(
                    input_directory, distribution, output_directory,
                    title='Radius Ratio', color=colors[1], kde=use_kde,
                    plot_titles=plot_titles, invert=True))

            if 'edge-ratio' in distribution:
                distributions_pngs.append(plot_distribution(
                    input_directory, distribution, output_directory,
                    title='Edge Ratio', color=colors[2], kde=use_kde,
                    plot_titles=plot_titles, invert=True))

            if 'radius-to-edge-ratio' in distribution:
                distributions_pngs.append(plot_distribution(
                    input_directory, distribution, output_directory,
                    title='Radius to Edge Ratio', color=colors[3], kde=use_kde,
                    plot_titles=plot_titles, invert=True))

            if 'min-angle' in distribution:
                distributions_pngs.append(plot_distribution(
                    input_directory, distribution, output_directory,
                    title='Min. Dihedral Angle (deg)', xmax=1, color=colors[4],
                    kde=use_kde, plot_titles=plot_titles))

            if 'max-angle' in distribution:
                distributions_pngs.append(plot_distribution(
                    input_directory, distribution, output_directory,
                    title='Max. Dihedral Angle (deg)', xmax=1, color=colors[5],
                    kde=use_kde, plot_titles=plot_titles))

            if 'relative-size' in distribution:
                distributions_pngs.append(plot_distribution(
                    input_directory, distribution, output_directory,
                    title='Relative Size', color=colors[6], kde=use_kde,
                    plot_titles=plot_titles))

            if 'triangle-shape' in distribution:
                distributions_pngs.append(plot_distribution(
                    input_directory, distribution, output_directory,
                    title='Shape', color=colors[7], kde=use_kde,
                    plot_titles=plot_titles))

            if 'triangle-shape-size' in distribution:
                distributions_pngs.append(plot_distribution(
                    input_directory, distribution, output_directory,
                    title='Shape & Size', color=colors[8], kde=use_kde,
                    plot_titles=plot_titles))

            if 'scaled-jacobian' in distribution:
                distributions_pngs.append(plot_distribution(
                    input_directory, distribution, output_directory,
                    title='Scaled Jacobian', color=colors[9], kde=use_kde,
                    plot_titles=plot_titles))

    # Return a reference to the images
    return distributions_pngs


####################################################################################################
# @plot_group
####################################################################################################
def plot_mesh_stats(distributions_directory,
                    output_directory):

    # Verify the packages
    verify_plotting_packages()

    # Get all the files in the distributions directory
    all_files = os.listdir(distributions_directory)

    # List all the distributions
    distributions = list()
    for f in all_files:
        if '.dist' in f:
            distributions.append(f)

    # Plot the distributions
    distributions_pngs = plot_distributions(
        keyword='.dist', distributions=distributions, input_directory=distributions_directory,
        output_directory=output_directory, plot_titles=True, use_kde=False)

    # Adjust the sizes to look nice
    create_adjusted_plot_images(input_directory=output_directory,
                                list_images=distributions_pngs,
                                output_directory=output_directory)

    montage_distributions_into_one_image(input_directory=output_directory,
                                         distribution_images=distributions_pngs,
                                         output_directory=output_directory)


