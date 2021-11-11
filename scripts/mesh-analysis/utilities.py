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

# System imports
import os
import matplotlib.font_manager as font_manager
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


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