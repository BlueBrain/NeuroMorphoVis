# NeuroMorphoVis Configuration Files

_NeuroMorphoVis_ also supports configuration files.

## Usage 

To use configuration files, the user should execute _NeuroMorphoVis_ via the shell script __neuromorphovis.sh__ and not via the python script __neuromorphovis.py__. The configuration file, for example _configuration-file.cfg_, is given as an input argument to the script __neuromorphovis.sh__ as follows

``` 
neuromorphovis.sh configuration-file.cfg
```

If the given configuration file, for example _user-configuration.cfg_, does not exist, the user will get this error 

```
./neuromorphovis.sh: user-configuration.cfg: No such file or directory
``` 

However, if the configuration file exists and is valid, _NeuroMorphoVis_ will print the following line upon its execution
```
 $ ./neuromorphovis.sh user-configuration.cfg 
 
Using the configuration file [user-configuration.cfg]
```

### Note
Note that this configuration file is also a shell script, and you can use any shell synatx inside it, for example _$HOME_ or _$PWD_. It must be also noted that there should not be any spaces when you set the different configuration parameters. For example, the following configurations are valid
```
BLENDER_EXECUTABLE=/usr/bin/blender
BLENDER_EXECUTABLE=/usr/bin/blender # This is the default Blender path
BLENDER_EXECUTABLE='/usr/bin/blender'
BLENDER_EXECUTABLE="/usr/bin/blender"
``` 

But the following configurations are invalid
```
BLENDER_EXECUTABLE= /usr/bin/blender  # Note the space between the equal sign and /usr.
BLENDER_EXECUTABLE=[/usr/bin/blender] # You cannot use square brackets.
BLENDER_EXECUTABLE=(/usr/bin/blender) # You cannot use normal brackets.
BLENDER_EXECUTABLE={/usr/bin/blender} # You cannot use curly brackets.
```

## Configuration File Structure
The full structure of a default _NeuroMorphoVis_ configuration file is as follows: 
```
####################################################################################################
# Copyright (c) 2016 - 2018, EPFL / Blue Brain Project
#               Marwan Abdellah <marwan.abdellah@epfl.ch>
#
# This file is part of NeuroMorphoVis <https://github.com/BlueBrain/NeuroMorphoVis>
#
# This library is free software; you can redistribute it and/or modify it under the terms of the
# GNU Lesser General Public License version 3.0 as published by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License along with this library;
# if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301 USA.
####################################################################################################

####################################################################################################
### INPUT PARAMETERS
####################################################################################################
# Blender executable
# By default, we will use the system-installed Blender, otherwise you can use a custom version
# You can also point to a specific Blender version, for example $HOME/blender-2.79/blender
BLENDER_EXECUTABLE=blender

# Input source
# Use ['file'] for loading .H5 or .SWC morphology files
# Use ['directory'] for loading a directory contains .H5 or .SWC morphology files
# Use ['gid'] for loading a single neuron in a BBP circuit (works only on BBP clusters)
# Use ['target'] for loading a target (group of GIDs) in a BBP circuit (works only on BBP clusters)
INPUT=[SELECT INPUT SOURCE]

# Blue config
# A BBP circuit config required only if INPUT is set to 'target' or 'gid', otherwise ignored.
BLUE_CONFIG=[SET BLUE CONFIG FILE]

# A BBP cell target (or group of GIDs), if INPUT is set to 'target', otherwise ignored.
TARGET=[SET TARGET]

# A BBP neuron GID, if INPUT is set to 'gid', otherwise ignored.
GID=[SET GID]

# Morphology file, if INPUT is set to 'file', otherwise ignored.
MORPHOLOGY_FILE=[SET MORPHOLOGY FILE]

# Morphology directory, if INPUT is set to 'directory', otherwise ignored.
MORPHOLOGY_DIRECTORY=[SET MORPHOLOGY DIRECTORY]

####################################################################################################
### OUTPUT PARAMETERS
####################################################################################################
# Output directory
# This is where all the results (somata, morphologies, meshes, images, etc...) will be generated
OUTPUT_DIRECTORY=[SET OUTPUT DIRECTORY]

####################################################################################################
# EXECUTION PARAMETERS
####################################################################################################
# Execution node
# Use ['local'] for running the framework on your machine
# Use ['cluster'] for running the framework on the BBP visualization cluster
EXECUTION_NODE=[SELECT EXECUTION NODE]

# Jobs granularity: This option is valid only for 'cluster' execution
# Use ['high] for rendering
# Use ['low'] for generating huge number of meshes
JOBS_GRANULARITY=[SET GRANULARITY]

# Number of cores that will be used to create the meshes if the granularity is low
NUMBER_CORES=[SET NUMBER OF CORES]

####################################################################################################
# MORPHOLOGY / SOMA SKELETON PARAMETERS
####################################################################################################
# Reconstruct morphology skeleton to export it later, 'yes/no'
RECONSTRUCT_MORPHOLOGY_SKELETON=yes

# Skeleton
# Use ['original'] for loading the original as specified in the morphology file, default
# Use ['tapered'] for constructing a tapered skeleton
# Use ['zigzag'] for constructing a zigzag algorithm
# Use ['tapered-zigzag'] for constructing a tapered-zigzaged skeleton
SKELETON=original

# Soma representation
# Use ['no'] to ignore the soma
# Use ['sphere'] to render the soma as a symbolic sphere
# Use ['profile'] to reconstruct a 3D profile using soft body simulation, default
SOMA_REPRESENTATION=profile

# Soma stiffness, range (0.01 - 0.99), default 0.25.
SOMA_STIFFNESS=0.1

# Soma subdivision level, convenient range (3-7), default 6.
SOMA_SUBDIVISION_LEVEL=5

# Axon building, 'yes/no'
IGNORE_AXON=no

# Basal dendrites building, 'yes/no'
IGNORE_BASAL_DENDRITES=no

# Apical dendrites building, 'yes/no'
IGNORE_APICAL_DENDRITES=no

# Maximum axon branching order
MAX_AXON_BRANCHING_ORDER=3

# Maximum basal dendrites branching order
MAX_BASAL_DENDRITES_BRANCHING_ORDER=1000

# Maximum apical dendrites branching order
MAX_APICAL_DENDRITES_BRANCHING_ORDER=1000

# Morphology reconstruction method
# Use ['connected-sections-repaired'], where sections are connected together (after repair).
# Use ['connected-sections'], where sections are connected together (without morphology repair).
# Use ['disconnected-sections'], where sections are disconnected from each others.
# Use ['articulated-sections'], where sections are connected by spheres.
# Use ['disconnected-segments'], where segments are disconnected.
MORPHOLOGY_RECONSTRUCTION_ALGORITHM=connected-sections-repaired

# Branching method
# Use ['angles'] to connect the smallest angle branch to the parent.
# Use ['radii'] to connect the largest radius branch to the parent, default.
BRANCHING_METHOD=radii

# Sections' radii
# Use ['default'] to use the reported radii in the morphology file
# Use ['scaled'] to scale the branches with a specific scale factor RADII_SCALE_FACTOR
# Use ['fixed'] to have fixed section radius FIXED_SECTION_RADIUS for all the arbors
SET_SECTION_RADII=default

# Radii scale factor if the 'SET_SECTION_RADII=scaled' method is used, otherwise ignored
RADII_SCALE_FACTOR=1.0

# Section fixed radius value if the 'SET_SECTION_RADII=fixed' method is used, otherwise ignored
FIXED_SECTION_RADIUS=1.0

# Sections bevel sides, reflecting number of sides per cross section (4, 8, 16 or 32), by default 16
SECTION_BEVEL_SIDES=16

# Save morphology .BLEND file, 'yes/no'
EXPORT_NEURON_MORPHOLOGY_BLEND=no

# Export soma .PLY mesh, 'yes/no'
EXPORT_SOMA_MESH_PLY=no

# Save soma .OBJ mesh, 'yes/no'
EXPORT_SOMA_MESH_OBJ=no

# Save soma .STL mesh, 'yes/no'
EXPORT_SOMA_MESH_STL=no

# Save soma .BLEND mesh, 'yes/no'
EXPORT_SOMA_MESH_BLEND=no

####################################################################################################
# MESH PARAMETERS
####################################################################################################
# Reconstruct soma mesh ONLY, 'yes/no'
RECONSTRUCT_SOMA_MESH=no

# Reconstruct the entire neuron mesh as a piecewise object, 'yes/no'
RECONSTRUCT_NEURON_MESH=no

# Meshing technique
# Use ['piecewise-watertight'] for creating piece-wise watertight meshes
# Use ['union'] for creating watertight meshes using the Union-based meshing algorithm
# Use ['bridging'] for creating smooth branching meshes
MESHING_TECHNIQUE=piecewise_watertight

# Neuron surface
# Use ['smooth'] for smooth surface
# Use ['rough'] for rough surface
SURFACE=rough

# Neuron edges
# Use ['smooth'] for smooth edges
# Use ['hard'] for hard edges
EDGES=hard

# Connect the soma mesh to the arbors, 'yes/no'
CONNECT_SOMA_MESH_TO_ARBORS=no

# Connect neuron objects into a single mesh, 'yes/no'
CONNECT_NEURON_OBJECTS_INTO_SINGLE_MESH=no

# Mesh Tessellation (between 0.1 and 1.0)
TESSELLATION_LEVEL=0.25

# Export the mesh in the global coordinates, 'yes/no'
GLOBAL_COORDINATES=no

# Spines
# Use ['ignore'] for ignoring building the spines
# Use ['circuit'] for building spines from a BBP circuit
# Use ['random'] for building random spines.
SPINES=circuit

# Spines meshes
# Use ['hq'] for loading high quality meshes
# Use ['lq'] for loading low quality meshes
SPINES_QUALITY=lq

# Random spines percentage (1-100)
RANDOM_SPINES_PERCENTAGE=20

# Add nucleus mesh, 'yes/no'
ADD_NUCLEUS=no

# export .PLY meshes, 'yes/no'
EXPORT_NEURON_MESH_PLY=no

# Save .OBJ meshes, 'yes/no'
EXPORT_NEURON_MESH_OBJ=no

# Save .STL meshes, 'yes/no'
EXPORT_NEURON_MESH_STL=no

# Save mesh .BLEND file, 'yes/no'
EXPORT_NEURON_MESH_BLEND=no

####################################################################################################
# MATERIALS PARAMETERS
####################################################################################################
# Soma RGB color in the form of 'R_G_B'
SOMA_COLOR=0_0_0

# Axon RGB color in the form of 'R_G_B'
AXON_COLOR=0_0_0

# Basal dendrites RGB color in the form of 'R_G_B'
BASAL_DENDRITES_COLOR=0_0_0

# Apical dendrite RGB color in the form of 'R_G_B'
APICAL_DENDRITE_COLOR=0_0_0

# Spines RGB color in the form of 'R_G_B'
SPINES_COLOR=1_0_0

# Nucleus RGB color in the form of 'R_G_B'
NUCLEUS_COLOR=0_0_0

# Articulations color RGB in the form of 'R_G_B', for example '1.0_0.5_0.25' or '255_128_64'
# This color is applied only for 'articulated-sections'
ARTICULATIONS_COLOR=50_115_182

# Shader, refer to the documentation to see all the shading modes and some examples
# Use ['lambert']
# Use ['electron-light']
# Use ['electron-dark']
# Use ['super-electron-light']
# Use ['super-electron-dark']
# Use ['shadow']
# Use ['sub-surface-scattering']
# Use ['flat']
SHADER=flat

####################################################################################################
# RENDERING PARAMETERS
####################################################################################################
# Render soma profile skeleton in the XY plane, 'yes/no'
RENDER_SOMA_SKELETON=no

# Render a static frame of the final reconstructed soma mesh only, 'yes/no'
RENDER_SOMA_MESH=no

# Render a sequence of frames reflecting the progressive reconstruction of the soma mesh, 'yes/no'
RENDER_SOMA_MESH_PROGRESSIVE=no

# Render a 360 sequence of the final reconstructed soma mesh, 'yes/no'
RENDER_SOMA_MESH_360=no

# Render a static frame of the reconstructed morphology, 'yes/no'
RENDER_NEURON_MORPHOLOGY=no

# Render a 360 sequence of the reconstructed morephology skeleton, 'yes/no'
RENDER_NEURON_MORPHOLOGY_360=no

# Render a sequence of frames reflecting the progressive reconstruction of the skeleton, 'yes/no'
RENDER_NEURON_MORPHOLOGY_PROGRESSIVE=no

# Render a static frame of the reconstructed mesh of the neuron, 'yes/no'
RENDER_NEURON_MESH=yes

# Render a 360 sequence of the reconstructed neuron mesh, 'yes/no'
RENDER_NEURON_MESH_360=no

# The rendering view
# Use ['wide-shot'] to render the whole view (wide-shot) of the morphology including all of its arbors
# Use ['mid-shot'] to render the reconstructed components only
# Use ['close-up'] to render a close-up around the soma with a given dimensions
RENDERING_VIEW=mid-shot

# Renders a frame to scale that is a factor of the largest dimension of the morphology, 'yes/no'
RENDER_TO_SCALE=no

# Frame resolution, only used if RENDER_TO_SCALE is set to no
FULL_VIEW_FRAME_RESOLUTION=2048

# Frame scale factor (only in case of RENDER_TO_SCALE is set to yes), default 1.0
FULL_VIEW_SCALE_FACTOR=10.0

# Close up frame resolution
CLOSE_UP_FRAME_RESOLUTION=1024

# Close up view dimensions (in microns)
CLOSE_UP_VIEW_DIMENSIONS=25

# Camera view
# Use ['front'] for the front view
# Use ['side'] for the side view
# Use ['top'] for the top view
CAMERA_VIEW=front

####################################################################################################
# ANALYSIS PARAMETERS
####################################################################################################
# Analyse the morphology skeleton, 'yes/no'
ANALYZE_MORPHOLOGY_SKELETON=no
```
