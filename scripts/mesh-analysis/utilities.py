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
import nmv.scene

# System imports
import os
import matplotlib.font_manager as font_manager
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# Internal
import core

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
# @normalize_array
####################################################################################################
def normalize_array(array):
    """Normalizes an input array.

    :param array:
        The given array to be normalized.
    """

    # Gets the maximum value
    max_value = max(array)

    # Normalize
    for i in range(len(array)):
        array[i] /= max_value


####################################################################################################
# @search_for_dist
####################################################################################################
def search_for_dist(distributions,
                    keyword_1,
                    keyword_2):
    """Searchs for a specific histogram in a list of given ones with two ketwords.

    :param distributions:
        List of given distributions files.
    :param keyword_1:
        Keyword 1
    :param keyword_2:
        Keyword 2
    :return:
        If found, the file name, otherwise None.
    """

    # Search by the keywords
    for distribution in distributions:
        if keyword_1 in distribution and keyword_2 in distribution:
            return distribution

    # Otherwise, return None
    return None


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
# @montage_distributions_horizontally
####################################################################################################
def montage_distributions_horizontally(name,
                                       distribution_images,
                                       input_directory,
                                       output_directory,
                                       delta=50):
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

    # Get the images one by one
    images = list()
    images.append(get_image(distribution_images, 'min-angle'))
    images.append(get_image(distribution_images, 'max-angle'))
    images.append(get_image(distribution_images, 'radius-ratio'))
    images.append(get_image(distribution_images, 'edge-ratio'))
    images.append(get_image(distribution_images, 'radius-to-edge-ratio'))

    # Get the dimensions from any image, all the images must have the same dimensions
    any_image = Image.open('%s/%s' % (input_directory, get_image(distribution_images, 'min-angle')))
    width, height = any_image.size

    # Vertical
    # Compute the dimensions of the new image
    total_width = (width * 5) + (delta * 4)
    total_height = height

    new_im = Image.new('RGB', (total_width, total_height), (255, 255, 255))
    for i, distribution_image in enumerate(images):
        im = Image.open('%s/%s' % (output_directory, distribution_image))
        w = 0 if i == 0 else i * (width + delta)
        new_im.paste(im, (w, 0))

    horizontal_image_path = '%s/%s-horizontal.png' % (output_directory, name)
    new_im.save(horizontal_image_path)
    return horizontal_image_path



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
# @compute_mesh_stats
####################################################################################################
def compute_mesh_stats(mesh_object):

    # Mesh stats.
    mesh_stats = core.MeshStats()

    print('  * Computing Mesh Fact Sheet')

    # Set the current object to be the active object
    nmv.scene.set_active_object(mesh_object)

    # Compute the bounding box
    mesh_bbox = core.compute_bounding_box(mesh_object)

    print('\t* Number Partitions')
    mesh_stats.partitions = core.compute_number_partitions(mesh_object)

    # Switch to geometry or edit mode from the object mode
    bpy.ops.object.editmode_toggle()

    # Convert the mesh into a bmesh
    bm = core.convert_from_mesh_object(mesh_object)

    # Compute the surface area
    print('\t* Surface Area')
    mesh_stats.surface_area = core.compute_surface_area(bm)

    # Compute the volume
    print('\t* Volume')
    mesh_stats.volume = core.compute_volume(bm)

    # Compute the number of polygons
    print('\t* Number Polygons')
    mesh_stats.polygons = core.compute_number_polygons(bm)

    # Compute the number of vertices
    print('\t* Number Vertices')
    mesh_stats.vertices = core.compute_number_vertices(bm)

    # Is it watertight
    print('\t* Validating Watertightness')
    watertight_check = core.check_watertightness(bm, mesh_stats.partitions)

    # Results
    return mesh_stats, mesh_bbox, watertight_check


####################################################################################################
# @create_mesh_fact_sheet
####################################################################################################
def create_input_vs_watertight_fact_sheet(input_stats, input_aabb, input_wtc,
                                          wt_stats, wt_aabb, wt_wtc,
                                          output_image_path,
                                          image_resolution=1500):
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
    delta_x = starting_x + int(image_width * 0.4)
    epsilon_x = starting_x + int(image_width * 0.7)

    i = 0.4
    delta_y = i * spacing
    drawing_area.text((starting_x, delta_y), 'Polygons', font=font, fill=(0, 0, 0))
    drawing_area.text((delta_x, delta_y), f'{input_stats.polygons:,d}', font=font, fill=(0, 0, 0))
    drawing_area.text((epsilon_x, delta_y), f'{wt_stats.polygons:,d}', font=font, fill=(0, 0, 0))

    i += 1
    delta_y = i * spacing
    drawing_area.text((starting_x, delta_y), 'Vertices', font=font, fill=(0, 0, 0))
    drawing_area.text((delta_x, delta_y), f'{input_stats.vertices:,d}', font=font, fill=(0, 0, 0))
    drawing_area.text((epsilon_x, delta_y), f'{wt_stats.vertices:,d}', font=font, fill=(0, 0, 0))


    i += 1.5
    delta_y = i * spacing
    drawing_area.text((starting_x, delta_y), 'AABB Width', font=font, fill=(0, 0, 0))
    drawing_area.text((delta_x, delta_y), '%s μm' % format_number_to_power_string(
        input_aabb.x), font=font, fill=(0, 0, 0))
    drawing_area.text((epsilon_x, delta_y), '%s μm' % format_number_to_power_string(
        wt_aabb.x), font=font, fill=(0, 0, 0))

    i += 1
    delta_y = i * spacing
    drawing_area.text((starting_x, delta_y), 'AABB Height', font=font, fill=(0, 0, 0))
    drawing_area.text((delta_x, delta_y), '%s μm' % format_number_to_power_string(
        input_aabb.y), font=font, fill=(0, 0, 0))
    drawing_area.text((epsilon_x, delta_y), '%s μm' % format_number_to_power_string(
        wt_aabb.y), font=font, fill=(0, 0, 0))

    i += 1
    delta_y = i * spacing
    drawing_area.text((starting_x, delta_y), 'AABB Depth', font=font, fill=(0, 0, 0))
    drawing_area.text((delta_x, delta_y), '%s μm' % format_number_to_power_string(
        input_aabb.z), font=font, fill=(0, 0, 0))
    drawing_area.text((epsilon_x, delta_y), '%s μm' % format_number_to_power_string(
        wt_aabb.z), font=font, fill=(0, 0, 0))

    i += 1.0
    delta_y = i * spacing
    drawing_area.text((starting_x, delta_y), 'AABB Diagonal', font=font, fill=(0, 0, 0))
    drawing_area.text((delta_x, delta_y), '%s μm' % format_number_to_power_string(
        input_aabb.diagonal), font=font, fill=(0, 0, 0))
    drawing_area.text((epsilon_x, delta_y), '%s μm' % format_number_to_power_string(
        wt_aabb.diagonal), font=font, fill=(0, 0, 0))

    i += 1.5
    delta_y = i * spacing
    drawing_area.text((starting_x, delta_y), 'Surface Area', font=font, fill=(0, 0, 0))
    drawing_area.text((delta_x, delta_y), '%s μm²' % format_number_to_power_string(
        input_stats.surface_area), font=font, fill=(0, 0, 0))
    drawing_area.text((epsilon_x, delta_y), '%s μm²' % format_number_to_power_string(
        wt_stats.surface_area), font=font, fill=(0, 0, 0))

    i += 1
    delta_y = i * spacing
    drawing_area.text((starting_x, delta_y), 'Volume*', font=font, fill=(0, 0, 0))
    drawing_area.text((delta_x, delta_y), '%s μm³' % format_number_to_power_string(
        input_stats.volume), font=font, fill=(0, 0, 0))
    drawing_area.text((epsilon_x, delta_y), '%s μm³' % format_number_to_power_string(
        wt_stats.volume), font=font, fill=(0, 0, 0))

    i += 1.5
    delta_y = i * spacing
    drawing_area.text((starting_x, delta_y), 'Mesh Partitions',
                      font=font, fill=(0, 0, 0))
    drawing_area.text((delta_x, delta_y), f'{input_stats.partitions:,d}',
                      font=font, fill=(0, 0, 0))
    drawing_area.text((epsilon_x, delta_y), f'{wt_stats.partitions:,d}',
                      font=font, fill=(0, 0, 0))

    i += 1.5
    delta_y = i * spacing
    drawing_area.text((starting_x, delta_y), 'Non Manifold Edges',
                      font=font, fill=(0, 0, 0))
    drawing_area.text((delta_x, delta_y), f'{input_wtc.non_manifold_edges:,d}',
                      font=font, fill=(0, 0, 0))
    drawing_area.text((epsilon_x, delta_y), f'{wt_wtc.non_manifold_edges:,d}',
                      font=font, fill=(0, 0, 0))

    i += 1
    delta_y = i * spacing
    drawing_area.text((starting_x, delta_y), 'Non Manifold Vertices',
                      font=font, fill=(0, 0, 0))
    drawing_area.text((delta_x, delta_y), f'{input_wtc.non_manifold_vertices:,d}',
                      font=font, fill=(0, 0, 0))
    drawing_area.text((epsilon_x, delta_y), f'{wt_wtc.non_manifold_vertices:,d}',
                      font=font, fill=(0, 0, 0))

    i += 1
    delta_y = i * spacing
    drawing_area.text((starting_x, delta_y), 'Non Continuous Edges',
                      font=font, fill=(0, 0, 0))
    drawing_area.text((delta_x, delta_y), f'{input_wtc.non_contiguous_edge:,d}',
                      font=font, fill=(0, 0, 0))
    drawing_area.text((epsilon_x, delta_y), f'{wt_wtc.non_contiguous_edge:,d}',
                      font=font, fill=(0, 0, 0))

    i += 1
    delta_y = i * spacing
    drawing_area.text((starting_x, delta_y), 'Self Intersections',
                      font=font, fill=(0, 0, 0))
    drawing_area.text((delta_x, delta_y), f'{input_wtc.self_intersections:,d}',
                      font=font, fill=(0, 0, 0))
    drawing_area.text((epsilon_x, delta_y), f'{wt_wtc.self_intersections:,d}',
                      font=font, fill=(0, 0, 0))

    i += 1.5
    delta_y = i * spacing
    drawing_area.text((starting_x, delta_y), 'Watertight', font=font, fill=(0, 0, 0))
    drawing_area.text((delta_x, delta_y), 'Yes' if input_wtc.watertight else 'No',
                      font=font, fill=(0, 0, 0))
    drawing_area.text((epsilon_x, delta_y), 'Yes' if wt_wtc.watertight else 'No',
                      font=font, fill=(0, 0, 0))

    fact_sheet_image_path = '%s/%s-fact-sheet.png' % (output_image_path, 'sample')
    fact_sheet_image.save(fact_sheet_image_path)
    fact_sheet_image.close()
    return fact_sheet_image_path