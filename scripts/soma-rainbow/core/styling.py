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
import nmv.scene
import nmv.shading
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



####################################################################################################
# @get_rgb_from_wavelength
####################################################################################################
def get_rgb_color_from_wavelength(wavelength,
                                  gamma=0.8):
    """This converts a given wavelength of light to an approximate RGB  color value.
    The wavelength must be given in nanometers in the range  from 380 nm through 750 nm (789 THz
    through 400 THz).

    :param wavelength: Input wavelength.
    :param gamma: Gamma value.
    :return: RGB color list [R G B]
    """

    # Wavelength
    wavelength = float(wavelength)

    if wavelength >= 380 and wavelength <= 440:
        attenuation = 0.3 + 0.7 * (wavelength - 380) / (440 - 380)
        r = ((-(wavelength - 440) / (440 - 380)) * attenuation) ** gamma
        g = 0.0
        b = (1.0 * attenuation) ** gamma
    elif wavelength >= 440 and wavelength <= 490:
        r = 0.0
        g = ((wavelength - 440) / (490 - 440)) ** gamma
        b = 1.0
    elif wavelength >= 490 and wavelength <= 510:
        r = 0.0
        g = 1.0
        b = (-(wavelength - 510) / (510 - 490)) ** gamma
    elif wavelength >= 510 and wavelength <= 580:
        r = ((wavelength - 510) / (580 - 510)) ** gamma
        g = 1.0
        b = 0.0
    elif wavelength >= 580 and wavelength <= 645:
        r = 1.0
        g = (-(wavelength - 645) / (645 - 580)) ** gamma
        b = 0.0
    elif wavelength >= 645 and wavelength <= 750:
        attenuation = 0.3 + 0.7 * (750 - wavelength) / (750 - 645)
        r = (1.0 * attenuation) ** gamma
        g = 0.0
        b = 0.0
    else:
        r = 0.0
        g = 0.0
        b = 0.0

    # Return a list of RGB
    return [r, g, b]


####################################################################################################
# @get_rgb_color_from_value
####################################################################################################
def get_rgb_color_from_value(value,
                             min_value,
                             max_value):
    """Gets an RGB value from a given value within a range.

    :param value:
        Given value.
    :param min_value:
        Min value of the range.
    :param max_value:
        Max value of the range.
    :return:
        RGB color in a list [R G B]
    """

    # Wavelengths
    min_wavelength = 380
    max_wavelength = 750

    # Ranges
    range_wavelength = max_wavelength - min_wavelength
    range_values = max_value - min_value

    # Wavelength corresponding to the given value after scaling
    wavelength = min_wavelength + (((value - min_value) / range_values) * range_wavelength)

    # Get the RGB color corresponding to wavelength
    color = get_rgb_color_from_wavelength(wavelength)

    # Return the color
    return color


####################################################################################################
# @apply_style
####################################################################################################
def apply_rainbow_style(neurons,
                        styles,
                        y_min,
                        y_max):
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

        # Get the height of the neuron
        location = neuron.position

        # Get object color
        color = get_rgb_color_from_value(location[1], y_min, y_max)

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