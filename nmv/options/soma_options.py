####################################################################################################
# Copyright (c) 2016 - 2023, EPFL / Blue Brain Project
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

# Internal imports
import nmv.consts
import nmv.enums


####################################################################################################
# @SomaOptions
####################################################################################################
class SomaOptions:
    """Soma options"""

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self):
        """Constructor"""

        # RECONSTRUCTION OPTIONS ###################################################################
        # Reconstruction method
        self.method = nmv.enums.Soma.Representation.META_BALLS

        # Meta ball resolution in case of using the MetaBall generation approach
        self.meta_ball_resolution = nmv.consts.MetaBall.META_DEFAULT_RESOLUTION

        # Radius scale factor for the SoftBody algorithm
        self.radius_scale_factor = nmv.consts.SoftBody.SOMA_SCALE_FACTOR

        # Stiffness
        self.stiffness = nmv.consts.SoftBody.STIFFNESS_DEFAULT

        # Subdivision level of the sphere
        self.subdivision_level = nmv.consts.SoftBody.SUBDIVISIONS_DEFAULT

        # Extrude the arbors from the soma to cover the maximal volume
        self.full_volume_extrusion = True

        # Simulation steps
        self.simulation_steps = nmv.consts.SoftBody.SIMULATION_STEPS_DEFAULT

        # MESH EXPORT OPTIONS ######################################################################
        # Export soma mesh in .ply format
        self.export_ply = False

        # Export soma mesh in .obj format
        self.export_obj = False

        # Export soma mesh in .stl format
        self.export_stl = False

        # Export soma mesh in .blend format
        self.export_blend = False

