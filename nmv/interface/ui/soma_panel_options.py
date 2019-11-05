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

# Internal modules
import nmv
import nmv.consts
import nmv.enums
import nmv.utilities


# Reconstruction method
bpy.types.Scene.NMV_SomaReconstructionMethod = bpy.props.EnumProperty(
    items=[(nmv.enums.Soma.ReconstructionMethod.META_BALLS,
            'MetaBalls',
            'Use the MetaBalls to reconstruct a rough estimate of the soma shape in real-time'),
           (nmv.enums.Soma.ReconstructionMethod.SOFT_BODY_PHYSICS,
            'SoftBody',
            'Use SoftBody physics to reconstruct an accurate shape of the neurons using the '
            'physics engine in Blender. This method takes few seconds to build the soma.')],
    name='Method',
    default=nmv.enums.Soma.ReconstructionMethod.META_BALLS)

# Metaball resolution
bpy.types.Scene.NMV_SomaMetaBallResolution = bpy.props.FloatProperty(
    name="MetaBall Resolution",
    description="The resolution of the MetaBall object. "
                "Normally it should be valid between 0.1 - 0.5",
    default=0.25, min=0.05, max=0.999)

# Profile
bpy.types.Scene.NMV_SomaProfile = bpy.props.EnumProperty(
    items=[(nmv.enums.Soma.Profile.ARBORS_ONLY,
            '3D Profile',
            'Reconstruct the shape of the soma using the arbors only'),
           (nmv.enums.Soma.Profile.PROFILE_POINTS_ONLY,
            '2D Profile',
            'Reconstruct the shape of the soma using the profile points only'),
           (nmv.enums.Soma.Profile.COMBINED,
            'Mixed',
            'Reconstruct a complex shape for the soma using all available data')],
    name='Profile',
    default=nmv.enums.Soma.Profile.ARBORS_ONLY)

# Reconstruction time
bpy.types.Scene.NMV_SomaReconstructionTime = bpy.props.FloatProperty(
    name="Generation Time (Sec)",
    description="The time it takes to load the morphology from file and draw it to the viewport",
    default=0, min=0, max=1000000)


# Soma color option
bpy.types.Scene.NMV_SomaBaseColor = bpy.props.FloatVectorProperty(
    name="Soma Base Color", subtype='COLOR',
    description="The color of the reconstructed soma",
    default=nmv.enums.Color.SOMA, min=0.0, max=1.0)

# The material applied to the soma mesh following to the reconstruction
bpy.types.Scene.NMV_SomaMaterial = bpy.props.EnumProperty(
    items=nmv.enums.Shading.MATERIAL_ITEMS,
    name="Material",
    default=nmv.enums.Shading.LAMBERT_WARD)

# Soft body stiffness option
bpy.types.Scene.NMV_Stiffness = bpy.props.FloatProperty(
    name="Stiffness",
    description="The spring factor (or stiffness) of the soft body",
    default=0.1, min=0.001, max=0.999)

# Ico-sphere subdivision level option
bpy.types.Scene.NMV_SubdivisionLevel = bpy.props.IntProperty(
    name="Subdivisions",
    description="Subdivision level of the ico-sphere (2-10), convenient 5",
    default=5, min=2, max=10)

# Simulation step option
bpy.types.Scene.NMV_SimulationSteps = bpy.props.IntProperty(
    name="Simulation Steps",
    description="The number of time steps required to perform the simulation, by default 100",
    default=100, min=10, max=300)

# Soma simulation progress bar
bpy.types.Scene.NMV_SomaSimulationProgress = bpy.props.IntProperty(
    name="Soma Simulation Progress",
    default=0, min=0, max=100, subtype='PERCENTAGE')

# Keep cameras
bpy.types.Scene.NMV_KeepSomaCameras = bpy.props.BoolProperty(
    name="Keep Cameras & Lights in Scene",
    description="Keep the cameras in the scene to be used later if this file is saved",
    default=False)

# View size option in microns
bpy.types.Scene.NMV_ViewDimensions = bpy.props.FloatProperty(
    name="Dimensions",
    description="The dimensions of the view that will be rendered in microns",
    default=20, min=5, max=50)

# Frame resolution option
bpy.types.Scene.NMV_SomaFrameResolution = bpy.props.IntProperty(
    name="Resolution",
    description="The resolution of the image generated from rendering the soma",
    default=512, min=128, max=1024 * 10)

# Soma rendering progress bar
bpy.types.Scene.NMV_SomaRenderingProgress = bpy.props.IntProperty(
    name="Soma Rendering Progress",
    default=0, min=0, max=100, subtype='PERCENTAGE')

# Irregular subdivisions for the faces extruded for emanating the arbors
bpy.types.Scene.NMV_IrregularSubdivisions = bpy.props.BoolProperty(
    name="Irregular Subdivisions",
    description="Make further irregular subdivisions for the faces created for the arbors",
    default=True)

