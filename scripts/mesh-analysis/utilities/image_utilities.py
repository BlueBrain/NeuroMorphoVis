####################################################################################################
# Copyright (c) 2020 - 2021, EPFL / Blue Brain Project
# Author: Marwan Abdellah <marwan.abdellah@epfl.ch>
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
import copy
from PIL import Image


####################################################################################################
# @get_image_dimensions
####################################################################################################
def get_image_dimensions(image_path):
    """Gets the image dimensions from the path

    :param image_path:
    :return:
    """

    # Open the image
    im = Image.open(image_path)

    # Get the size
    width, height = copy.deepcopy(im.size)

    # Close
    im.close()

    # Return size
    return width, height


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

    # Largest dimensions, in which we can normalize all the images
    largest_width, largest_height = get_largest_dimensions_of_all_images(input_directory,
                                                                         list_images)
    for image in list_images:
        create_adjusted_plot_image(
            image, input_directory, output_directory, largest_width, largest_height)


####################################################################################################
# @montage_list_images_with_same_dimensions_horizontally
####################################################################################################
def montage_list_images_with_same_dimensions_horizontally(list_images,
                                                          output_directory,
                                                          montage_name,
                                                          delta=50):

    # Get the dimensions from any image, all the images must have the same dimensions
    any_image = Image.open(list_images[0])
    width, height = any_image.size

    # Compute the dimensions of the new image
    total_width = (width * len(list_images)) + (delta * len(list_images) - 1)
    total_height = height

    montage_im = Image.new('RGB', (total_width, total_height), (255, 255, 255))
    for i, image in enumerate(list_images):
        im = Image.open(image)
        w = 0 if i == 0 else i * (width + delta)
        montage_im.paste(im, (w, 0))

    # Save the path to the montage image
    montage_path = '%s/%s-horizontal.png' % (output_directory, montage_name)
    montage_im.save(montage_path)
    return montage_path


####################################################################################################
# @montage_list_images_with_same_dimensions_vertically
####################################################################################################
def montage_list_images_with_same_dimensions_vertically(list_images,
                                                        output_directory,
                                                        montage_name,
                                                        delta=50):

    # Get the dimensions from any image, all the images must have the same dimensions
    any_image = Image.open(list_images[0])
    width, height = any_image.size

    # Compute the dimensions of the new image
    total_width = width
    total_height = (height * len(list_images)) + (delta * len(list_images) - 1)

    montage_im = Image.new('RGB', (total_width, total_height), (255, 255, 255))
    for i, image in enumerate(list_images):
        im = Image.open(image)
        h = 0 if i == 0 else i * (height + delta)
        montage_im.paste(im, (0, h))

    # Save the path to the montage image
    montage_path = '%s/%s-vertical.png' % (output_directory, montage_name)
    montage_im.save(montage_path)
    return montage_path


####################################################################################################
# @montage_distributions_horizontally
####################################################################################################
def montage_distributions_horizontally(distribution_images,
                                       input_directory,
                                       output_directory,
                                       montage_name,
                                       delta=50):
    """Montages the important distributions into a single image.

    :param distribution_images:
        A list of all the distribution images.
    :param input_directory:
        Directory containing images.
    :param output_directory:
        Results directory.
    :param montage_name:
        The name of the final image.
    :param delta:
        Delta between the images, default 100.
    :return:
        The path to the montage image
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

    # Compute the dimensions of the new image
    total_width = (width * len(images)) + (delta * len(images) - 1)
    total_height = height

    montage_im = Image.new('RGB', (total_width, total_height), (255, 255, 255))
    for i, distribution_image in enumerate(images):
        im = Image.open('%s/%s' % (output_directory, distribution_image))
        w = 0 if i == 0 else i * (width + delta)
        montage_im.paste(im, (w, 0))

    # Save the path to the montage image
    montage_path = '%s/%s-horizontal.png' % (output_directory, montage_name)
    montage_im.save(montage_path)
    return montage_path


####################################################################################################
# @combine_distributions_with_fact_sheet
####################################################################################################
def combine_distributions_with_fact_sheet(distributions_image,
                                          fact_sheet_image,
                                          output_directory,
                                          image_name,
                                          delta=0):

    # Open the input images
    dist_im = Image.open(distributions_image)
    fact_sheet_im = Image.open(fact_sheet_image)

    # Compute the ratio
    ratio = dist_im.size[1] / (1.0 * fact_sheet_im.size[1])
    fact_sheet_im = fact_sheet_im.resize((int(fact_sheet_im.size[0] * ratio),
                                          dist_im.size[1]), resample=2)

    # Create the combined image
    combined_image = Image.new('RGB', (dist_im.size[0] + fact_sheet_im.size[0] + delta,
                                       dist_im.size[1]), (255, 255, 255))

    # Paste the images
    combined_image.paste(dist_im, (0, 0))
    combined_image.paste(fact_sheet_im, (dist_im.size[0] + delta, 0))

    # Combined image path
    combined_image_path = '%s/%s-analysis.png' % (output_directory, image_name)
    combined_image.save(combined_image_path)

    # Close all the open images
    combined_image.close()
    dist_im.close()
    fact_sheet_im.close()

    # Return a reference to the combined image path
    return combined_image_path


####################################################################################################
# @create_comparative_combined_analysis_image
####################################################################################################
def create_comparative_combined_analysis_image(distribution_with_fact_sheet_image,
                                               combined_renderings_image,
                                               output_directory,
                                               reference_name,
                                               delta=0):
    # Open the input images
    dist_and_fs_image = Image.open(distribution_with_fact_sheet_image)
    combined_im = Image.open(combined_renderings_image)

    # Compute the ratio
    ratio = dist_and_fs_image.size[1] / (1.0 * combined_im.size[1])
    combined_im = combined_im.resize((int(dist_and_fs_image.size[0]),
                                          int(combined_im.size[1] / ratio)), resample=2)

    # Create the combined image
    final_image = Image.new('RGB', (combined_im.size[0],
                                    dist_and_fs_image.size[1] + combined_im.size[1] + delta),
                               (255, 255, 255))

    # Paste the images
    final_image.paste(dist_and_fs_image, (0, 0))
    final_image.paste(combined_im, (0, dist_and_fs_image.size[1] + delta))

    # Save
    final_image_path = '%s/%s-combined.png' % (output_directory, reference_name)
    final_image.save(final_image_path)

    dist_and_fs_image.close()
    combined_im.close()
    final_image.close()

    # Return the final image
    return final_image_path


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
