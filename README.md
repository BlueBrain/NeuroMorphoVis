[![DOI](https://zenodo.org/badge/DOI/10.1093/bib.bty231.svg)](https://doi.org/10.1093/bioinformatics/bty231)

<p align="center">
  <img src="https://github.com/BlueBrain/NeuroMorphoVis/wiki/images/logos/nmv-banner.jpeg" width=1200>
</p>

# Introduction
## Features

+ Automated analysis of neuronal morphology skeletons that are digitally reconstructed from optical microscopy stacks. 
+ An easy context to load broken morphology skeletons and repair them manually. 
+ Sketching and building three-dimensional representations of the morphology skeletons using various methods for visual analytics. 
+ Dendrogram visualization and rendering.
+ Visualization of spines and synapses for neuronal morphologies of digitally reconstructed BBP circuits using BluePy.
+ Automated reconstruction of accurate three-dimensional somata profiles, even with classical morphology skeletons that do not have any three-dimensional data of their somata. This approach uses the physics engine of Blender based on Hooke's law and mass spring models.
+ Automated reconstruction of polygonal mesh models that represent the membranes of the neuronal morphologies based on the piecewise meshing method presented by [Abdellah et al., 2017](https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-017-1788-4).
+ Accurate mesh reconstruction with metaballs to handle morphologies with irregular and small branching angles.
+ Watertight mesh reconstruction using [voxelization based remeshing](https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/tool_settings/remesh.html) (in Blender 3.0 onwards) for reaction-diffusion simulations [Abdellah et al., 2024](https://academic.oup.com/bib/article/25/5/bbae393/7731493).
+ Automated generation of high quality media for scientific documents and publications using different shading styles and materials. 
+ High fidelity mesh reconstruction based on Skin modifiers as presented by [Abdellah et al., 2019](https://diglib.eg.org/xmlui/handle/10.2312/cgvc20191257).
+ Robust mesh reconstruction of synthetic astroglial cells using Metaballs and implicit geometries [Abdellah et al., 2021](https://academic.oup.com/bioinformatics/article/37/Supplement_1/i426/6319688)
+ Fast mesh reconstruction of spiny neuronal morohologies based on union operators for rendering transparent meshes [Abdellah et al., 2022](https://diglib.eg.org/handle/10.2312/cgvc20221168).
+ Multiple interfaces: user-friendly graphical user interface, a rich command line interface, editable configuration files and a high level python API for python scripting.
+ Importing morphologies in multiple file formats including [SWC](http://www.neuronland.org/NLMorphologyConverter/MorphologyFormats/SWC/Spec.html), [H5](https://developer.humanbrainproject.eu/docs/projects/morphology-documentation/0.0.2/index.html), [Neurolucida ASCII format ](https://docs.arbor-sim.org/en/stable/fileformat/asc.html) or even from a [BBP circuit](https://portal.bluebrain.epfl.ch/resources/models/microcircuits-2/) using GIDs and cell targets. 
+ Exporting the reconstructed meshes in several file formats including [PLY](https://en.wikipedia.org/wiki/PLY_(file_format)), [OBJ](https://en.wikipedia.org/wiki/Wavefront_.obj_file), [STL](https://en.wikipedia.org/wiki/STL_(file_format)) and also as a Blender file ([.blend](https://en.wikipedia.org/wiki/Blender_(software)#File_format)).
+ Parallel batch processing on multi-node visualization clusters using [SLURM workload manager](https://slurm.schedmd.com/). 

# News
+ 09.2024: [Paper](https://academic.oup.com/bib/article/25/5/bbae393/7731493): The [voxelization-based remeshing algorithm](https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/remesh.html) is now published in Oxford Briefing in Bioinformatics, [more information](https://github.com/BlueBrain/NeuroMorphoVis/wiki/Papers).  
+ 05.2023: Blender 3.0 will be no longer supported by _NeuroMorphoVis_ from October 2024. Please use Blender 3.5 or later.
+ 08.2024: Adding support to run on [Windows 10 and Windows 11](https://github.com/BlueBrain/NeuroMorphoVis/wiki/Installation#installation-on-windows-operating-systems).
+ 06.2023: New logo release. 
+ 05.2023: Release 1.9.0
+ 05.2023: Blender 2.79 and 2.8 are no longer supported by _NeuroMorphoVis_.
+ 04.2023: Implementation of the Voxelization-based remeshing to create watertight mesh models of neurons and astrocytes.
+ 03.2023: Adding the [Synaptics panel](https://github.com/BlueBrain/NeuroMorphoVis/wiki/Synaptics) to _NeuroMorphoVis_. 
+ 09.2022: [Paper](https://www.researchgate.net/profile/Marwan-Abdellah/publication/363538092_Meshing_of_Spiny_Neuronal_Morphologies_using_Union_Operators/links/637b320d2f4bca7fd07b7f13/Meshing-of-Spiny-Neuronal-Morphologies-using-Union-Operators.pdf), Generating high fidelity surface meshes of neocortical neurons using skin modifiers, in EG Computer Graphics and Visual Computing (CGVC) 2022, [more information](https://github.com/BlueBrain/NeuroMorphoVis/wiki/Papers).
+ 04.2020: Release [1.4.5](https://github.com/BlueBrain/NeuroMorphoVis/releases/tag/v1.4.5)
+ 09.2019: [Paper](https://diglib.eg.org/handle/10.2312/cgvc20191257): Generating High Fidelity Surface Meshes of Neocortical Neurons using Skin Modifiers, in EG Computer Graphics and Visual Computing (CGVC) 2019, [more information](https://github.com/BlueBrain/NeuroMorphoVis/wiki/Papers).
+ 05.2019: Release [1.3.1](https://github.com/BlueBrain/NeuroMorphoVis/releases/tag/v1.3.1)
+ 03.2019: Release [1.3.0](https://github.com/BlueBrain/NeuroMorphoVis/releases/tag/v1.3.0)
+ 10.2018: Release [1.0.0](https://github.com/BlueBrain/NeuroMorphoVis/releases/tag/v1.0.0)
+ 07.2018: [NeuroMorphoVis' core paper](https://academic.oup.com/bioinformatics/article/34/13/i574/5045775?login=true) is published in Oxford Bioinformatics, [more information](https://github.com/BlueBrain/NeuroMorphoVis/wiki/Papers). 
# Package Details 

_NeuroMorphoVis_ is mainly based on [Blender](https://www.blender.org/). Blender is a free software and can be downloaded from [Blender.org](http://download.blender.org/release/). Blender is released under the GNU General Public License ([GPL](https://www.blender.org/about/license/), or “free software”).
The current version of _NeuroMorphoVis_ is compatible with the following Blender versions:

+ [Blender 3.0](http://download.blender.org/release/Blender3.0/)
+ [Blender 3.5](http://download.blender.org/release/Blender3.5/)
+ [Blender 4.0](http://download.blender.org/release/Blender4.0/)
+ [Blender 4.2](http://download.blender.org/release/Blender4.2/)

Nevertheless, it is recommended to avoid version 2.79 and use version 3.5. 

_NeuroMorphoVis_ can be downloaded as a __binary archive bundled within Blender__ that can be easily extracted and used [out-of-the-box](https://en.wikipedia.org/wiki/Out_of_the_box_(feature)). The optional dependencies are already shiped within this archive using [pip](https://pypi.org/project/pip/) on each respective platform. This package (released every minor version update of the software) is recommended for __Windows users__ or those who cannot use the [__Terminal__](https://en.wikipedia.org/wiki/Unix_shell). Otherwise, users can just download an installation script that will automatically install the entire package to a user-specified directory. This script __does not__ require __sudo__ permissions. 

## Installation 
_NeuroMorphoVis_ can be installed to a user-specified directory from a Unix (Linux or macOSX) terminal. Installation procedures are available in this [page](https://github.com/BlueBrain/NeuroMorphoVis/wiki/Installation).   

## Downloading Package 

_NeuroMorphoVis_ packages are available for Ubuntu, RedHat, macOSX and Windows from the [__releases__](https://github.com/BlueBrain/NeuroMorphoVis/releases) page. After downloading the package, users can load NeuroMorphoVis into Blender as explained in this [page](https://github.com/BlueBrain/NeuroMorphoVis/wiki/Running-NeuroMorphoVis).   

# Interfaces

_NeuroMorphoVis_ is primarily designed as a plug-in in [Blender](https://www.blender.org/). It comes with a user-friendly GUI and a rich set of command line options. Moreover, the tool is configurable via input configuration files making it possible to link it to web interface or using it on massively parallel visualization clusters for batch production. 

The tool is also extensible via its powerful python API that can be imported in Blender console and text browser. 

## GUI

To make it accessible to end users with minimal programming knowledge or even with no programming experience at all, the core functionality of _NeuroMorphoVis_ is exposed to users via a friendly graphical user interface that would allow them to navigate and adjust the parameters of the different toolboxes seamlessly. A detailed guide to use NeuroMorphoVis from its GUI is available in this [user guide](https://github.com/BlueBrain/NeuroMorphoVis/wiki/Graphical-User-Interface).

<p align="center">
<img src="https://github.com/BlueBrain/NeuroMorphoVis/wiki/images/modules/panels/interface-2.8.jpeg" width=800>
<figcaption><center>A screen shot of a neuronal morphology skeleton reconstructed by  NeuroMorphoVis and sketched in the 3D view port of Blender. Note that the neurites are tagged with different colors (green for apical dendrite, red for basal dendrites and blue for the axon) and the soma (in yellow) is reconstructed as a realistic three-dimensional profile not as a sphere.</figcaption>
</p>

## Command Line Options

_NeuroMorphoVis_ has a rich command line interface that would make it easy to connect it to a web interface or use it to accomplish multiple tasks in an automated way. A list of all the command line options and their description are available in this [user guide](https://github.com/BlueBrain/NeuroMorphoVis/wiki/Command-Line-Interface).

## Configuration Files 

Users can easily configure and use _NeuroMorphoVis_ via editable configuration files. Instructions to write and use configurations files are available in this [user guide](https://github.com/BlueBrain/NeuroMorphoVis/wiki/Configuration-File).

# Gallery 

<p align="center">
	<img src="https://github.com/BlueBrain/NeuroMorphoVis/wiki/images/renderings/dancing-neuron.jpeg" width=350>
	<img src="https://github.com/BlueBrain/NeuroMorphoVis/wiki/images/renderings/scary-neuron.jpeg" width=350>
</p>

<p align="center">
	<img src="https://github.com/BlueBrain/NeuroMorphoVis/wiki/images/renderings/bumpy-shading.png" width=704>
</p>

<p align="center">
	<img src="https://github.com/BlueBrain/NeuroMorphoVis/wiki/images/renderings/somata-ncc.jpeg" width=704>
</p>

<p align="center">
	<img src="https://github.com/BlueBrain/NeuroMorphoVis/wiki/images/renderings/neuron-group.jpeg" width=704>
</p>

<p align="center">	
	<img src="https://github.com/BlueBrain/NeuroMorphoVis/wiki/images/renderings/fluorescent-neuron.jpeg" width=350>	
	<img src="https://github.com/BlueBrain/NeuroMorphoVis/wiki/images/renderings/golgi-staining-neuron.jpeg" width=350>	
</p>


# Known Bugs or Feature Requests

Please refer to the [github issue tracker](https://github.com/BlueBrain/NeuroMorphoVis/issues?utf8=%E2%9C%93&q=) for fixed and open bugs. User can also report any bugs and request new features needed for their research. We are happy to provide direct [support](#contact) . 


# Publications & Citation 

If you use _NeuroMorphoVis_ for your research, media design or other purposes, please cite our paper [NeuroMorphoVis: a collaborative framework for analysis and visualization of neuronal morphology skeletons reconstructed from microscopy stacks](https://academic.oup.com/bioinformatics/article/34/13/i574/5045775) using the following entry:

```
@article{abdellah2018neuromorphovis,
  title={NeuroMorphoVis: a collaborative framework for analysis and visualization of 
  neuronal morphology skeletons reconstructed from microscopy stacks},
  author={Abdellah, Marwan and Hernando, Juan and Eilemann, Stefan and 
  Lapere, Samuel and Antille, Nicolas and Markram, Henry and 
  Sch{\"u}rmann, Felix},
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
  title={Reconstruction and visualization of large-scale volumetric models of neocortical 
  circuits for physically-plausible in silico optical studies},
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

The mesh generation algorithm with skin modifiers is described in this paper [Generating High Fidelity Surface Meshes of Neocortical Neurons using Skin Modifiers](https://diglib.eg.org/xmlui/handle/10.2312/cgvc20191257)

```
@journal{abdellah2019generating,
  booktitle={Computer Graphics and Visual Computing (CGVC)},
  editor={Vidal, Franck P. and Tam, Gary K. L. and Roberts, Jonathan C.},
  title={Generating High Fidelity Surface Meshes of Neocortical Neurons using 
  Skin Modifiers},
  author={Abdellah, Marwan and Favreau, Cyrille and Hernando, Juan and Lapere, Samuel 
  and Schürmann, Felix},
  year={2019},
  publisher={The Eurographics Association},
  isbn={978-3-03868-096-3},
  doi={10.2312/cgvc.20191257}
}
```

The mesh generation algorithm with using the Voxel remesher (for creating models needed for running reaction-diffusion simulations) is described in this paper [Synthesis of geometrically realistic and watertight neuronal ultrastructure manifolds for in silico modeling](https://academic.oup.com/bib/article/25/5/bbae393/7731493)

```
@article{abdellah2024synthesis,
  title={Synthesis of geometrically realistic and watertight neuronal ultrastructure 
  manifolds for in silico modeling},
  author={Marwan Abdellah, Alessandro Foni, Juan José García Cantero, 
  Nadir Román Guerrero, Elvis Boci, Adrien Fleury, Jay S Coggan, Daniel Keller, 
  Judit Planas, Jean-Denis Courcol, Georges Khazen},
  journal={Briefings in Bioinformatics},
  volume={25},
  number={5},
  pages={393},
  year={2024},
  publisher={Oxford}
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


# Publications that use or mention NeuroMorphoVis

An exhaustive list of all the publications that use or mention NeuroMorphoVis is available in this [Wiki page](https://github.com/BlueBrain/NeuroMorphoVis/wiki/Publications-Citing-NeuroMorphoVis).

# Acknowledgement & Funding
_NeuroMorphoVis_ is developed by the Visualization team at the [Blue Brain Project](https://bluebrain.epfl.ch/page-52063.html), [Ecole Polytechnique Federale de Lausanne (EPFL)](https://www.epfl.ch/) as part of [Marwan Abdellah's](http://marwan-abdellah.com/) [PhD (In silico Brain Imaging: Physically-plausible Methods for Visualizing Neocortical Microcircuitry)](https://infoscience.epfl.ch/record/232444?ln=en). Financial support was provided by funding to the [Blue Brain Project](https://bluebrain.epfl.ch/), a research center of the École polytechnique fédérale de Lausanne (EPFL), from the Swiss government’s ETH Board of the Swiss Federal Institutes of Technology, and by competitive research funding from [King Abdullah University of Science and Technology (KAUST)](https://www.kaust.edu.sa/en).

# License 
_NeuroMorphoVis_ is available to download and use under the GNU General Public License ([GPL](https://www.gnu.org/licenses/gpl.html), or “free software”). The code is open sourced with approval from the open sourcing committee and principal coordinators of the Blue Brain Project in December 2019. 

Copyright (c) 2016-2023 Blue Brain Project/EPFL

# Attributions 

* [Blender](https://www.blender.org/) (C) is copyright to Blender Foundation. The Blender Foundation is a non-profit organization responsible for the development of Blender. Blender is released under the GNU Public License, as Free Software, and therefore can be distributed by anyone freely. 

* [Slurm](slurm.schedmd.com), is a free and open-source job scheduler for Linux and Unix-like kernels, used by many of the world's supercomputers and computer clusters. Slurm is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation.

* The SWC morphology samples are available from [NeuroMorpho.Org](http://neuromorpho.org/). NeuroMorpho.Org is a centrally curated inventory or repository of digitally reconstructed neurons associated with peer-reviewed publications.

* The H5 morphology samples are available with permissions from the [Blue Brain Project](https://bluebrain.epfl.ch/page-52063.html), [Ecole Polytechnique Federale de Lausanne (EPFL)](https://www.epfl.ch/). 

* The analysis plots are created based on [Matplotlib](https://matplotlib.org/) and [Seaborn](https://seaborn.pydata.org/). Matplotlib is a comprehensive library for creating static, animated, and interactive visualizations in Python and Seaborn is a Python data visualization library based on matplotlib. It provides a high-level interface for drawing attractive and informative statistical graphics. Matplotlib only uses BSD compatible code, and its license is based on the [PSF](https://python.org/psf/license) license. Seaborn uses BSD license.

* The analysis distributions are gathered into a single PDF using [PyPDF2](http://mstamy2.github.io/PyPDF2/). PyPDF2 is a pure-python PDF library capable of splitting, merging together, cropping, and transforming the pages of PDF files. PyPDF2 uses the [BSD License](https://github.com/mstamy2/PyPDF2/blob/master/LICENSE).

* The table of contents for all the user documentation pages are generated with [markdown-toc](http://ecotrust-canada.github.io/markdown-toc/).


# Contact

For more information on _NeuroMorphoVis_, comments or suggestions, please contact:

__Marwan Abdellah__  
Scientific Visualiation Expert  
Visualization Team, Computing Division  
Blue Brain Project  
[marwan.abdellah@epfl.ch](marwan.abdellah@epfl.ch)  
[marwan-abdellah.com](http://marwan-abdellah.com)  

# Navigation 

+ Starting 
  + [Home](https://github.com/BlueBrain/NeuroMorphoVis/wiki)
  + [Downlading NeuroMorphoVis](https://github.com/BlueBrain/NeuroMorphoVis/wiki#downloading-package)
  + [Installing NeuroMorphoVis](https://github.com/BlueBrain/NeuroMorphoVis/wiki/Installation)
  + [Running NeuroMorphoVis](https://github.com/BlueBrain/NeuroMorphoVis/wiki/Running-NeuroMorphoVis)
  + [FAQs](https://github.com/BlueBrain/NeuroMorphoVis/wiki/FAQs)

+ Panels 

  + [Input / Output](https://github.com/BlueBrain/NeuroMorphoVis/wiki/Input-&-Output)
  + [Morphology Analysis](https://github.com/BlueBrain/NeuroMorphoVis/wiki/Morphology-Analysis)
  + [Morphology Editing](https://github.com/BlueBrain/NeuroMorphoVis/wiki/Morphology-Editing)
  + [Soma Reconstruction](https://github.com/BlueBrain/NeuroMorphoVis/wiki/Soma-Reconstruction)
  + [Morphology Reconstruction](https://github.com/BlueBrain/NeuroMorphoVis/wiki/Morphology-Reconstruction)
  + [Synaptics](https://github.com/BlueBrain/NeuroMorphoVis/wiki/Synaptics)
  + [Mesh Reconstruction](https://github.com/BlueBrain/NeuroMorphoVis/wiki/Mesh-Reconstruction)
  + [About NeuroMorphoVis](https://github.com/BlueBrain/NeuroMorphoVis/wiki/About)


+ Other Links 

  + [Analysis Kernels](https://github.com/BlueBrain/NeuroMorphoVis/wiki/Analysis)
  + [Colors & Shading](https://github.com/BlueBrain/NeuroMorphoVis/wiki/Colors-&-Shading)
  + [Configuration File](https://github.com/BlueBrain/NeuroMorphoVis/wiki/Configuration-File) 

<p align="center">
	<img src="https://raw.githubusercontent.com/wiki/BlueBrain/NeuroMorphoVis/images/logos/epfl-logo.png" width=200>
</p>
