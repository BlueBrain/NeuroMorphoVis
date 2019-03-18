####################################################################################################
# Copyright (c) 2016 - 2018, EPFL / Blue Brain Project
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
import sys, os
import_paths = ['core']
for import_path in import_paths:
    sys.path.append(('%s/%s' %(os.path.dirname(os.path.realpath(__file__)), import_path)))

# NeuroMorphoVis imports
import nmv
import nmv.shading
import nmv.rendering
import nmv.enums
import nmv.geometry


####################################################################################################
# @get_tag_rgb_color
####################################################################################################
def get_tag_rgb_color(tag,
                      styles):
    """Returns the RGB color of a given tag from the style list.

    :param tag:
        A given tag.
    :param styles:
        A list of styles
    :return:
        RGB color.
    """

    for style in styles:
        if style[0] == tag:
            return style[1]


####################################################################################################
# @get_tag_alpha
####################################################################################################
def get_tag_alpha(tag,
                  styles):
    """Returns the alpha value of a given tag from the style list.

    :param tag:
        A given tag.
    :param styles:
        A list of styles
    :return:
        Alpha value.
    """

    for style in styles:
        if style[0] == tag:
            return style[2]


####################################################################################################
# @get_tag_shader
####################################################################################################
def get_tag_shader(tag,
                   styles):
    """Returns the shader of a given tag from the style list.

    :param tag:
        A given tag.
    :param styles:
        A list of styles
    :return:
        Alpha value.
    """

    for style in styles:
        if style[0] == tag:
            return style[3]


####################################################################################################
# @apply_style
####################################################################################################
def apply_style(neurons,
                styles):
    """Apply a style given from the configuration to the loaded neurons.

    :param neurons:
        A list of neurons loaded to the scene.
    :param styles:
        A style configuration.
    """

    print('* Applying style')
    for i, neuron in enumerate(neurons):

        if neuron.membrane_meshes is None:
            continue

        # Get the tag
        tag = neuron.tag

        # Color
        color = get_tag_rgb_color(tag, styles)

        # Shader
        shader = nmv.enums.Shading.get_enum(get_tag_shader(tag, styles))

        # Alpha
        alpha = get_tag_alpha(tag, styles)

        style_name = 'style_%s_%s' % (str(tag),  str(neuron.gid))

        # Create the shader from the shader library
        material = nmv.shading.create_material(style_name, color, shader)

        # Apply the shader to the membrane object
        for membrane_mesh in neuron.membrane_meshes:
            if membrane_mesh is None: continue
            nmv.shading.set_material_to_object(membrane_mesh, material)


####################################################################################################
# @apply_style
####################################################################################################
def draw_spheres(neurons,
                 styles):
    """Draw the neurons as spheres.

    :param neurons:
        A list of neurons.
    :param styles:
        A style configuration.
    :return:
        Draw spheres list.
    """

    spheres = list()

    for i, neuron in enumerate(neurons):

        # Get the tag
        tag = neuron.tag

        # Color
        color = get_tag_rgb_color(tag, styles)

        # Shader
        shader = nmv.enums.Shading.get_enum(get_tag_shader(tag, styles))

        # Alpha
        alpha = get_tag_alpha(tag, styles)

        style_name = 'style_%s_%s' % (str(tag), str(neuron.gid))

        # Create the shader from the shader library
        material = nmv.shading.create_material(style_name, color, shader)

        # Draw the sphere
        neuron_sphere = nmv.geometry.create_uv_sphere(location=neuron.position,
            radius=neuron.soma_mean_radius, name='neuron_%s' % str(neuron.gid))
        spheres.append(neuron_sphere)

        nmv.shading.set_material_to_object(neuron_sphere, material)

    # Return a list of spheres of the neurons
    return spheres
