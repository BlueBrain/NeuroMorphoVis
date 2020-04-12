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
import nmv.consts
import nmv.enums
import nmv.utilities

####################################################################################################
# Panel options
####################################################################################################
# Reconstruction method
bpy.types.Scene.NMV_SomaReconstructionMethod = bpy.props.EnumProperty(
    items=[(nmv.enums.Soma.Representation.META_BALLS,
            'MetaBalls',
            'Use MetaBalls to reconstruct a rough estimate of the soma shape in real-time.'
            'This approach is extremely fast compared to the Soft Body method and can be '
            'extremely useful for creating large scale circuits with thousands of neurons'),
           (nmv.enums.Soma.Representation.SOFT_BODY,
            'Soft Body',
            'Use Soft Body physics to reconstruct an accurate shape of the neurons using the '
            'physics engine in Blender. This method takes few seconds to build the soma, but it is '
            'way more accurate than the MetaBalls method. Note that this method does not preserve '
            'the final volume of the reconstructed soma shape. It only creates a highly realistic '
            'shape of the soma though for machine learning purposes')],
    name='Method',
    default=nmv.enums.Soma.Representation.META_BALLS)

# Metaball resolution
bpy.types.Scene.NMV_SomaMetaBallResolution = bpy.props.FloatProperty(
    name='MetaBall Resolution',
    description='The resolution of the MetaBall object if the MetaBalls method is selected. '
                'This resolution is valid between 0.01 - 1.0',
    default=0.2, min=0.05, max=1.0)

# Profile
bpy.types.Scene.NMV_SomaProfile = bpy.props.EnumProperty(
    items=[(nmv.enums.Soma.Profile.ARBORS_ONLY,
            '3D Profile',
            'Reconstruct the shape of the soma using the initial samples of the arbors only'),
           (nmv.enums.Soma.Profile.PROFILE_POINTS_ONLY,
            '2D Profile',
            'Reconstruct the shape of the soma using the reported profile points only. '
            'If the morphology file does not contain any profile points, the initial sphere will '
            'not be deformed at all'),
           (nmv.enums.Soma.Profile.COMBINED,
            'Mixed',
            'Reconstruct a complex shape for the soma using all available data')],
    name='Profile',
    default=nmv.enums.Soma.Profile.ARBORS_ONLY)

# Reconstruction time
bpy.types.Scene.NMV_SomaReconstructionTime = bpy.props.FloatProperty(
    name='Generation Time (Sec)',
    description='The time it takes to reconstruct the soma and load its object to the scene',
    default=0, min=0, max=1000000)

# Soma color option
bpy.types.Scene.NMV_SomaBaseColor = bpy.props.FloatVectorProperty(
    name='Soma Base Color', subtype='COLOR',
    description='The base color that will be applied to the reconstructed soma object',
    default=nmv.enums.Color.SOMA, min=0.0, max=1.0)

# The material applied to the soma mesh following to the reconstruction
bpy.types.Scene.NMV_SomaMaterial = bpy.props.EnumProperty(
    items=nmv.enums.Shader.MATERIAL_ITEMS,
    name='Shading',
    description='The shading material that will be applied to the reconstructed soma mesh',
    default=nmv.enums.Shader.LAMBERT_WARD)

# Soma scale factor
bpy.types.Scene.NMV_SomaRadiusScaleFactor = bpy.props.FloatProperty(
    name='Radius Scale Factor',
    description='This scale factor is used to scale the initial radius of the soma soft body '
                'before applying the pulling operation. It ranges from 0.25to 0.9',
    default=0.5, min=0.25, max=0.9)

# Soft body stiffness option
bpy.types.Scene.NMV_Stiffness = bpy.props.FloatProperty(
    name='Stiffness',
    description='The spring factor (or stiffness) of the soft body',
    default=0.1, min=0.001, max=0.999)

# Ico-sphere subdivision level option
bpy.types.Scene.NMV_SubdivisionLevel = bpy.props.IntProperty(
    name='Subdivisions',
    description='Subdivision level of the ico-sphere (2-10), convenient 5, otherwise it might '
                'take several seconds to build the final soma shape',
    default=5, min=2, max=10)

# Irregular subdivisions for the faces extruded for emanating the arbors
bpy.types.Scene.NMV_IrregularSubdivisions = bpy.props.BoolProperty(
    name='Irregular Subdivisions',
    description='Make further irregular subdivisions for the faces created for the arbors to '
                'create smoother and more accurate soma object',
    default=True)

# Simulation step option
bpy.types.Scene.NMV_SimulationSteps = bpy.props.IntProperty(
    name='Simulation Steps',
    description='The number of time steps required to perform the simulation, by default 100. '
                'Minimum value 50, maximum value is 300',
    default=100, min=50, max=300)

# Soma simulation progress bar
bpy.types.Scene.NMV_SomaSimulationProgress = bpy.props.IntProperty(
    name='Physics Simulation Progress',
    description='Reconstruction progress',
    default=0, min=0, max=100, subtype='PERCENTAGE')

# Image format
bpy.types.Scene.NMV_SomaImageFormat = bpy.props.EnumProperty(
    items=nmv.enums.Image.Extension.IMAGE_EXTENSION_ITEMS,
    name='',
    default=nmv.enums.Image.Extension.PNG)

# View size option in microns
bpy.types.Scene.NMV_ViewDimensions = bpy.props.FloatProperty(
    name='Dimensions',
    description='The dimensions of the view that will be rendered in microns',
    default=20, min=5, max=50)

# Frame resolution option
bpy.types.Scene.NMV_SomaFrameResolution = bpy.props.IntProperty(
    name='Resolution',
    description='The resolution of the image generated from rendering the soma. '
                'Default 1024, minimum 512, maximum 1000, ',
    default=1024, min=512, max=1024 * 16)

# Soma rendering progress bar
bpy.types.Scene.NMV_SomaRenderingProgress = bpy.props.IntProperty(
    name='Rendering Progress',
    description='Rendering progress',
    default=0, min=0, max=100, subtype='PERCENTAGE')

# Rendering time
bpy.types.Scene.NMV_SomaRenderingTime = bpy.props.FloatProperty(
    name='Rendering (Sec)',
    description='The time it takes to render the soma into an image',
    default=0, min=0, max=1000000)