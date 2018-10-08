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

__author__      = "Marwan Abdellah"
__copyright__   = "Copyright (c) 2016 - 2018, Blue Brain Project / EPFL"
__credits__     = ["Ahmet Bilgili", "Juan Hernando", "Stefan Eilemann"]
__version__     = "1.0.0"
__maintainer__  = "Marwan Abdellah"
__email__       = "marwan.abdellah@epfl.ch"
__status__      = "Production"



# Blender imports
from mathutils import Vector

# NeuroMorphoVis imports
import neuromorphovis as nmv
import neuromorphovis.geometry
import neuromorphovis.mesh
import neuromorphovis.file
import neuromorphovis.scene

# Import vasculature scripts
import vasculature_sample
import vasculature_section


####################################################################################################
# VasculatureSketcher
####################################################################################################
class VasculatureSketcher:
    """Vasculature sketching class."""

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self,
                 bevel_object):
        """Constructor.

        :param bevel_object:
            Input bevel object.
        """

        self.bevel_object = bevel_object

    ################################################################################################
    # @sketch_section
    ################################################################################################
    def sketch_section(self,
                       section):
        """Sketches the section as a tube

        :param section:
            A given vasculature section.
        :return:
            A reference to the section polyline.
        """

        # Construct the poly-line data
        poly_line_data = list()

        # Append the samples
        for sample in section.samples_list:
            poly_line_data.append([(sample.point[0], sample.point[1], sample.point[2], 1),
                                   sample.radius])

        bevel_object = nmv.mesh.create_bezier_circle(radius=1.0, vertices=16, name='bevel')

        # Draw a polyline
        section_polyline = nmv.geometry.ops.draw_poly_line(poly_line_data,
                                                           bevel_object=bevel_object,
                                                           name=section.name,
                                                           caps=True)
        return section_polyline

    ################################################################################################
    # @sketch_section
    ################################################################################################
    def draw_and_save_section(self,
                              section,
                              output_directory):
        """Draw and save the section.

        :param section:
            Input section.
        :param output_directory:
            Output directory
        """

        # Construct the section polyline
        section_polyline = self.sketch_section(section)

        # Convert the section polyline into a mesh
        section_mesh = nmv.scene.ops.convert_object_to_mesh(section_polyline)

        # Save the section mesh into file
        nmv.file.export_object_to_ply_file(section_mesh, output_directory, section.name)

    ################################################################################################
    # @sketch_section
    ################################################################################################
    def draw_and_save_sections(self,
                               sections_list,
                               output_directory,
                               portion,
                               max_portions):
        """Draws and saves the section as a ply file.

        :param sections_list:
            Input list of sections to be drawn.
        :param output_directory:
            Output directory.
        """

        portion_size = int(float(len(sections_list)) / max_portions)

        start_index = portion * portion_size
        end_index = start_index + portion_size

        # For each section
        for i in range(start_index, end_index):

            if i >= len(sections_list):
                break

            # Indication
            print('%d/%d' % (i, end_index))

            # Clear the scene
            nmv.scene.clear_scene()

            # Draw and save the section
            self.draw_and_save_section(sections_list[i], output_directory)
