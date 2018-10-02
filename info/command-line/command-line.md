# Command Line Options

_NeuroMorphoVis_  

## Options

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

<p align="left">
  <img src="images/blender-logo.png">
</p>

Depending on your operating system, but assuming a UNIX-based one, Blender can be  
+ installed as a system package, 
+ or downloaded directly from this [repository](http://download.blender.org/release/).

### Installing Blender as a System Package

On __Ubuntu__, Blender can be installed from the terminal as follows 
```
$ sudo apt-get install blender
```

On __RedHat__, Blender can be installed from the terminal as follows
```
sudo yum install blender
```

__NOTE__: If blender is installed as a system package, then all the addons (or plug-ins) must be loaded from the following directory
```
$HOME/.config/blender/2.XX/scripts/addons
```
where XX is the major and minor versions of Blender that is installed on your machine. In certain cases, you can have multiple versions installed at the same moment, so if you list this directory ``` $ ls $HOME/.config/blender/```, you might find multiple directories that correspond to each version of Blender that is installed on your machine. In this case, the user must be cautious to avoid installing NeuroMorphoVis in the wrong directory. 
```
$ ls $HOME/.config/blender/ -ls 
2.76
2.77
2.78
2.79
```

If this is the first time you install Blender, it is advised to launch Blender by typing the command ```blender ``` in your terminal to ensure its proper installation. If you see a similar image to the one below, then Blender is installed successfully. 

<p align="center">
  <img src="images/blender-interface.png">
</p>

### Downloading Blender 
Blender can be also downloaded for all the operating systems from this [repository](http://download.blender.org/release/). NeuroMorphoVis is tested on the following Blender versions 
+ [Blender 2.76](http://download.blender.org/release/Blender2.76/)
+ [Blender 2.78](http://download.blender.org/release/Blender2.78/)
+ [Blender 2.79](http://download.blender.org/release/Blender2.79/)

#### Example 
+ Download Blender version [2.78c](http://download.blender.org/release/Blender2.78/blender-2.78c-linux-glibc219-x86_64.tar.bz2) into your home directory.
```
$ cd $HOME
$ wget http://download.blender.org/release/Blender2.78/blender-2.78c-linux-glibc219-x86_64.tar.bz2
```

+ Extract the tar file and change the directory name to avoid confusion
```
$ tar xvf blender-2.78c-linux-glibc219-x86_64.tar.bz2 
$  mv blender-2.78c-linux-glibc219-x86_64 blender
```






All the different versions of Blender can be downloaded from  You can also install Blender 

+ Download Blender from this [repository](http://download.blender.org/release/Blender2.78/).
+ Extract the file. 
+ Open the Blender folder 
+ Go to the addons directory 

```bash
BLENDER
├── 2.78
    ├── scripts 
        ├── addons
```
 + Clone the NeuroMorphoVis repository using the following command 
 
 ```
 git clone 
 ```
 
 + Open Blender 
 ```
 cd BLENDER_DIRECTORY 
 ./blender 
 ```
 

## Summary
Use the input / output panel to set the input files and the output directories where the results will be generated.    

## Linux
The current version of NeuroMorphoVis can read morphologies stored in the following file formats:
+ The standard [.SWC](http://www.neuronland.org/NLMorphologyConverter/MorphologyFormats/SWC/Spec.html) file format. 
+ [H5](https://developer.humanbrainproject.eu/docs/projects/morphology-documentation/0.0.2/index.html) file format. This format is specific to the Blue Brain Project / Human Brain Projects, but the python bindings of HDF5 library must be installed to the system to load it.   

## Mac 
+ The users can load morphologies from individual .SWC or .H5 files based on their absolute pathes in the file system. In this case, the __Input Source__ option should be set to __H5 or SWC File__, and the path to the morphology file should be set in the __Morphology File__ text box. You can also use the button on the right of the text box to open a file dialog and select the file from a specific path.

<p align="center">
  <img src="images/io-1.png">
</p>

+ The users can also load a morphology of a certain neuron reconstructed in a BBP circuit using its GID. In this case, the __Input Source__ option should be set to __BBP Circuit (GID)__, and then the path to the circuit configuration should be set in the __Circuit File__ text box (replace __Select Circuit File__ by the absolute path of the circuit, for example: /gpfs/WHATEVER_PROJECT/config.circuit) and the GID of the neuron should be set in the __GID__ field (replace __Add a GID__ by the GID of the neuron, for example: 1000).  

<p align="center">
  <img src="images/io-2.png">
</p>

## Windows
NeuroMorphoVis can be only used to load and visualize morphologies. But if the users would like create any output, for example images, videos or meshes, then the __Output Directory__, where there artifacts will be generated, __must__ be set (replace __Select Directory__ by the absolute path of the output directory).

#### Output Tree
When the output directory is created, it automatically creates a list of subdirectories, each of them will contain a specific type of output. The default structure of the out directory is as follows 

```bash
OUTPUT_DIRECTORY
├── images
├── sequences
├── meshes
├── morphologies
├── analysis



```

If the user wants to change the name any of these subdirectories, then the checkbox __Use Default Output Paths__ must be unchecked. 

<p align="center">
  <img src="images/io-3.png">
</p>

To use NeuroMorphoVis, you must have a recent version of Blender installed on your system. To verify this: 
+ Open a terminal and type ``` blender```. 
+ If you get this message ```command not found: blender```, then you must install blender using the package manager or by downloading it from the [Blender repository](http://download.blender.org/release/).
+ You can use the package manager of Ubunut to install Blender using this command 
``` sudo apt-get install blender ```

NeuroMorphoVis is tested to work with Blender versions [2.78](http://download.blender.org/release/Blender2.78/) and [2.79](http://download.blender.org/release/Blender2.79/).

If Blender is already installed, you will get the following message 
```
Reading package lists... Done
Building dependency tree       
Reading state information... Done
blender is already the newest version (2.79.b+dfsg0-1).
0 upgraded, 0 newly installed, 0 to remove and 104 not upgraded.
```

Tutorial (Python  Scripting ... )
Users who have python programming experience can also use NeuroMorphoVis API to write their customized scripts to generate high quality images and videos of the loaded morphologies.  
