# Command Line Options User Guide

_NeuroMorphoVis_ can be executed in the background mode from the command line usign the ```neuromorphovis.py``` script. 

## Options

The full list of the command line options is shown below. 

```
$ ./neuromorphovis.py -h
usage: neuromorphovis.py [-h] [--blender BLENDER] [--input INPUT]
                         [--morphology-file MORPHOLOGY_FILE]
                         [--morphology-directory MORPHOLOGY_DIRECTORY]
                         [--gid GID] [--target TARGET]
                         [--blue-config BLUE_CONFIG]
                         [--output-directory OUTPUT_DIRECTORY]
                         [--soma-stiffness SOMA_STIFFNESS]
                         [--soma-subdivision-level SOMA_SUBDIVISION_LEVEL]
                         [--reconstruct-morphology-skeleton]
                         [--morphology-reconstruction-algorithm MORPHOLOGY_RECONSTRUCTION_ALGORITHM]
                         [--morphology-skeleton MORPHOLOGY_SKELETON]
                         [--soma-representation SOMA_REPRESENTATION]
                         [--ignore-axon] [--ignore-basal-dendrites]
                         [--ignore-apical-dendrites]
                         [--axon-branching-order AXON_BRANCHING_ORDER]
                         [--apical-dendrites-branching-order APICAL_DENDRITES_BRANCHING_ORDER]
                         [--basal-dendrites-branching-order BASAL_DENDRITES_BRANCHING_ORDER]
                         [--sections-radii SECTIONS_RADII]
                         [--radii-scale-factor RADII_SCALE_FACTOR]
                         [--fixed-section-radius FIXED_SECTION_RADIUS]
                         [--bevel-sides BEVEL_SIDES] [--spines SPINES]
                         [--spines-quality SPINES_QUALITY]
                         [--random-spines-percentage RANDOM_SPINES_PERCENTAGE]
                         [--add-nucleus] [--soma-color SOMA_COLOR]
                         [--axon-color AXON_COLOR]
                         [--basal-dendrites-color BASAL_DENDRITES_COLOR]
                         [--apical-dendrites-color APICAL_DENDRITES_COLOR]
                         [--spines-color SPINES_COLOR]
                         [--nucleus-color NUCLEUS_COLOR]
                         [--articulation-color ARTICULATION_COLOR]
                         [--shader SHADER] [--reconstruct-soma-mesh]
                         [--reconstruct-neuron-mesh]
                         [--meshing-algorithm MESHING_ALGORITHM]
                         [--edges EDGES] [--surface SURFACE]
                         [--branching BRANCHING]
                         [--tessellation-level TESSELLATION_LEVEL]
                         [--global-coordinates] [--export-morphology-swc]
                         [--export-morphology-h5] [--export-morphology-blend]
                         [--export-neuron-mesh-ply] [--export-neuron-mesh-obj]
                         [--export-neuron-mesh-stl]
                         [--export-neuron-mesh-blend] [--export-soma-mesh-ply]
                         [--export-soma-mesh-obj] [--export-soma-mesh-stl]
                         [--export-soma-mesh-blend]
                         [--render-neuron-morphology]
                         [--render-neuron-morphology-360]
                         [--render-neuron-morphology-progressive]
                         [--render-soma-skeleton] [--render-soma-mesh]
                         [--render-soma-mesh-360]
                         [--render-soma-mesh-progressive]
                         [--render-neuron-mesh] [--render-neuron-mesh-360]
                         [--render-to-scale] [--rendering-view RENDERING_VIEW]
                         [--camera-view CAMERA_VIEW]
                         [--close-up-dimensions CLOSE_UP_DIMENSIONS]
                         [--full-view-resolution FULL_VIEW_RESOLUTION]
                         [--close-up-resolution CLOSE_UP_RESOLUTION]
                         [--resolution-scale-factor RESOLUTION_SCALE_FACTOR]
                         [--execution-node EXECUTION_NODE]
                         [--number-cores NUMBER_CORES]
                         [--job-granularity JOB_GRANULARITY]
                         [--analyze-morphology]

NeuroMorphoVis: a collaborative framework for analysis and visualization of
	morphological skeletons reconstructed from microscopy stacks

optional arguments:
  -h, --help            show this help message and exit

Blender:
  Blender

  --blender BLENDER     Blender executable
                        Default: blender, system installed: sudo apt-get install blender

Input:
  Input

  --input INPUT         Input morphology sources.
                        Options: ['gid', 'target', 'file', 'directory']
  --morphology-file MORPHOLOGY_FILE
                        Morphology file (.H5 or .SWC)
  --morphology-directory MORPHOLOGY_DIRECTORY
                        Morphology directory containing (.H5 or .SWC) files
  --gid GID             Cell GID (requires BBP circuit).
  --target TARGET       Cell target in target file (requires BBP circuit).
  --blue-config BLUE_CONFIG
                        BBP circuit configuration

Output:
  Output

  --output-directory OUTPUT_DIRECTORY
                        Root output directory

Soma:
  Soma

  --soma-stiffness SOMA_STIFFNESS
                        Soma surface stiffness (0.001 - 0.999).
                        Default 0.25.
  --soma-subdivision-level SOMA_SUBDIVISION_LEVEL
                        Soma surface subdivision level, between (3-7).
                        Default 5.

Morphology Skeleton:
  Morphology Skeleton

  --reconstruct-morphology-skeleton
                        Reconstruct morphology skeleton for visualization or analysis.
  --morphology-reconstruction-algorithm MORPHOLOGY_RECONSTRUCTION_ALGORITHM
                        Morphology reconstruction algorithm.
                        Options: ['connected-sections',
                        	  '(connected-sections-repaired)',
                        	  'disconnected-sections',
                        	  'disconnected-segments',
                        	  'articulated-sections']
  --morphology-skeleton MORPHOLOGY_SKELETON
                        Morphology skeleton style.
                        Options: ['(original)', 'tapered', 'zigzag', 'tapered-zigzag']
  --soma-representation SOMA_REPRESENTATION
                        Soma representation in the reconstructed morphology.
                        Options ['ignore', 'sphere', '(profile)']
  --ignore-axon         Ignore reconstructing the axon.
  --ignore-basal-dendrites
                        Ignore reconstructing basal dendrites.
  --ignore-apical-dendrites
                        Ignore reconstructing apical dendrites.
  --axon-branching-order AXON_BRANCHING_ORDER
                        Maximum branching order for the axon (1, infinity).
                        Default 5.
  --apical-dendrites-branching-order APICAL_DENDRITES_BRANCHING_ORDER
                        Maximum branching order for the basal dendrites (1, infinity).
                        Default infinity.
  --basal-dendrites-branching-order BASAL_DENDRITES_BRANCHING_ORDER
                        Maximum branching order for the apical dendrite (1, infinity).
                        Default infinity.
  --sections-radii SECTIONS_RADII
                        The radii of the morphological sections.
                        Options: ['(default)', 'scaled', 'fixed']
  --radii-scale-factor RADII_SCALE_FACTOR
                        A scale factor used to scale the radii of the morphology.
                        Valid only if --sections-radii = scaled.
                        Default is 1.0
  --fixed-section-radius FIXED_SECTION_RADIUS
                        A fixed radius for all morphology sections.
                        Valid only if --sections-radii = fixed.
                        Default is 1.0
  --bevel-sides BEVEL_SIDES
                        Number of sides of the bevel object used to reconstruct the morphology.
                        Default 16 (4: low quality - 64: high quality)

Spines - Nucleus:
  Spines - Nucleus

  --spines SPINES       Build the spines and integrate them with the mesh.
                        Options: ['(ignore)', 'circuit', 'random']
  --spines-quality SPINES_QUALITY
                        The quality of the spine meshes.
                        Options: ['(lq)', 'hq']
  --random-spines-percentage RANDOM_SPINES_PERCENTAGE
                        The percentage of the spines that are added randomly (0-100).
                        Default 50.
  --add-nucleus         Add nucleus mesh.

Materials - Colors:
  Materials - Colors

  --soma-color SOMA_COLOR
                        Soma color
  --axon-color AXON_COLOR
                        Axon color
  --basal-dendrites-color BASAL_DENDRITES_COLOR
                        Basal dendrites color
  --apical-dendrites-color APICAL_DENDRITES_COLOR
                        Apical dendrite color
  --spines-color SPINES_COLOR
                        Spines color
  --nucleus-color NUCLEUS_COLOR
                        Nucleus color
  --articulation-color ARTICULATION_COLOR
                        Articulations color.
                        Valid only for the articulated-sections.
                        Default Yellow.
  --shader SHADER       Shading mode or material.
                        Options: (lambert)
                        	 electron-light
                        	 electron-dark
                        	 super-electron-light
                        	 super-electron-dark
                        	 shadow
                        	 flat
                        	 subsurface-scattering

Meshing:
  Meshing

  --reconstruct-soma-mesh
                        Reconstruct the mesh of the soma only.
  --reconstruct-neuron-mesh
                        Reconstruct the mesh of the entire neuron.
  --meshing-algorithm MESHING_ALGORITHM
                        Meshing algorithm.
                        Options: ['(piecewise-watertight)', 'union', 'bridging']
  --edges EDGES         Arbors edges.
                        This option only applies to the meshes.
                        Options: ['smooth', '(hard)']
  --surface SURFACE     The surface roughness of the neuron mesh.
                        Options: ['rough', '(smooth)']
  --branching BRANCHING
                        Arbors branching based on angles or radii.
                        Options : ['angles', '(radii)']
  --tessellation-level TESSELLATION_LEVEL
                        Mesh tessellation factor between (0.1, 1.0).
                        Default 1.0.
  --global-coordinates  Export the mesh at global coordinates.
                        Valid only for BBP circuits.

Export Options:
  You can export morphology skeletons or reconstructed meshes in various
  file formats.

  --export-morphology-swc
                        Exports the morphology to (.SWC) file.
  --export-morphology-h5
                        Exports the morphology to (.H5) file.
  --export-morphology-blend
                        Exports the morphology as a Blender file (.BLEND).
  --export-neuron-mesh-ply
                        Exports the neuron mesh to (.PLY) file.
  --export-neuron-mesh-obj
                        Exports the neuron mesh to (.OBJ) file.
  --export-neuron-mesh-stl
                        Exports the neuron mesh to (.STL) file.
  --export-neuron-mesh-blend
                        Exports the neuron mesh as a Blender file (.BLEND).
  --export-soma-mesh-ply
                        Exports the soma mesh to a (.PLY) file.
  --export-soma-mesh-obj
                        Exports the soma mesh to a (.OBJ) file.
  --export-soma-mesh-stl
                        Exports the soma mesh to a (.STL) file.
  --export-soma-mesh-blend
                        Exports the soma mesh to a Blender file (.BLEND).

Rendering:
  Rendering

  --render-neuron-morphology
                        Render image of the morphology skeleton.
  --render-neuron-morphology-360
                        Render a 360 sequence of the morphology skeleton.
  --render-neuron-morphology-progressive
                        Render a progressive reconstruction of the morphology skeleton.
  --render-soma-skeleton
                        Render a static image of the soma skeleton (connected profile).
  --render-soma-mesh    Render an image of the reconstructed soma mesh.
  --render-soma-mesh-360
                        Render a 360 sequence of the reconstructed soma mesh.
  --render-soma-mesh-progressive
                        Render a sequence of the progressive reconstruction of the soma mesh.
  --render-neuron-mesh  Render an image of the reconstructed neuron mesh.
  --render-neuron-mesh-360
                        Render a 360 sequence of the reconstructed neuron mesh.
  --render-to-scale     Render the skeleton to scale.
  --rendering-view RENDERING_VIEW
                        The rendering view of the skeleton for the skeleton.
                        Options: ['close-up', 'mid-shot', '(wide-shot)']
  --camera-view CAMERA_VIEW
                        The camera direction.
                        Options: ['(front)', 'side', 'top']
  --close-up-dimensions CLOSE_UP_DIMENSIONS
                        Close up dimensions (the view around the soma in microns).
                        Valid only when the --rendering-view = close-up.
                        Default 20.
  --full-view-resolution FULL_VIEW_RESOLUTION
                        Base resolution of full view images (wide-shot or mid-shot).
                        Default 1024.
  --close-up-resolution CLOSE_UP_RESOLUTION
                        Base resolution of close-up images.
                        Valid only when the --rendering-view = close-up.
                        Default 512.
  --resolution-scale-factor RESOLUTION_SCALE_FACTOR
                        A factor used to scale the resolution of the image.
                        Valid only if --render--to-scale is set.
                        Default 1.

Execution:
  Execution

  --execution-node EXECUTION_NODE
                        Execution is local or using cluster nodes.
                        Options: ['(local)', 'cluster']
  --number-cores NUMBER_CORES
                        Number of execution cores on cluster.
                        Default 256.
  --job-granularity JOB_GRANULARITY
                        The granularity of the jobs running on the cluster.
                        Options: ['high', '(low)']

Analysis:
  Analysis

  --analyze-morphology  Analyze the morphology skeleton and report the artifacts.
```
 
## Basic Command 

To run _NeuroMorphoVis_ on a single morphology that is specified by a GID in a circuit, the user must set the ```--input``` option to ```gid``` and specify the circuit by a circuit configuration file using the option ```--blue-config```.  

```
neuromorphovis.py \
	--input=gid --blue-config=BLUE_CONFIG_FILE --gid=NEURON_GID \
	--output=OUTPUT_DIRECTORY 
```

_NeuroMoprhoVis_ can be used to process multiple morphology files grouped in a cell target if the user sets the ```--input``` to ```target``` and then specifies the target in the ```--target``` option. 


```
neuromorphovis.py \
	--input=target --blue-config=BLUE_CONFIG_FILE --target=CELL_TARGET \
	--output=OUTPUT_DIRECTORY 
```


```
neuromorphovis.py \
	--input=file --morphology-file=MORPHOLOGY_FILE \
	--output=OUTPUT_DIRECTORY 
```

```
neuromorphovis.py \
	--input=directory --morphology-directory=MORPHOLOGY_DIRECTORY \
	--output=OUTPUT_DIRECTORY 
```
