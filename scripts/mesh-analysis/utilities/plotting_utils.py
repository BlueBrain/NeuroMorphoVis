####################################################################################################
# Copyright (c) 2020 - 2021, EPFL / Blue Brain Project
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

# Blender imports
import bpy

# Internal imports
import nmv.scene

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

# Internal
import mesh_analysis
import geometry_utils

####################################################################################################
# Per-adjust all the plotting configuration
####################################################################################################
font_size = 42
seaborn.set_style("whitegrid")
pyplot.rcParams['axes.grid'] = 'True'
pyplot.rcParams['grid.linestyle'] = '--'
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
# @get_image
####################################################################################################
def get_image(images,
              measure):
    """Gets an image with a specific measure in the file name.

    :param images:
        A list of images.
    :param measure:
        Search keyword.
    :return:
        The result.
    """
    for file in images:
        if measure in file:
            if '.png' in file:
                return file
    return None


####################################################################################################
# @get_largest_dimensions_of_all_images
####################################################################################################
def get_largest_dimensions_of_all_images(directory,
                                         images_list):
    """Gets the largest dimension of a set of images.

    :param directory:
        The directory that contains the images.
    :param images_list:
        A list of all the images.
    :return:
        The largest dimension of all images.
    """

    # Lists
    widths = list()
    heights = list()

    # Compute ...
    for image in images_list:
        im = Image.open('%s/%s' % (directory, image))
        width, height = im.size
        widths.append(width)
        heights.append(height)

    # Return the largest
    return max(widths), max(heights)


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
# @create_adjusted_plot_image
####################################################################################################
def create_adjusted_plot_image(image,
                               input_directory,
                               output_directory,
                               new_width,
                               new_height):
    """Creates a new image (corresponding to a graph) to match the sizes.

    :param image:
        An input image.
    :param input_directory:
        The directory that contains the image.
    :param output_directory:
        The results directory.
    :param new_width:
        The new width of the image.
    :param new_height:
        The new height of the image.
    """

    # Get the width and height
    im = Image.open('%s/%s' % (input_directory, image))
    width, height = im.size

    # New image
    new_size = (new_width, new_height)
    new_im = Image.new("RGB", new_size, (255, 255, 255))
    starting_y = new_height - height
    starting_x = new_width - width
    new_im.paste(im, (starting_x, starting_y))

    # Save it
    new_im.save('%s/%s' % (output_directory, image))
    new_im.close()
    im.close()


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
# @create_adjusted_plot_images
####################################################################################################
def create_adjusted_plot_images(input_directory,
                                list_images,
                                output_directory):
    """Create the images with adjusted dimensions.

    :param input_directory:
        The directory that contains all the images.
    :param list_images:
        A list of images to be adjusted.
    :param output_directory:
        The results directory.
    """

    # Largest width
    largest_width, largest_height = get_largest_dimensions_of_all_images(input_directory,
                                                                         list_images)
    for image in list_images:
        create_adjusted_plot_image(
            image, input_directory, output_directory, largest_width, largest_height)


####################################################################################################
# @create_adjusted_plot_images
####################################################################################################
def montage_important_distributions_into_one_image(name,
                                                   distribution_images,
                                                   input_directory,
                                                   output_directory,
                                                   delta=100):
    """Montages the important distributions into a single image.

    :param name:
        Final image name.
    :param distribution_images:
        A list of all the distribution images.
    :param input_directory:
        Directory containing images.
    :param output_directory:
        Results directory.
    :param delta:
        Delta between the images, default 100.
    :return:
    """
    # Split them in two groups
    group_1 = list()
    group_2 = list()

    # Get the images one by one

    group_1.append(get_image(distribution_images, 'min-angle'))
    group_1.append(get_image(distribution_images, 'max-angle'))
    group_1.append(get_image(distribution_images, 'triangle-shape'))

    group_2.append(get_image(distribution_images, 'radius-ratio'))
    group_2.append(get_image(distribution_images, 'edge-ratio'))
    group_2.append(get_image(distribution_images, 'radius-to-edge-ratio'))

    # Get the dimensions from any image, all the images must have the same dimensions
    any_image = Image.open('%s/%s' % (input_directory, get_image(distribution_images, 'min-angle')))
    width, height = any_image.size

    # Vertical
    # Compute the dimensions of the new image
    total_width = (width * 2) + (delta * 1)
    total_height = (height * 3) + (delta * 2)

    new_im = Image.new('RGB', (total_width, total_height), (255, 255, 255))
    for i, distribution_image in enumerate(group_1):
        im = Image.open('%s/%s' % (output_directory, distribution_image))
        h = 0 if i == 0 else i * (height + delta)
        new_im.paste(im, (0, h))

    for i, distribution_image in enumerate(group_2):
        im = Image.open('%s/%s' % (output_directory, distribution_image))
        h = 0 if i == 0 else i * (height + delta)
        new_im.paste(im, (width + delta, h))

    vertical_image_path = '%s/%s-vertical.png' % (output_directory, name)
    new_im.save(vertical_image_path)

    # Horizontal
    # Compute the dimensions of the new image
    total_width = (width * 3) + (delta * 2)
    total_height = height * 2 + (delta * 1)

    new_im = Image.new('RGB', (total_width, total_height), (255, 255, 255))
    for i, distribution_image in enumerate(group_1):
        im = Image.open('%s/%s' % (output_directory, distribution_image))
        w = 0 if i == 0 else i * (width + delta)
        new_im.paste(im, (w, 0))

    for i, distribution_image in enumerate(group_2):
        im = Image.open('%s/%s' % (output_directory, distribution_image))
        w = 0 if i == 0 else i * (width + delta)
        new_im.paste(im, (w, height + delta))

    horizontal_image_path = '%s/%s-horizontal.png' % (output_directory, name)
    new_im.save(horizontal_image_path)

    # Return reference to the vertical and horizontal images
    return vertical_image_path, horizontal_image_path


####################################################################################################
# @create_adjusted_plot_images
####################################################################################################
def montage_distributions_into_one_image(name,
                                         distribution_images,
                                         input_directory,
                                         output_directory,
                                         delta=100):

    # Split them in two groups
    group_1 = list()
    group_2 = list()

    # Get the images one by one

    group_1.append(get_image(distribution_images, 'min-angle'))
    group_1.append(get_image(distribution_images, 'radius-ratio'))
    group_1.append(get_image(distribution_images, 'radius-to-edge-ratio'))
    group_1.append(get_image(distribution_images, 'relative-size'))

    group_2.append(get_image(distribution_images, 'max-angle'))
    group_2.append(get_image(distribution_images, 'edge-ratio'))
    group_2.append(get_image(distribution_images, 'triangle-shape'))
    group_2.append(get_image(distribution_images, 'scaled-jacobian'))

    # group_1.append(get_image(distribution_images, 'condition-number'))
    # group_2.append(get_image(distribution_images, 'triangle-size-shape'))

    # Get the dimensions from any image, all the images must have the same dimensions
    any_image = Image.open('%s/%s' % (input_directory, get_image(distribution_images, 'min-angle')))
    width, height = any_image.size

    # Vertical
    # Compute the dimensions of the new image
    total_width = (width * 2) + (delta * 1)
    total_height = (height * 4) + (delta * 3)

    new_im = Image.new('RGB', (total_width, total_height), (255, 255, 255))
    for i, distribution_image in enumerate(group_1):
        im = Image.open('%s/%s' % (output_directory, distribution_image))
        h = 0 if i == 0 else i * (height + delta)
        new_im.paste(im, (0, h))

    for i, distribution_image in enumerate(group_2):
        im = Image.open('%s/%s' % (output_directory, distribution_image))
        h = 0 if i == 0 else i * (height + delta)
        new_im.paste(im, (width + delta, h))

    vertical_image_path = '%s/%s-vertical.png' % (output_directory, name)
    new_im.save(vertical_image_path)

    # Horizontal
    # Compute the dimensions of the new image
    total_width = (width * 4) + (delta * 3)
    total_height = height * 2 + (delta * 1)

    new_im = Image.new('RGB', (total_width, total_height), (255, 255, 255))
    for i, distribution_image in enumerate(group_1):
        im = Image.open('%s/%s' % (output_directory, distribution_image))
        w = 0 if i == 0 else i * (width + delta)
        new_im.paste(im, (w, 0))

    for i, distribution_image in enumerate(group_2):
        im = Image.open('%s/%s' % (output_directory, distribution_image))
        w = 0 if i == 0 else i * (width + delta)
        new_im.paste(im, (w, height + delta))

    horizontal_image_path = '%s/%s-horizontal.png' % (output_directory, name)
    new_im.save(horizontal_image_path)

    # Return reference to the vertical and horizontal images
    return vertical_image_path, horizontal_image_path


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

    # Adjusting the figure size
    pyplot.figure(figsize=(10, 5))
    pyplot.tight_layout()

    # Set the title inside the figure to save some space
    if plot_titles:
        pyplot.title(title, y=1.05)

    # Plot the histogram
    ax = seaborn.histplot(np_data, color=color, bins=40, alpha=0.95, stat="probability")

    # Formatters
    pyplot.gca().yaxis.set_major_formatter(
        PercentFormatter(xmax=xmax, decimals=decimals, symbol='%'))
    pyplot.gca().xaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:2.2f}'.format(y)))

    # No label
    pyplot.ylabel('')

    # Adjust the Y-axis format
    ax.set_xticks(major_ticks)

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

            if 'min-angle' in distribution:
                c = colors[0]
                distributions_pngs.append(plot_distribution(
                    input_directory, distribution, output_directory,
                    title='Min. Dihedral Angle$^\circ$', xmax=1, color=c,
                    kde=use_kde, plot_titles=plot_titles))

            if 'max-angle' in distribution:
                c = colors[1]
                distributions_pngs.append(plot_distribution(
                    input_directory, distribution, output_directory,
                    title='Max. Dihedral Angle$^\circ$', xmax=1, color=c,
                    kde=use_kde, plot_titles=plot_titles))

            if 'triangle-shape' in distribution:
                c = colors[2]
                distributions_pngs.append(plot_distribution(
                    input_directory, distribution, output_directory,
                    title='Shape', color=c, kde=use_kde,
                    plot_titles=plot_titles))

            if 'radius-ratio' in distribution:
                c = colors[3]
                distributions_pngs.append(plot_distribution(
                    input_directory, distribution, output_directory,
                    title='Radius Ratio', color=c, kde=use_kde,
                    plot_titles=plot_titles, invert=True))

            if 'edge-ratio' in distribution:
                c = colors[4]
                distributions_pngs.append(plot_distribution(
                    input_directory, distribution, output_directory,
                    title='Edge Ratio', color=c, kde=use_kde,
                    plot_titles=plot_titles, invert=True))

            if 'radius-to-edge-ratio' in distribution:
                c = colors[5]
                distributions_pngs.append(plot_distribution(
                    input_directory, distribution, output_directory,
                    title='Radius to Edge Ratio', color=c, kde=use_kde,
                    plot_titles=plot_titles, invert=True))

            if 'relative-size' in distribution:
                c = colors[5]
                distributions_pngs.append(plot_distribution(
                    input_directory, distribution, output_directory,
                    title='Relative Size', color=c, kde=use_kde,
                    plot_titles=plot_titles))

            if 'scaled-jacobian' in distribution:
                c = colors[5]
                distributions_pngs.append(plot_distribution(
                    input_directory, distribution, output_directory,
                    title='Scaled Jacobian', color=c, kde=use_kde,
                    plot_titles=plot_titles))

    # Return a reference to the images
    return distributions_pngs


####################################################################################################
# @get_super
####################################################################################################
def get_super(x):

    normal = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-=()"
    super_s = "ᴬᴮᶜᴰᴱᶠᴳᴴᴵᴶᴷᴸᴹᴺᴼᴾQᴿˢᵀᵁⱽᵂˣʸᶻᵃᵇᶜᵈᵉᶠᵍʰᶦʲᵏˡᵐⁿᵒᵖ۹ʳˢᵗᵘᵛʷˣʸᶻ⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾"
    res = x.maketrans(''.join(normal), ''.join(super_s))
    return x.translate(res)


####################################################################################################
# @format_number_to_power_string
####################################################################################################
def format_number_to_power_string(number):
    """Formats the string to make it readable.

    :param number:
        Input number.
    :return:
        Corresponding string.
    """

    if float(number) < 1e3:
        return '%2.2f' % number
    elif (float(number) > 1e3) and (float(number) < 1e6):
        value = float(number) / float(1e3)
        return '%2.2f x10%s' % (value, get_super('3'))
    elif (float(number) > 1e6) and (float(number) < 1e9):
        value = float(number) / float(1e6)
        return '%2.2f x10%s' % (value, get_super('6'))
    elif (float(number) > 1e9) and (float(number) < 1e12):
        value = float(number) / float(1e9)
        return "%2.2f x10%s" % (value, get_super('9'))
    else:
        value = float(number) / float(1e12)
        return '%2.2f x10%s' % (value, get_super('12'))


####################################################################################################
# @create_mesh_fact_sheet
####################################################################################################
def create_mesh_fact_sheet(mesh_object,
                           mesh_name,
                           output_image_path,
                           image_resolution=1500,
                           mesh_scale=1):
    """Creates the fact sheet of the mesh into an image.

    :param mesh_object:
        A given mesh object in Blender.
    :param mesh_name:
        The name of the mesh.
    :param output_image_path:
        The output path.
    :param image_resolution:
        The resolution of the image.
    :return:
        The path to the image.
    """

    print('  * Computing Mesh Fact Sheet')

    # Set the current object to be the active object
    nmv.scene.set_active_object(mesh_object)

    # Compute the bounding box
    mesh_bbox = mesh_analysis.compute_bounding_box(mesh_object)

    print('\t* Number Partitions')
    number_partitions = mesh_analysis.compute_number_partitions(mesh_object)

    # Switch to geometry or edit mode from the object mode
    bpy.ops.object.editmode_toggle()

    # Convert the mesh into a bmesh
    bm = geometry_utils.convert_from_mesh_object(mesh_object)

    # Compute the surface area
    print('\t* Surface Area')
    surface_area = mesh_analysis.compute_surface_area(bm)

    # Compute the volume
    print('\t* Volume')
    volume = mesh_analysis.compute_volume(bm)

    # Compute the number of polygons
    print('\t* Number Polygons')
    polygons = mesh_analysis.compute_number_polygons(bm)

    # Compute the number of vertices
    print('\t* Number Vertices')
    vertices = mesh_analysis.compute_number_vertices(bm)

    # Is it watertight
    print('\t* Validating Watertightness')
    watertight_check = mesh_analysis.check_watertightness(bm, number_partitions)

    # Free the bmesh
    bm.free()

    # Switch to geometry or edit mode from the object mode
    bpy.ops.object.editmode_toggle()

    # We have 12 entries in the image
    number_entries = 14

    # Image dimensions
    image_width = int(image_resolution * 1.15)
    image_height = image_resolution

    # Calculate the spacing between items
    spacing = int(image_height / (number_entries * 1.2))

    # Create stats. image
    fact_sheet_image = Image.new("RGB", (image_width, image_height),
                                 (255, 255, 255))

    # Create a drawing area
    drawing_area = ImageDraw.Draw(fact_sheet_image)

    # Select a font
    font_path = os.path.dirname(os.path.realpath(__file__)) + '/fonts/1H.otf'
    font = ImageFont.truetype(font_path, int(spacing * 0.8))
    footnote_font = ImageFont.truetype(font_path, int(spacing * 0.45))

    # Compute the offsets
    starting_x = int(0.04 * image_width)
    delta_x = starting_x + int(image_width * 0.65)

    i = 0.4
    delta_y = i * spacing
    drawing_area.text((starting_x, delta_y), 'Number of Polygons', font=font, fill=(0, 0, 0))
    drawing_area.text((delta_x, delta_y), f'{polygons:,d}', font=font, fill=(0, 0, 0))

    i += 1
    delta_y = i * spacing
    drawing_area.text((starting_x, delta_y), 'Number of Vertices', font=font, fill=(0, 0, 0))
    drawing_area.text((delta_x, delta_y), f'{vertices:,d}', font=font, fill=(0, 0, 0))

    i += 1.5
    delta_y = i * spacing
    drawing_area.text((starting_x, delta_y), 'Bounding Box Width', font=font, fill=(0, 0, 0))
    drawing_area.text((delta_x, delta_y), '%s μm' % format_number_to_power_string(
        mesh_bbox.x * mesh_scale), font=font, fill=(0, 0, 0))

    i += 1
    delta_y = i * spacing
    drawing_area.text((starting_x, delta_y), 'Bounding Box Height', font=font, fill=(0, 0, 0))
    drawing_area.text((delta_x, delta_y), '%s μm' % format_number_to_power_string(
        mesh_bbox.y * mesh_scale), font=font, fill=(0, 0, 0))
    i += 1
    delta_y = i * spacing
    drawing_area.text((starting_x, delta_y), 'Bounding Box Depth', font=font, fill=(0, 0, 0))
    drawing_area.text((delta_x, delta_y), '%s μm' % format_number_to_power_string(
        mesh_bbox.z * mesh_scale), font=font, fill=(0, 0, 0))

    i += 1.0
    delta_y = i * spacing
    drawing_area.text((starting_x, delta_y), 'Bounding Box Diagonal', font=font, fill=(0, 0, 0))
    drawing_area.text((delta_x, delta_y), '%s μm' % format_number_to_power_string(
        mesh_bbox.diagonal * mesh_scale), font=font, fill=(0, 0, 0))

    i += 1.5
    delta_y = i * spacing
    drawing_area.text((starting_x, delta_y), 'Total Surface Area', font=font, fill=(0, 0, 0))
    drawing_area.text((delta_x, delta_y), '%s μm²' % format_number_to_power_string(
        surface_area * mesh_scale * mesh_scale), font=font, fill=(0, 0, 0))

    i += 1
    delta_y = i * spacing
    drawing_area.text((starting_x, delta_y), 'Total Volume*', font=font, fill=(0, 0, 0))
    drawing_area.text((delta_x, delta_y), '%s μm³' % format_number_to_power_string(
        volume * mesh_scale * mesh_scale * mesh_scale), font=font, fill=(0, 0, 0))

    i += 1.5
    delta_y = i * spacing
    drawing_area.text((starting_x, delta_y), 'Number of Mesh Partitions',
                      font=font, fill=(0, 0, 0))
    drawing_area.text((delta_x, delta_y), f'{number_partitions:,d}',
                      font=font, fill=(0, 0, 0))

    i += 1.5
    delta_y = i * spacing
    drawing_area.text((starting_x, delta_y), 'Number of Non Manifold Edges',
                      font=font, fill=(0, 0, 0))
    drawing_area.text((delta_x, delta_y), f'{watertight_check.non_manifold_edges:,d}',
                      font=font, fill=(0, 0, 0))

    i += 1
    delta_y = i * spacing
    drawing_area.text((starting_x, delta_y), 'Number of Non Manifold Vertices',
                      font=font, fill=(0, 0, 0))
    drawing_area.text((delta_x, delta_y), f'{watertight_check.non_manifold_vertices:,d}',
                      font=font, fill=(0, 0, 0))

    i += 1
    delta_y = i * spacing
    drawing_area.text((starting_x, delta_y), 'Number of Non Continuous Edges',
                      font=font, fill=(0, 0, 0))
    drawing_area.text((delta_x, delta_y), f'{watertight_check.non_contiguous_edge:,d}',
                      font=font, fill=(0, 0, 0))

    i += 1
    delta_y = i * spacing
    drawing_area.text((starting_x, delta_y), 'Number of Self Intersections',
                      font=font, fill=(0, 0, 0))
    drawing_area.text((delta_x, delta_y), f'{watertight_check.self_intersections:,d}',
                      font=font, fill=(0, 0, 0))

    i += 1.5
    delta_y = i * spacing
    drawing_area.text((starting_x, delta_y), 'Watertight', font=font, fill=(0, 0, 0))
    drawing_area.text((delta_x, delta_y), 'Yes' if watertight_check.watertight else 'No',
                      font=font, fill=(0, 0, 0))

    fact_sheet_image_path = '%s/%s-fact-sheet.png' % (output_image_path, mesh_name)
    fact_sheet_image.save(fact_sheet_image_path)
    fact_sheet_image.close()
    return fact_sheet_image_path


####################################################################################################
# @plot_mesh_stats
####################################################################################################
def plot_mesh_stats(name,
                    distributions_directory,
                    output_directory,
                    color):
    """Plots the stats of the mesh.

    :param name:
        Image name.
    :param distributions_directory:
        The directory that contains all the distributions.
    :param output_directory:
        Results directory.
    :param color:
        Distributions color.
    :return:
        Resulting images
    """

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
        output_directory=output_directory, plot_titles=True, use_kde=False, color=color)

    # Adjust the sizes to look nice
    create_adjusted_plot_images(input_directory=output_directory,
                                list_images=distributions_pngs,
                                output_directory=output_directory)

    vertical_image, horizontal_image = montage_important_distributions_into_one_image(
        name=name, input_directory=output_directory, distribution_images=distributions_pngs,
        output_directory=output_directory)

    return vertical_image, horizontal_image


####################################################################################################
# @combine_stats_with_rendering
####################################################################################################
def combine_stats_with_rendering(rendering_image,
                                 vertical_stats_image,
                                 horizontal_stats_image,
                                 output_image_path,
                                 delta=50):
    """Creates a final image with the mesh and the stats. next to it.

    :param rendering_image:
        The image of the astrocyte mesh.
    :param vertical_stats_image:
        The vertical stats. image.
    :param horizontal_stats_image:
        The horizontal stats. image.
    :param output_image_path:
        The path to the output directory.
    :param delta:
        Distance between main figure and stats.
    :return:
        A reference to the combined vertical and horizontal images.
    """

    # Open the images
    rendering_im = Image.open(rendering_image)
    horizontal_im = Image.open(horizontal_stats_image)
    vertical_im = Image.open(vertical_stats_image)

    # Compute the ratios for the horizontal image and scale it
    horizontal_image_ratio = rendering_im.size[1] / (1.0 * horizontal_im.size[1])
    horizontal_im_width = int(horizontal_im.size[0] * horizontal_image_ratio)
    horizontal_im_height = rendering_im.size[1]
    horizontal_im = horizontal_im.resize((horizontal_im_width, horizontal_im_height), resample=2)

    # Compute the ratios for the vertical image and scale it
    vertical_image_ratio = rendering_im.size[1] / (1.0 * vertical_im.size[1])
    vertical_im_width = int(vertical_im.size[0] * vertical_image_ratio)
    vertical_im_height = rendering_im.size[1]
    vertical_im = vertical_im.resize((vertical_im_width, vertical_im_height), resample=2)

    # Create the combined horizontal image
    new_horizontal_im = Image.new('RGB', (rendering_im.size[0] + horizontal_im.size[0] + delta,
                                          rendering_im.size[1]), (255, 255, 255))
    new_horizontal_im.paste(rendering_im, (0, 0))
    new_horizontal_im.paste(horizontal_im, (rendering_im.size[0] + delta, 0))
    combined_horizontal_path = '%s-horizontal.png' % output_image_path
    new_horizontal_im.save(combined_horizontal_path)
    new_horizontal_im.close()

    # Create the vertical image
    new_vertical_im = Image.new('RGB', (rendering_im.size[0] + vertical_im.size[0] + delta,
                                        rendering_im.size[1]), (255, 255, 255))
    new_vertical_im.paste(rendering_im, (0, 0))
    new_vertical_im.paste(vertical_im, (rendering_im.size[0] + delta, 0))
    combined_vertical_path = '%s-vertical.png' % output_image_path
    new_vertical_im.save(combined_vertical_path)
    new_vertical_im.close()

    # Close all the images
    rendering_im.close()
    vertical_im.close()
    horizontal_im.close()

    # Return a reference to the final images
    return combined_vertical_path, combined_horizontal_path





