# System imports
import sys, os, re, math
import subprocess
import argparse
from PIL import Image

FILE_TYPE = '.png'


####################################################################################################
# @create_directory
####################################################################################################
def create_directory(path):
    """Creates a new directory of it doesn't exist.

    :param path :
        The path of the directory to be created.
    """

    if os.path.exists(path):
        return
    try:
        os.mkdir(path)
    except ValueError:
        print('ERROR: cannot create directory %s' % path)


####################################################################################################
# @create_adjusted_plot_image
####################################################################################################
def create_adjusted_plot_image(image, input_directory, output_directory, new_width, new_height):

    # Get the width and height
    im = Image.open('%s/%s' % (input_directory, image))
    width, height = im.size

    new_size = (new_width, new_height)
    new_im = Image.new("RGB", new_size, (255, 255, 255))
    starting_y = int(0.5 * (new_height - height))
    new_im.paste(im, (0, starting_y))

    new_im.save('%s/%s' % (output_directory, image))


####################################################################################################
# @create_adjusted_front_projection_image
####################################################################################################
def create_adjusted_front_projection_image(input_directory, output_directory, new_width, new_height):

    # Get the width and height
    morphology_name = os.path.basename(input_directory)
    im = Image.open('%s/%s' % (input_directory, '%s_front_fixed_radius.png' % morphology_name))
    width, height = im.size
    im_white = Image.new("RGB", (width, height + 10), (255, 255, 255))
    im_white.paste(im, (0, 5), im)
    im_white.save('%s/z-front_fixed_radius.png' % output_directory)
    im.close()
    im = im_white
    width, height = im.size

    new_size = (new_width, height)
    new_im = Image.new("RGB", new_size, (255, 255, 255))
    starting_x = int(0.5 * (new_width - width))
    new_im.paste(im, (starting_x, 0))
    new_im.save('%s/%s' % (output_directory, '%s_front_fixed_radius.png' % morphology_name))


####################################################################################################
# @create_adjusted_dendrogram_image
####################################################################################################
def create_adjusted_dendrogram_image(input_directory, output_directory, new_width, new_height):

    im = Image.open('%s/%s' % (input_directory, 'dendrogram_simplified.png'))
    im_white = Image.new("RGB", im.size, (255, 255, 255))
    im_white.paste(im, (0, 0), im)
    im_white.save('%s/z-dendrogram_simplified.png' % output_directory)
    im.close()

    im_width, im_height = im_white.size
    aspect_ratio = (im_width * 1.0) / (1.0 * im_height)

    if aspect_ratio > 1.0:
        actual_width = new_width
        actual_height = int(new_height / aspect_ratio)
        im_white = im_white.resize((actual_width, actual_height), Image.ANTIALIAS)
    else:
        actual_width = new_width
        actual_height = int(aspect_ratio * new_height)
        im_white = im_white.resize((actual_width, actual_height), Image.ANTIALIAS)
    im_white.save('%s/z-dendrogram-simplified.png' % output_directory)
    im_white.close()


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
# @create_adjusted_plot_images
####################################################################################################
def create_adjusted_plot_images(input_directory, output_directory):

    # Get a list of images in all the given ones
    list_images = ['arbor_length.png',
                   'arbor_surface_area.png',
                   'arbor_volume.png',
                   'burke_taper_range_per_arbor.png',
                   'contraction_per_arbor.png',
                   'daughter_ratio_range_per_arbor.png',
                   'global_bifurcation_angle_range_per_arbor.png',
                   'hillman_taper_range_per_arbor.png',
                   'local_bifurcation_angle_range_per_arbor.png',
                   'maximum_branching_order_per_arbor.png',
                   'maximum_euclidean_distance_per_arbor.png',
                   'maximum_path_distance_per_arbor.png',
                   'minimum_euclidean_distance_per_arbor.png',
                   'number_of_bifurcations_per_arbor.png',
                   'number_of_samples_per_arbor.png',
                   'number_of_sections_per_arbor.png',
                   'number_of_short_sections_per_arbor.png',
                   'number_of_terminal_segments_per_arbor.png',
                   'number_of_terminal_tips_per_arbor.png',
                   'number_of_zero_radii_samples_per_arbor.png',
                   'parent_daughter_ratio_range_per_arbor.png',
                   'samples_radii_range_per_arbor.png',
                   'sections_length_range_per_arbor.png',
                   'sections_surface_area_range_per_arbor.png',
                   'sections_volume_range_per_arbor.png',
                   'segments_length_range_per_arbor.png',
                   'segments_surface_area_range_per_arbor.png',
                   'segments_volume_range_per_arbor.png']

    # Largest width
    largest_width, largest_height = get_largest_dimensions_of_all_images(input_directory,
                                                                         list_images)
    for image in list_images:
        create_adjusted_plot_image(
            image, input_directory, output_directory, largest_width, largest_height)

    # Front projection
    create_adjusted_front_projection_image(input_directory, output_directory,
                                           3 * largest_width, largest_height)

    # Dendrogram
    create_adjusted_dendrogram_image(input_directory, output_directory,
                                     3 * largest_width, 3 * largest_height)


####################################################################################################
# @parse_command_line_arguments
####################################################################################################
def parse_command_line_arguments(arguments=None):
    # Add all the options
    description = 'Plotting'
    parser = argparse.ArgumentParser(description=description)

    arg_help = 'Input file'
    parser.add_argument('--input', action='store', dest='input', help=arg_help)

    arg_help = 'Output directory where output written'
    parser.add_argument('--output', action='store', dest='output', help=arg_help)

    # Parse the arguments
    return parser.parse_args()


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
# @group_images
####################################################################################################
def montage_images_to_one_image(input_directory,
                                output_directory,
                                images_list,
                                x_tiles,
                                y_tiles,
                                output_image_name):
    """Group a list of images into a single image.

    :param input_directory:
        Input directory where the images are.
    :param output_directory:
        The output directory where the final image will be created.
    :param images_list:
        A list of images to be stacked.
    :param x_tiles:
        Number of x tiles.
    :param y_tiles:
        Number of y tiles.
    :param output_image_name:
        The name of the output image.
    """

    widths = list()
    heights = list()
    for image in images_list:
        im = Image.open('%s/%s' % (input_directory, image))
        width, height = im.size
        widths.append(width)
        heights.append(height)
        im.close()

    total_width = 0
    total_height = 0
    for i in widths:
        total_width += i
    for i in heights:
        total_height += i

    if x_tiles > y_tiles:
        new_im = Image.new('RGB', (total_width, max(heights)))

        current_width = 0
        for i in range(len(images_list)):
            print(images_list[i])
            im = Image.open('%s/%s' % (output_directory, images_list[i]))
            new_im.paste(im, (current_width, 0))
            current_width += widths[i]
    else:
        new_im = Image.new('RGB', (max(widths), total_height))

        current_height = 0
        for i in range(len(images_list)):
            im = Image.open('%s/%s' % (output_directory, images_list[i]))
            new_im.paste(im, (0, current_height))
            current_height += heights[i]

    new_im.save('%s/%s.png' % (output_directory, output_image_name))
    new_im.save('%s/%s.pdf' % (output_directory, output_image_name))


####################################################################################################
# @group_length_analysis
####################################################################################################
def group_length_analysis(input_directory,
                          output_directory):

    # Get the files
    image_files = list()
    image_files.append(get_image(os.listdir(input_directory),
                                 'arbor_length'))
    image_files.append(get_image(os.listdir(input_directory),
                                 'sections_length_range_per_arbor'))
    image_files.append(get_image(os.listdir(input_directory),
                                 'segments_length_range_per_arbor'))

    montage_images_to_one_image(input_directory, output_directory, image_files, 3, 1,
                                'z-lengths')


####################################################################################################
# @group_surface_area_analysis
####################################################################################################
def group_surface_area_analysis(input_directory,
                                output_directory):

    # Get the files
    image_files = list()
    image_files.append(get_image(os.listdir(input_directory),
                                 'arbor_surface_area'))
    image_files.append(get_image(os.listdir(input_directory),
                                 'sections_surface_area_range_per_arbor'))
    image_files.append(get_image(os.listdir(input_directory),
                                 'segments_surface_area_range_per_arbor'))

    montage_images_to_one_image(input_directory, output_directory, image_files, 3, 1,
                                'z-surface_areas')


####################################################################################################
# @group_volume_analysis
####################################################################################################
def group_volume_analysis(input_directory,
                          output_directory):

    # Get the files
    image_files = list()
    image_files.append(get_image(os.listdir(input_directory),
                                 'arbor_volume'))
    image_files.append(get_image(os.listdir(input_directory),
                                 'sections_volume_range_per_arbor'))
    image_files.append(get_image(os.listdir(input_directory),
                                 'segments_volume_range_per_arbor'))

    montage_images_to_one_image(input_directory, output_directory, image_files, 3, 1,
                                'z-volumes')


####################################################################################################
# @group_distance_analysis
####################################################################################################
def group_distance_analysis(input_directory,
                            output_directory):

    # Get the files
    image_files = list()
    image_files.append(get_image(os.listdir(input_directory),
                                 'minimum_euclidean_distance_per_arbor'))
    image_files.append(get_image(os.listdir(input_directory),
                                 'maximum_euclidean_distance_per_arbor'))
    image_files.append(get_image(os.listdir(input_directory),
                                 'maximum_path_distance_per_arbor'))

    montage_images_to_one_image(input_directory, output_directory, image_files, 3, 1,
                                'z-distances')


####################################################################################################
# @group_angles_analysis
####################################################################################################
def group_angles_analysis(input_directory,
                          output_directory):

    # Get the files
    image_files = list()
    image_files.append(get_image(os.listdir(input_directory),
                                 'local_bifurcation_angle_range_per_arbor'))
    image_files.append(get_image(os.listdir(input_directory),
                                 'global_bifurcation_angle_range_per_arbor'))

    montage_images_to_one_image(input_directory, output_directory, image_files, 2, 1,
                                'z-angles')


####################################################################################################
# @group_taper_analysis
####################################################################################################
def group_taper_analysis(input_directory,
                         output_directory):

    # Get the files
    image_files = list()
    image_files.append(get_image(os.listdir(input_directory),
                                 'burke_taper_range_per_arbor'))
    image_files.append(get_image(os.listdir(input_directory),
                                 'hillman_taper_range_per_arbor'))

    montage_images_to_one_image(input_directory, output_directory, image_files, 2, 1,
                                'z-tapers')


####################################################################################################
# @group_ratios_analysis
####################################################################################################
def group_ratios_analysis(input_directory,
                          output_directory):

    # Get the files
    image_files = list()
    image_files.append(get_image(os.listdir(input_directory),
                                 'contraction_per_arbor'))
    image_files.append(get_image(os.listdir(input_directory),
                                 'daughter_ratio_range_per_arbor'))
    image_files.append(get_image(os.listdir(input_directory),
                                 'parent_daughter_ratio_range_per_arbor'))

    montage_images_to_one_image(input_directory, output_directory, image_files, 3, 1,
                                'z-ratios')


####################################################################################################
# @group_number_analysis
####################################################################################################
def group_number_analysis(input_directory,
                          output_directory):

    # Get the files
    image_files = list()
    image_files.append(get_image(os.listdir(input_directory),
                                 'number_of_samples_per_arbor'))
    image_files.append(get_image(os.listdir(input_directory),
                                 'number_of_sections_per_arbor'))
    image_files.append(get_image(os.listdir(input_directory),
                                 'number_of_bifurcations_per_arbor'))
    montage_images_to_one_image(input_directory, output_directory, image_files, 3, 1,
                                'z-numbers-1')

    image_files = list()
    image_files.append(get_image(os.listdir(input_directory),
                                 'number_of_terminal_tips_per_arbor'))
    image_files.append(get_image(os.listdir(input_directory),
                                 'number_of_terminal_segments_per_arbor'))
    image_files.append(get_image(os.listdir(input_directory),
                                 'number_of_short_sections_per_arbor'))
    montage_images_to_one_image(input_directory, output_directory, image_files, 3, 1,
                                'z-numbers-2')


def group_results(input_directory, output_directory):

    image_files = list()
    morphology_name = os.path.basename(input_directory)
    image_files.append(get_image(os.listdir(output_directory), '%s_front_fixed_radius.png' %
                                 morphology_name))
    #image_files.append(get_image(os.listdir(output_directory), 'z-dendrogram-simplified'))
    image_files.append(get_image(os.listdir(output_directory), 'z-numbers-1'))
    image_files.append(get_image(os.listdir(output_directory), 'z-numbers-2'))
    image_files.append(get_image(os.listdir(output_directory), 'z-lengths'))
    image_files.append(get_image(os.listdir(output_directory), 'z-surface_areas'))
    image_files.append(get_image(os.listdir(output_directory), 'z-volumes'))
    image_files.append(get_image(os.listdir(output_directory), 'z-distances'))
    image_files.append(get_image(os.listdir(output_directory), 'z-ratios'))
    montage_images_to_one_image(output_directory, output_directory, image_files, 1, 7,
                                'z-group')


####################################################################################################
# @Main
####################################################################################################
if __name__ == "__main__":

    # Parse the command line arguments
    args = parse_command_line_arguments()

    output = '%s/output' % args.input
    create_directory(output)

    create_adjusted_plot_images(args.input, output)

    group_length_analysis(output, output)
    group_surface_area_analysis(output, output)
    group_volume_analysis(output, output)
    group_distance_analysis(output, output)
    group_angles_analysis(output, output)
    group_number_analysis(output, output)
    group_ratios_analysis(output, output)
    group_taper_analysis(output, output)

    group_results(args.input, output)
