####################################################################################################
# Copyright (c) 2025, Open Brain Institute
# Author(s): Marwan Abdellah <marwan.abdellah@openbraininstitute.org>
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
import argparse
from PIL import Image, ImageOps
import os
import sys 

def get_images_from_directory(directory):
    """
    Given a directory, finds and returns the file paths of the large image and the closeup image.
    The closeup image is expected to end with '_closeup.png'.
    
    Returns:
        (large_image_path, small_image_path)
    """
    png_files = [f for f in os.listdir(directory) if f.lower().endswith(".png")]

    # Separate closeup image
    small_image = None
    large_image = None
    for f in png_files:
        if f.lower().endswith("_closeup.png"):
            small_image = os.path.join(directory, f)
        else:
            large_image = os.path.join(directory, f)

    if not large_image or not small_image:
        raise FileNotFoundError("Could not find both large and _closeup PNG images in the directory.")

    return large_image, small_image

    
####################################################################################################
# @run_compose_images
####################################################################################################
def run_compose_images(options):
    
    # Search for the images 
    large_img_path, small_img_path = get_images_from_directory(options.images_directory)
    
    # Load images
    large_img = Image.open(large_img_path)   
    small_img = Image.open(small_img_path)  

    # Resize small image to be about 1/4 the width of the large image
    large_width, large_height = large_img.size
    target_width = int(large_width  * options.closeup_ratio)
    aspect_ratio = small_img.height / small_img.width
    target_height = int(target_width * aspect_ratio)
    small_img_resized = small_img.resize((target_width, target_height), Image.LANCZOS)

    # Add black border (5 pixels)
    border_width = 3
    small_img_bordered = ImageOps.expand(small_img_resized, border=border_width, fill='black')

    # Calculate position for top-right corner
    bordered_width, bordered_height = small_img_bordered.size
    x_offset = large_width - bordered_width
    y_offset = 0

    # Ensure both images are RGBA (for transparency support)
    large_img = large_img.convert("RGBA")
    small_img_bordered = small_img_bordered.convert("RGBA")

    # Overlay the bordered small image on top of the large image
    combined = large_img.copy()
    combined.paste(small_img_bordered, (x_offset, y_offset), small_img_bordered)

    # Save or show result
    image_name = os.path.basename(large_img_path)
    combined.save(f"{options.images_directory}/{os.path.splitext(image_name)[0]}_combined.png")
        
        
####################################################################################################
# @parse_command_line_arguments
####################################################################################################
def parse_command_line_arguments(arguments=None):
    """Parses the input arguments.

    :param arguments:
        Command line arguments.
    :return:
        Arguments list.
    """

    # add all the options
    description = 'Composes images.'
    parser = argparse.ArgumentParser(description=description)
    
    arg_help = 'A circuit in sonata format'
    parser.add_argument('--images-directory',
                        action='store', dest='images_directory', help=arg_help)
    
    arg_help = 'Ratio between two images, e.g. 0.25 for a small image that is 1/4 the width of the large image'
    parser.add_argument('--closeup-ratio',
                        action='store', dest='closeup_ratio', type=float, default=0.25,
                        help=arg_help)

    # Parse the arguments
    return parser.parse_args()


####################################################################################################
# @ Main
####################################################################################################
if __name__ == "__main__":

    print("Command line arguments:", sys.argv)

    # Parse the command line arguments
    args = parse_command_line_arguments()
    
    # Run the rendering task
    run_compose_images(options=args)    