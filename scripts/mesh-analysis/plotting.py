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

# Blender imports
import bpy
import bmesh

# Internal imports
import nmv.scene

# System imports
import os
import numpy
import seaborn
import pandas
import matplotlib
import matplotlib.pyplot as pyplot
import matplotlib.font_manager as font_manager
import matplotlib.ticker
import colorsys
from matplotlib.ticker import PercentFormatter
from matplotlib.ticker import FormatStrFormatter
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import core

####################################################################################################
# Per-adjust all the plotting configuration
####################################################################################################
seaborn.set_style("whitegrid")
pyplot.rcParams['axes.grid'] = 'True'
pyplot.rcParams['grid.linestyle'] = '-'
pyplot.rcParams['grid.linewidth'] = 2
pyplot.rcParams['font.family'] = 'NimbusSanL'
#pyplot.rcParams['font.family'] = 'Helvetica LT Std'
pyplot.rcParams['font.monospace'] = 'Bold'
pyplot.rcParams['font.style'] = 'normal'
pyplot.rcParams['axes.linewidth'] = 0.0
pyplot.rcParams['axes.labelsize'] = 50
pyplot.rcParams['axes.labelweight'] = 'bold'
pyplot.rcParams['xtick.labelsize'] = 50
pyplot.rcParams['ytick.labelsize'] = 50
pyplot.rcParams['legend.fontsize'] = 50
pyplot.rcParams['figure.titlesize'] = 50
pyplot.rcParams['axes.titlesize'] = 50
pyplot.rcParams['xtick.major.pad'] = '20'
pyplot.rcParams['ytick.major.pad'] = '12'
pyplot.rcParams['axes.edgecolor'] = '1'


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
def montage_important_distributions_into_one_image(name,
                                                   distribution_images,
                                                   input_directory,
                                                   output_directory,
                                                   delta=100):

    # Split them in two groups
    group_1 = list()

    # Get the images one by one
    group_1.append(get_image(distribution_images, 'min-angle'))
    group_1.append(get_image(distribution_images, 'max-angle'))
    group_1.append(get_image(distribution_images, 'radius-ratio'))
    group_1.append(get_image(distribution_images, 'edge-ratio'))
    group_1.append(get_image(distribution_images, 'radius-to-edge-ratio'))

    # group_1.append(get_image(distribution_images, 'relative-size'))
    # group_2.append(get_image(distribution_images, 'triangle-shape'))
    # group_2.append(get_image(distribution_images, 'scaled-jacobian'))

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

    vertical_image_path = '%s/%s-vertical.png' % (output_directory, name)
    new_im.save(vertical_image_path)

    # Horizontal
    # Compute the dimensions of the new image
    total_width = (width * 5) + (delta * 4)
    total_height = height

    new_im = Image.new('RGB', (total_width, total_height), (255, 255, 255))
    for i, distribution_image in enumerate(group_1):
        im = Image.open('%s/%s' % (output_directory, distribution_image))
        w = 0 if i == 0 else i * (width + delta)
        new_im.paste(im, (w, 0))

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
                      decimals=1,
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
    pyplot.figure(figsize=(10, 10))

    # Set the title inside the figure to save some space
    if plot_titles:
        pyplot.title(title, y=1.0)

    # Plot the histogram
    seaborn.distplot(np_data, color='r', hist=True, kde=kde, norm_hist=True, bins=40,
                     hist_kws={"color": color, "lw": 0.5},
                     kde_kws={"color": color, "lw": 0.5})

    # Percent formatter
    pyplot.gca().yaxis.set_major_formatter(
        PercentFormatter(xmax=xmax, decimals=decimals, symbol='%'))

    # Adjust the Y-axis format
    pyplot.gca().xaxis.set_major_locator(pyplot.MaxNLocator(4))
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
def lighten_color(color, amount=1.0):
    """Lightens the given color by multiplying (1-luminosity) by the given amount.
    Input can be matplotlib color string, hex string, or RGB tuple.
    """

    try:
        actual_color = matplotlib.colors.cnames[color]
    except:
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

    # Get the colormap
    colors = seaborn.color_palette("brg", 10)

    # A list of all the distributions in .png format
    distributions_pngs = list()

    for distribution in distributions:
        if keyword in distribution:

            if 'min-angle' in distribution:
                distributions_pngs.append(plot_distribution(
                    input_directory, distribution, output_directory,
                    title='Min. Dihedral Angle$^\circ$', xmax=1, color=color,
                    kde=use_kde, plot_titles=plot_titles))

            if 'max-angle' in distribution:
                distributions_pngs.append(plot_distribution(
                    input_directory, distribution, output_directory,
                    title='Max. Dihedral Angle$^\circ$', xmax=1, color=color,
                    kde=use_kde, plot_titles=plot_titles))

            if 'radius-ratio' in distribution:
                distributions_pngs.append(plot_distribution(
                    input_directory, distribution, output_directory,
                    title='Radius Ratio', color=color, kde=use_kde,
                    plot_titles=plot_titles, invert=True))

            if 'edge-ratio' in distribution:
                distributions_pngs.append(plot_distribution(
                    input_directory, distribution, output_directory,
                    title='Edge Ratio', color=color, kde=use_kde,
                    plot_titles=plot_titles, invert=True))

            if 'radius-to-edge-ratio' in distribution:
                distributions_pngs.append(plot_distribution(
                    input_directory, distribution, output_directory,
                    title='Radius to Edge Ratio', color=color, kde=use_kde,
                    plot_titles=plot_titles, invert=True))

            if 'triangle-shape' in distribution:
                distributions_pngs.append(plot_distribution(
                    input_directory, distribution, output_directory,
                    title='Shape', color=color, kde=use_kde,
                    plot_titles=plot_titles))

            if 'relative-size' in distribution:
                distributions_pngs.append(plot_distribution(
                    input_directory, distribution, output_directory,
                    title='Relative Size', color=color, kde=use_kde,
                    plot_titles=plot_titles))

            if 'scaled-jacobian' in distribution:
                distributions_pngs.append(plot_distribution(
                    input_directory, distribution, output_directory,
                    title='Scaled Jacobian', color=color, kde=use_kde,
                    plot_titles=plot_titles))

    # Return a reference to the images
    return distributions_pngs


####################################################################################################
# @create_mesh_statistics_image
####################################################################################################
def create_mesh_statistics_image(mesh_object, mesh_name, output_image_path, image_resolution=1500):

    # Set the current object to be the active object
    nmv.scene.set_active_object(mesh_object)

    # Compute the bounding box
    mesh_bbox = core.compute_bounding_box(mesh_object)

    print('\tNumber Partitions')
    number_partitions = core.compute_number_partitions(mesh_object)

    # Switch to geometry or edit mode from the object mode
    bpy.ops.object.editmode_toggle()

    # Convert the mesh into a bmesh
    bm = core.convert_from_mesh_object(mesh_object)

    # Compute the surface area
    print('\tSurface Area')
    surface_area = core.compute_surface_area(bm)

    # Compute the volume
    print('\tVolume')
    volume = core.compute_volume(bm)

    # Compute the number of polygons
    print('\tNumber Polygons')
    polygons = core.compute_number_polygons(bm)

    # Compute the number of vertices
    print('\tVertices')
    vertices = core.compute_number_vertices(bm)

    # Is it watertight
    print('\tWatertightness')
    watertight_check = core.check_watertightness(bm)

    # Free the bmesh
    bm.free()

    # Switch to geometry or edit mode from the object mode
    bpy.ops.object.editmode_toggle()

    # We have 12 entries in the image
    number_entries = 13

    # Image dimensions
    image_width = int(image_resolution / 0.6)
    image_height = image_resolution

    # Calculate the spacing between items
    spacing = int(image_width / (number_entries * 1.0 * 2.0))

    # Create stats. image
    statistics_image = Image.new("RGB", (image_width, image_height),
                                 (255, 255, 255))

    # Create a drawing area
    drawing_area = ImageDraw.Draw(statistics_image)

    # Select a font
    font = ImageFont.truetype(
        '/ssd1/blender/bluebrain-blender-2.82/blender-neuromorphovis/2.82/scripts/addons/neuromorphovis/scripts/mesh-analysis/fonts/NimbusSanL-Bold.ttf',
        int(spacing * 0.8))

    # Compute the offsets
    starting_x = int(0.05 * image_width)
    delta_x = starting_x + int(image_width * 0.54)

    i = 0.8
    delta_y = i * spacing
    drawing_area.text((starting_x, delta_y), 'Number of Polygons', font=font, fill=(0, 0, 0))
    drawing_area.text((delta_x, delta_y), '%d' % polygons, font=font, fill=(0, 0, 0))

    i += 1
    delta_y = i * spacing
    drawing_area.text((starting_x, delta_y), 'Number of Vertices', font=font, fill=(0, 0, 0))
    drawing_area.text((delta_x, delta_y), '%d' % vertices, font=font, fill=(0, 0, 0))

    i += 1.5
    delta_y = i * spacing
    drawing_area.text((starting_x, delta_y), 'Bounding Box Dimensions', font=font, fill=(0, 0, 0))
    drawing_area.text((delta_x, delta_y),
                      '%2.2f x %2.2f x %2.2f' % (mesh_bbox.x, mesh_bbox.y, mesh_bbox.z),
                      font=font, fill=(0, 0, 0))

    i += 1
    delta_y = i * spacing
    drawing_area.text((starting_x, delta_y), 'Bounding Box Diagonal', font=font, fill=(0, 0, 0))
    drawing_area.text((delta_x, delta_y), '%f' % mesh_bbox.diagonal, font=font, fill=(0, 0, 0))

    i += 1.5
    delta_y = i * spacing
    drawing_area.text((starting_x, delta_y), 'Total Surface Area', font=font, fill=(0, 0, 0))
    drawing_area.text((delta_x, delta_y), '%f' % surface_area, font=font, fill=(0, 0, 0))

    i += 1
    delta_y = i * spacing
    drawing_area.text((starting_x, delta_y), 'Total Volume', font=font, fill=(0, 0, 0))
    drawing_area.text((delta_x, delta_y), '%f' % volume, font=font, fill=(0, 0, 0))

    i += 1.5
    delta_y = i * spacing
    drawing_area.text((starting_x, delta_y), 'Watertight', font=font, fill=(0, 0, 0))
    drawing_area.text((delta_x, delta_y), str(watertight_check.watertight),
                      font=font, fill=(0, 0, 0))

    i += 1.5
    delta_y = i * spacing
    drawing_area.text((starting_x, delta_y), 'Number of Mesh Partitions',
                      font=font, fill=(0, 0, 0))
    drawing_area.text((delta_x, delta_y), '%d' % number_partitions,
                      font=font, fill=(0, 0, 0))

    i += 1.0
    delta_y = i * spacing
    drawing_area.text((starting_x, delta_y), 'Number of Non Manifold Edges',
                      font=font, fill=(0, 0, 0))
    drawing_area.text((delta_x, delta_y), '%d' % watertight_check.non_manifold_edges,
                      font=font, fill=(0, 0, 0))

    i += 1
    delta_y = i * spacing
    drawing_area.text((starting_x, delta_y), 'Number of Non Manifold Vertices',
                      font=font, fill=(0, 0, 0))
    drawing_area.text((delta_x, delta_y), '%d' % watertight_check.non_manifold_vertices,
                      font=font, fill=(0, 0, 0))

    i += 1
    delta_y = i * spacing
    drawing_area.text((starting_x, delta_y), 'Number of Non Continuous Edges',
                      font=font, fill=(0, 0, 0))
    drawing_area.text((delta_x, delta_y), '%d' % watertight_check.non_contiguous_edge,
                      font=font, fill=(0, 0, 0))

    i += 1
    delta_y = i * spacing
    drawing_area.text((starting_x, delta_y), 'Number of Self Intersections',
                      font=font, fill=(0, 0, 0))
    drawing_area.text((delta_x, delta_y), '%d' % watertight_check.self_intersections,
                      font=font, fill=(0, 0, 0))

    stats_image_path = '%s/%s-blender-stats.png' % (output_image_path, mesh_name)
    statistics_image.save(stats_image_path)
    return stats_image_path


####################################################################################################
# @plot_mesh_stats
####################################################################################################
def plot_mesh_stats(name,
                    distributions_directory,
                    output_directory,
                    color):

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


####################################################################################################
# @combine_skinned_with_optimized
####################################################################################################
def combine_skinned_with_optimized(skinned_horizontal_image_path,
                                   optimized_horizontal_image_path,
                                   output_path,
                                   delta=100):

    # Open the images
    skinned_im = Image.open(skinned_horizontal_image_path)
    optimized_im = Image.open(optimized_horizontal_image_path)
    
    # Resize to make them with the exact same size 
    optimized_im = optimized_im.resize(skinned_im.size, resample=2)
    
    # Make a new image 
    combined_im = Image.new('RGB', (optimized_im.size[0], (optimized_im.size[1] * 2) + delta),
                            (255, 255, 255))
    combined_im.paste(skinned_im, (0, 0))
    combined_im.paste(optimized_im, (0, optimized_im.size[1] + delta))
    combined_im.save(output_path)
    combined_im.close()
    
    # Close all the images
    skinned_im.close()
    optimized_im.close()


####################################################################################################
# @combine_skinned_with_optimized_with_artistic
####################################################################################################
def combine_skinned_with_optimized_with_artistic(skinned_horizontal_image_path,
                                                 optimized_horizontal_image_path,
                                                 artistic_image,
                                                 output_path,
                                                 delta=200,
                                                 scale_size=2000):

    # Open the images
    skinned_im = Image.open(skinned_horizontal_image_path)
    optimized_im = Image.open(optimized_horizontal_image_path)
    artistic_im = Image.open(artistic_image)
    
    # Add background color to the artistic
    artistic_white_im = Image.new("RGB", artistic_im.size, "WHITE")
    artistic_white_im.paste(artistic_im, (0, 0), artistic_im)
    artistic_im.close() 
        
    # Resize to make them with the exact same size 
    optimized_im = optimized_im.resize(skinned_im.size, resample=2)
    
    # Scale the artistic
    artistic_white_im = artistic_white_im.resize(
        (optimized_im.size[1] * 2, optimized_im.size[1] * 2), resample=2)
    
    # Make a new image 
    combined_im = Image.new('RGB', 
        (optimized_im.size[0] + delta + artistic_white_im.size[0], 
        (optimized_im.size[1] * 2) + delta), (255, 255, 255))

    combined_im.paste(artistic_white_im, (0, 0))
    combined_im.paste(skinned_im, (artistic_white_im.size[0] + delta, 0))
    combined_im.paste(optimized_im, (artistic_white_im.size[0] + delta, optimized_im.size[1] + delta))
    combined_im.save(output_path)
    combined_im.close()
    
    # Close all the images
    artistic_white_im.close()
    skinned_im.close()
    optimized_im.close()
