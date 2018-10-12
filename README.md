# NeuroMorphoVis
![](docs/artifacts/logo/neuromorphovis-logo.png "NeuroMorphoVis")



[![Say Thanks](https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg)](https://saythanks.io/to/marwan-abdellah)
[![GitHub Stars](https://img.shields.io/github/stars/BlueBrain/NeuroMorphoVis.svg)](https://github.com/BlueBrain/NeuroMorphoVis/stargazers)



## Introduction

_NeuroMorphoVis_ is an interactive, extensible and cross-platform framework for building, visualizing and analyzing digital reconstructions of neuronal morphology skeletons extracted from microscopy stacks. The framework is capable of detecting and repairing several tracing artifacts, allowing the generation of high fidelity surface meshes and high resolution volumetric models for simulation and _in silico_ studies. 

## Features

_NeuroMorphoVis_ provides four major toolboxes that can be used for 

+ Automated analysis of neuronal morphology skeletons that are digitally reconstructed from optical microscopy stacks. 
+ An easy context to load broken morphology skeletons and repair them manually. 
+ Sketching and building three-dimensional representations of the morphology skeletons using various methods for visual analytics. 
+ Automated reconstruction of accurate three-dimensional somata profiles, even with classical morphology skeletons that do not have any three-dimensional data of their somata. This approach uses the physics engine of Blender based on Hooke's law and mass spring models.
+ Automated reconstruction of polygonal mesh models that represent the membranes of the neuronal morphologies based on the piecewise meshing method presented by [Abdellah et al., 2017](https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-017-1788-4).
+ Automated generation of high quality media for scientific documents and publications using different shading styles and materials. 
+ Multiple interfaces: user-friendly graphical user interface, a rich command line interface, editable configuration files and a high level python API for python scripting.
+ Importing morphologies in multiple file formats including [SWC](http://www.neuronland.org/NLMorphologyConverter/MorphologyFormats/SWC/Spec.html), [H5](https://developer.humanbrainproject.eu/docs/projects/morphology-documentation/0.0.2/index.html) or even from a [BBP circuit](https://portal.bluebrain.epfl.ch/resources/models/microcircuits-2/) using GIDs and cell targets. 
+ Exporting the reconstructed meshes in several file formats including [PLY](https://en.wikipedia.org/wiki/PLY_(file_format)), [OBJ](https://en.wikipedia.org/wiki/Wavefront_.obj_file), [STL](https://en.wikipedia.org/wiki/STL_(file_format)) and also as a Blender file ([.blend](https://en.wikipedia.org/wiki/Blender_(software)#File_format)).
+ Parallel batch processing on multi-node visualization clusters using [SLURM workload manager](https://slurm.schedmd.com/). 

## Interfaces

_NeuroMorphoVis_ is primarily designed as a plug-in in [Blender](https://www.blender.org/). It comes with a user-friendly GUI and a rich set of command line options. Moreover, the tool is configurable via input configuration files making it possible to link it to web interface or using it on massively parallel visualization clusters for batch production. 

The tool is also extensible via its powerful python API that can be imported in Blender console and text browser. 

### GUI

To make it accessible to end users with minimal programming knowledge or even with no programming experience at all, the core functionality of _NeuroMorphoVis_ is exposed to users via a friendly graphical user interface that would allow them to navigate and adjust the parameters of the different toolboxes seamlessly. A detailed guide to use NeuroMorphoVis from its GUI is available in this [user guide](docs/user/modules/gui/gui.md).

<figure align="center">
<img src="docs/artifacts/interface-images/interface.png">
<figcaption>A screen shot of a neuronal morphology skeleton reconstructed by  NeuroMorphoVis and sketched in the 3D view port of Blender. Note that the neurites are tagged with different colors (green for apical dendrite, red for basal dendrites and blue for the axon) and the soma (in orange) is reconstructed as a realistic three-dimensional profile not as a sphere.</figcaption>
</figure>

### Command Line Options

_NeuroMorphoVis_ has a rich command line interface that would make it easy to connect it to a web interface or use it to accomplish multiple tasks in an automated way. A list of all the command line options and their description are available in this [user guide](docs/user/modules/cli/cli.md).

### Configuration Files 

Users can easily configure and use _NeuroMorphoVis_ via editable configuration files. Instructions to write and use configurations files are available in this [user guide](docs/user/modules/configurations/configurations.md).

## Download 

_NeuroMorphoVis_ is mainly based on [Blender](https://www.blender.org/). Blender is a free software and can be downloaded from this [page](http://download.blender.org/release/). Blender is released under the GNU General Public License ([GPL](https://www.blender.org/about/license/), or “free software”).
The current version is compatible with the following Blender versions:

+ [Blender 2.76](http://download.blender.org/release/Blender2.76/): 2.76a and 2.76b
+ [Blender 2.77](http://download.blender.org/release/Blender2.77/): 2.77 and 2.77a
+ [Blender 2.78](http://download.blender.org/release/Blender2.78/): 2.78, 2.78a, 2.78b and 2.78c
+ [Blender 2.79](http://download.blender.org/release/Blender2.79/): 2.79, 2.79a, 2.79b and 2.79c 

_NeuroMorphoVis_ can be downloaded as a __binary archive bundled within Blender__ that can be easily extracted and used without installing any further dependencies. The optional dependencies are already shiped within this archive using [pip](https://pypi.org/project/pip/) on each respective operating system.    

### Supported Platforms 

A binary package of the current version of _NeuroMorphoVis_ __is shipped with Blender version 2.79__ for the followign platforms:

+ __Ubuntu__ Release [1.0.0](https://github.com/BlueBrain/NeuroMorphoVis/releases/tag/v1.0.0) is available from this [link](https://github.com/BlueBrain/NeuroMorphoVis/releases/download/v1.0.0/neuromorphovis-1.0.0-blender-2.79b-linux-x86_64.zip).

+ __Red Hat__ Release [1.0.0](https://github.com/BlueBrain/NeuroMorphoVis/releases/tag/v1.0.0) is available from this [link](https://github.com/BlueBrain/NeuroMorphoVis/releases/download/v1.0.0/neuromorphovis-1.0.0-blender-2.79b-linux-x86_64.zip).

+ __Mac OS__ Release [1.0.0](https://github.com/BlueBrain/NeuroMorphoVis/releases/tag/v1.0.0) is available from this [link](https://github.com/BlueBrain/NeuroMorphoVis/releases/download/v1.0.0/neuromorphovis-blender-2.79-macOS-10.6.zip).

+ __Windows__ Release [1.0.0](https://github.com/BlueBrain/NeuroMorphoVis/releases/tag/v1.0.0) is available from this [link](https://github.com/BlueBrain/NeuroMorphoVis/releases/download/v1.0.0/neuromorphovis-1.0.0-blender-2.79-windows64.zip).

### Sample Morphologies 

To test the software, a set of sample morphology files (in SWC and H5 formats) are available to download from this [link](https://github.com/BlueBrain/NeuroMorphoVis/releases/download/v1.0.0/sample-morphologies.zip).

## How to Use

_NeuroMorphoVis_ can be used from the GUI of Blender. This is the easiest and most recommended approach to use. For systems without an X server, _NeuroMorphoVis_ can be executed in the background mode (similar to ```blender -b```) using the command line interface. For batch processing of multiple morphology files, the editable configuration files are provided. The python API can be also used to write plugins for high quality media production. 

### GUI
The user guide of the GUI is available in this [link](docs/user/modules/gui/gui.md). In the following section, we provde a few video tutorials to show how to use the interface seamlessly. 

### Command Line Interface 
The user guide of the command line interface is available in this [link](docs/user/modules/cli/cli.md). 

### Configuration Files 
The configuration file user guide is available in this [link](docs/user/modules/configurations/configurations.md). 

### Python API 

We are currently writing a detailed documentation to use the python API. If you are interested to collaborate with us to extend _NeuroMorphoVis_ to fit your applications, please contact [marwan.abdellah@epfl.ch](marwan.abdellah@epfl.ch).

## Installation 

The end users are recommended to download the archives from the links provided in the previous section. But if the users are willing to contribute and extend _NeuroMorphoVis_, we recommend to install it as described in this [installation guide](docs/user/installation/install.md).

## Highlights 

### Features 

#### Neuronal Soma Reconstruction 

A demonstration of using the _Soma Reconstruction_ toolbox to reconstruct a three-dimensional profile of the soma of a pyramidal cell morphology using Hooke's law and mass spring models.

<p align="center">
<a href="https://www.youtube.com/watch?v=v02HogkFODU">
	<img src="docs/artifacts/interface-images/soma-reconstruction.png">
</a>
</p>

#### Neuronal Morphology Visualization 

Using the _Morphology Reconstruction_ toolbox to create a three-dimensional model of a morphology skeleton.

<p align="center">
<a href="https://www.youtube.com/watch?v=74PGirMx3ks&t=102s">
	<img src="docs/artifacts/interface-images/morphology-reconstruction.png">
</a>
</p>

#### Neuronal Mesh Reconstruction 

Using the _Mesh Reconstruction_ toolbox to generate a piecewise watertight mesh model of a given morphology skeleton. 
  
<p align="center">
<a href="https://www.youtube.com/watch?v=oxCKwrZSV98&t=130s">
	<img src="docs/artifacts/interface-images/mesh-generation.png">
</a>
</p>

### Gallery 

<p align="center">
	<img src="docs/artifacts/renderings/dancing-neuron.jpeg" width=400>
	<img src="docs/artifacts/renderings/scary-neuron.jpeg" width=400>
</p>

<p align="center">
	<img src="docs/artifacts/renderings/fluorescent-neuron.jpeg" width=400>
	<img src="docs/artifacts/renderings/golgi-staining-neuron.jpeg" width=400>
</p>

<p align="center">
	<img src="docs/artifacts/renderings/somata-ncc.jpeg" width=850>
</p>


## Known Bugs or Feature Requests

Please refer to the [github issue tracker](https://github.com/BlueBrain/NeuroMorphoVis/issues?utf8=%E2%9C%93&q=) for fixed and open bugs, and also to report new bugs and to request new features that you need in your research.


## Publication & Citation 

If you use _NeuroMorphoVis_ for your research, media design or other purposes, please cite our paper [NeuroMorphoVis: a collaborative framework for analysis and visualization of neuronal morphology skeletons reconstructed from microscopy stacks](https://academic.oup.com/bioinformatics/article/34/13/i574/5045775) using the following entry:

```
@article{abdellah2018neuromorphovis,
  title={NeuroMorphoVis: a collaborative framework for analysis and visualization of neuronal morphology 
  skeletons reconstructed from microscopy stacks},
  author={Abdellah, Marwan and Hernando, Juan and Eilemann, Stefan and Lapere, Samuel and Antille, 
  Nicolas and Markram, Henry and Sch{\"u}rmann, Felix},
  journal={Bioinformatics},
  volume={34},
  number={13},
  pages={i574--i582},
  year={2018},
  publisher={Oxford University Press}
}
```

The supplementary material of this paper is also available in this [document](docs/artifacts/papers/abdellah-et-al-2018-supplementary.pdf).

The core algorithms of the soma and mesh reconstruction modules are described in this paper [Reconstruction and visualization of large-scale volumetric models of neocortical circuits for physically-plausible in silico optical studies](https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-017-1788-4)

```
@article{abdellah2017reconstruction,
  title={Reconstruction and visualization of large-scale volumetric models of neocortical circuits 
  for physically-plausible in silico optical studies},
  author={Abdellah, Marwan and Hernando, Juan and Antille, Nicolas and Eilemann, Stefan and 
  Markram, Henry and Sch{\"u}rmann, Felix},
  journal={BMC bioinformatics},
  volume={18},
  number={10},
  pages={402},
  year={2017},
  publisher={BioMed Central}
}
```

The applications of _NeuroMorhoVis_ are deomnstrated in the thesis [In silico Brain Imaging: Physically-plausible Methods for Visualizing Neocortical Microcircuitry](https://infoscience.epfl.ch/record/232444?ln=en)

```
@phdthesis{abdellah2017insilico:232444,
  title = {In Silico Brain Imaging Physically-plausible Methods for Visualizing 
  Neocortical Microcircuitry},
  author = {Abdellah, Marwan},
  publisher = {EPFL},
  address = {Lausanne},
  pages = {400},
  year = {2017}
}

```

## Acknowledgement
_NeuroMorphoVis_ is developed by the Visualization team at the [Blue Brain Project](https://bluebrain.epfl.ch/page-52063.html), [Ecole Polytechnique Federale de Lausanne (EPFL)](https://www.epfl.ch/) as part of [Marwan Abdellah's](http://marwan-abdellah.com/) [PhD (In silico Brain Imaging: Physically-plausible Methods for Visualizing Neocortical Microcircuitry)](https://infoscience.epfl.ch/record/232444?ln=en). Financial support was provided by competitive research funding from [King Abdullah University of Science and Technology (KAUST)](https://www.kaust.edu.sa/en).

## License 
_NeuroMorphoVis_ is available to download and use under the GNU General Public License ([GPL](https://www.gnu.org/licenses/gpl.html), or “free software”).

## Attributions 

* [Blender](https://www.blender.org/) (C) is copyright to Blender Foundation. The Blender Foundation is a non-profit organization responsible for the development of Blender. Blender is released under the GNU Public License, as Free Software, and therefore can be distributed by anyone freely. 

* [Slurm](slurm.schedmd.com), is a free and open-source job scheduler for Linux and Unix-like kernels, used by many of the world's supercomputers and computer clusters. Slurm is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation.

* The SWC morphology samples are available from [NeuroMorpho.Org](http://neuromorpho.org/). NeuroMorpho.Org is a centrally curated inventory or repository of digitally reconstructed neurons associated with peer-reviewed publications.

* The H5 morphology samples are available with permissions from the [Blue Brain Project](https://bluebrain.epfl.ch/page-52063.html), [Ecole Polytechnique Federale de Lausanne (EPFL)](https://www.epfl.ch/). 

## Contact

For more information on NeuroMorphoVis, comments or suggestions, please contact:

__Marwan Abdellah__  
Scientific Visualiation Engineer  
Blue Brain Project  
[marwan.abdellah@epfl.ch](marwan.abdellah@epfl.ch) 
 
__Samuel Lapere__  
Section Manager, Visualization  
Blue Brain Project  
[samuel.lapere@epfl.ch](samuel.lapere@epfl.ch) 

Should you have any questions concerning press enquiriries, please contact:

__Kate Mullins__  
Communications  
Blue Brain Project  
[kate.mullins@epfl.ch](kate.mullins@epfl.ch)

<p align="center">
	<img src="docs/artifacts/logo/epfl-logo.jpg" width=200>
</p>
