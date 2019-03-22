####################################################################################################
# Copyright (c) 2019, EPFL / Blue Brain Project
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
from mathutils import Vector
from bpy.props import IntProperty
from bpy.props import BoolProperty
from bpy.props import FloatProperty
from bpy.props import EnumProperty
from bpy.props import FloatVectorProperty

# Internal modules
import nmv
import nmv.consts
import nmv.enums
import nmv.utilities


# Soma color option
bpy.types.Scene.SomaBaseColor = FloatVectorProperty(
    name="Soma Base Color", subtype='COLOR',
    description="The color of the reconstructed soma",
    default=nmv.enums.Color.SOMA, min=0.0, max=1.0)

# Reconstruction method
bpy.types.Scene.SomaReconstructionMethod = EnumProperty(
    items=[(nmv.enums.Soma.ReconstructionMethod.ARBORS_ONLY,
            '3D Profile',
            'Reconstruct the shape of the soma using the arbors only'),
           (nmv.enums.Soma.ReconstructionMethod.PROFILE_POINTS_ONLY,
            '2D Profile',
            'Reconstruct the shape of the soma using the profile points only'),
           (nmv.enums.Soma.ReconstructionMethod.COMBINED,
            'Mixed',
            'Reconstruct a complex shape for the soma using all available data')],
    name='Method',
    default=nmv.enums.Soma.ReconstructionMethod.ARBORS_ONLY)

# The material applied to the soma mesh following to the reconstruction
bpy.types.Scene.SomaMaterial = EnumProperty(
    items=nmv.enums.Shading.MATERIAL_ITEMS,
    name="Material",
    default=nmv.enums.Shading.LAMBERT_WARD)

# Soft body stiffness option
bpy.types.Scene.Stiffness = FloatProperty(
    name="Stiffness",
    description="The spring factor (or stiffness) of the soft body",
    default=0.1, min=0.001, max=0.999)

# Ico-sphere subdivision level option
bpy.types.Scene.SubdivisionLevel = IntProperty(
    name="Subdivisions",
    description="Subdivision level of the ico-sphere (2-10), convenient 5",
    default=5, min=2, max=10)

# Simulation step option
bpy.types.Scene.SimulationSteps = IntProperty(
    name="Simulation Steps",
    description="The number of steps required to do the simulation",
    default=100, min=10, max=1000)

# Soma simulation progress bar
bpy.types.Scene.SomaSimulationProgress = IntProperty(
    name="Soma Simulation Progress",
    default=0, min=0, max=100, subtype='PERCENTAGE')

# Keep cameras
bpy.types.Scene.KeepSomaCameras = BoolProperty(
    name="Keep Cameras & Lights in Scene",
    description="Keep the cameras in the scene to be used later if this file is saved",
    default=False)

# View size option in microns
bpy.types.Scene.ViewDimensions = FloatProperty(
    name="Dimensions",
    description="The dimensions of the view that will be rendered in microns",
    default=20, min=5, max=50)

# Frame resolution option
bpy.types.Scene.SomaFrameResolution = IntProperty(
    name="Resolution",
    description="The resolution of the image generated from rendering the soma",
    default=512, min=128, max=1024 * 10)

# Soma rendering progress bar
bpy.types.Scene.SomaRenderingProgress = IntProperty(
    name="Soma Rendering Progress",
    default=0, min=0, max=100, subtype='PERCENTAGE')

# Irregular subdivisions for the faces extruded for emanating the arbors
bpy.types.Scene.IrregularSubdivisions = BoolProperty(
    name="Irregular Subdivisions",
    description="Make further irregular subdivisions for the faces created for the arbors",
    default=True)

