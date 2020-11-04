#!/usr/bin/python

from PIL import Image, ImageOps
import ntpath


####################################################################################################
# @compose_synaptic_pathway_frame
####################################################################################################
def compose_synaptic_pathway_frame(full_view_file,
                                   close_up_file,
                                   background_image_file,
                                   output_directory,
                                   edge_gap=100,
                                   close_up_frame_border_thickness=2,
                                   full_view_to_close_up_ratio=0.7):
    """Just a simple function to test the compositing.

    :param full_view_file:
        The path to the full view file.
    :param close_up_file:
        The path to the close up file.
    :param background_image_file:
        The path to the background image
    :param output_directory:
        The output directory of the project.
    :param edge_gap:
        The edge gap for the sides of the frame.
    :param close_up_frame_border_thickness:
        The border thickness of the close-up image.
    :param full_view_to_close_up_ratio:
        The ratio between the full-view image to the close-up image in the frame.
    """

    # Open the background image
    background_image = Image.open(background_image_file)

    # Open the full view image
    full_view_image = Image.open(full_view_file)

    # Open the close-up image
    close_up_image = Image.open(close_up_file)

    # Add a frame to the close-up image
    close_up_image = ImageOps.expand(
        close_up_image, border=close_up_frame_border_thickness, fill='white')

    # Get the size of the background image
    background_width, background_height = background_image.size

    # Widths in pixels for the full view area and the close-up one
    full_view_area_width = int(background_width * full_view_to_close_up_ratio)
    close_up_area_width = background_width - full_view_area_width

    # The drawing areas, where the final images are drawn should consider the edge gap
    full_view_drawing_width = int(full_view_area_width - (edge_gap * 2))
    full_view_drawing_height = int(background_height - (edge_gap * 2))

    # Scale the full view image to fit within the drawing area
    full_view_image_width, full_view_image_height = full_view_image.size
    full_view_aspect_ratio = (1.0 * full_view_image_width) / (1.0 * full_view_image_height)
    if full_view_aspect_ratio > 1.0:
        scale = (1.0 * full_view_image_width) / (1.0 * full_view_drawing_width)
        resized_image_width = full_view_drawing_width
        resized_image_height = int(full_view_image_height / scale)
    else:
        scale = (1.0 * full_view_image_height) / (1.0 * full_view_drawing_height)
        resized_image_height = full_view_drawing_height
        resized_image_width = int(full_view_image_width / scale)

    # The final full-view image is ready to be pasted to the background frame
    full_view_resized_image = full_view_image.resize((
            resized_image_width, resized_image_height), Image.BICUBIC)

    # Calculate the starting x and y pixels where the pasting will happen
    full_view_delta_x = int((full_view_drawing_width - full_view_resized_image.size[0]) * 0.5)
    full_view_delta_y = int((full_view_drawing_height - full_view_resized_image.size[1]) * 0.5)
    full_view_starting_x = edge_gap + full_view_delta_x
    full_view_starting_y = edge_gap + full_view_delta_y

    # Paste the full view image to the background image
    background_image.paste(full_view_resized_image, (full_view_starting_x, full_view_starting_y),
                           full_view_resized_image)

    # The drawing areas, where the final images are drawn should consider the edge gap
    close_up_drawing_width = int(close_up_area_width - (edge_gap * 2))
    close_up_drawing_height = int(background_height - (edge_gap * 2))

    # Scale the close-up image to fit within the drawing area
    close_up_image_width, close_up_image_height = close_up_image.size
    close_up_image_aspect_ratio = (1.0 * close_up_image_width) / (1.0 * close_up_image_height)
    if close_up_image_aspect_ratio < 1.0:
        scale = (1.0 * close_up_image_height) / (1.0 * close_up_drawing_height)
        resized_image_height = close_up_drawing_height
        resized_image_width = int(close_up_image_width / scale)
    else:
        scale = (1.0 * close_up_image_width) / (1.0 * close_up_drawing_width)
        resized_image_width = close_up_drawing_width
        resized_image_height = int(close_up_drawing_height / scale)

    # The final close-up image that will be pasted on the background frame
    close_up_resized_image = close_up_image.resize(
            (resized_image_width, resized_image_height), Image.BICUBIC)

    # Calculate the starting x and y pixels where the pasting will happen
    close_up_image_delta_x = int((close_up_drawing_width - close_up_resized_image.size[0]) * 0.5)
    close_up_image_delta_y = int((close_up_drawing_height - close_up_resized_image.size[1]) * 0.5)
    close_up_starting_x = full_view_area_width + edge_gap + close_up_image_delta_x
    close_up_starting_y = edge_gap + close_up_image_delta_y

    # Paste the close-up image to the background image
    background_image.paste(close_up_resized_image, (close_up_starting_x, close_up_starting_y),
                           close_up_resized_image)

    # Save the background image with the new data
    background_image.save('%s/%s.png' % (output_directory, ntpath.basename(full_view_file)))

    # Close all the images
    background_image.close()
    full_view_image.close()
    close_up_image.close()





