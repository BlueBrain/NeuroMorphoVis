####################################################################################################
# Copyright (c) 2016 - 2021, EPFL / Blue Brain Project
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


####################################################################################################
# @create_text_object
####################################################################################################
def create_text_object(text_string,
                       name='Text'):
    """Create a text object and add it to the scene

    :param text_string:
        The string that will be created.
    :param name:
        The name of text object as appears in the editor.
    :return:
        A reference to the created text object.
    """

    # Create the font curve
    text_curve = bpy.data.curves.new(type="FONT", name=name)

    # Set the body of the font curve to the scale bar value
    text_curve.body = text_string

    # Update the font, for the moment use Arial
    text_curve.font = bpy.data.fonts['ArialMT']

    # Align the font in the center to allow adjusting the position of the handle easily
    text_curve.align_x = 'CENTER'
    text_curve.align_y = 'CENTER'

    # Create the font object and link it to the scene at the origin
    text_object = bpy.data.objects.new(name=name, object_data=text_curve)
    bpy.context.scene.collection.objects.link(text_object)

    # Return a reference to the text object
    return text_object
