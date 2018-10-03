# How to Install NeuroMorphoVis
_NeuroMorphoVis_ is designed and written as a [Blender _add-on_ or _plug-in_](https://docs.blender.org/manual/fi/dev/preferences/addons.html). This add-on can be loaded from the GUI or even called in Blender's python console relying on its API. Therefore, a recent version of Blender must be installed properly on your system to be able to use _NeuroMorphoVis_. 

## NeuroMorphoVis Requirements 
Before procedding to the installation procedures, the users must check the software and hardware requirements that are necessary to run _NeuroMorphoVis_. A summary of these requirements is given in this [page](requirements.md). 

## Software Dependencies 

_NeuroMorphoVis_ is mainly based on [Blender](https://www.blender.org/). [Blender](https://www.blender.org/) is a free software and can be downloaded from this page. [Blender](https://www.blender.org/) comes with an [LGPL license](https://en.wikipedia.org/wiki/GNU_Lesser_General_Public_License). The current version is compatible with the following Blender versions

+ [Blender 2.76](http://download.blender.org/release/Blender2.76/): 2.76a and 2.76b
+ [Blender 2.77](http://download.blender.org/release/Blender2.77/): 2.77 and 2.77a
+ [Blender 2.78](http://download.blender.org/release/Blender2.78/): 2.78, 2.78a, 2.78b and 2.78c
+ [Blender 2.79](http://download.blender.org/release/Blender2.79/): 2.79, 2.79a, 2.79b and 2.79c 


### Optional Dependencies 

By default, _NeuroMorphoVis_ uses Blender as a main dependency to load [SWC](http://www.neuronland.org/NLMorphologyConverter/MorphologyFormats/SWC/Spec.html) morphology files. This requires no further dependencies at all. 

#### H5 Morphologies 

To load [H5](https://developer.humanbrainproject.eu/docs/projects/morphology-documentation/0.0.2/index.html) morphology files, the following dependencies must be installed:

+ [HDF5 Python Bindings](https://www.h5py.org). Installing h5py is detailed in this [link](http://docs.h5py.org/en/latest/build.html)

#### BBP Circuits Morphologies 

There are other optional dependencies that are specific to users from the [Blue Brain Project](https://github.com/BlueBrain). To load circuit morphologies specified by GIDs or cell targets, the following dependencies must be installed:

+ [Blue Brain Brion](https://github.com/BlueBrain/Brion). 

## NeuroMorphoVis Installation

The [Blue Brain Project](https://bluebrain.epfl.ch/) distributes _NeuroMorphoVis_ in three different ways that you can choose from, to better suit the needs of the end users. 

+ _NeuroMorphoVis_ can be downloaded as an archive file that comprises a binary package for Blender __including the add-on__ for all the supported platforms. The add-on is already installed in the add-ons directory of Blender and can be immediately loaded when Blender is launched. This approach is easy and convenient for external users who are dealing only with standard morphology files (for example SWC files). Loading H5 files requires an additional step to install the python binding of the HDF5 library. Moreover, using loading morphologies in BBP circuits would require a further step for installing Brion. 

+ Users can download Blender as an archive from this [repository](http://download.blender.org/release/). Then _NeuroMorphoVis_ can be downloaded as an archive or cloned from this [repository](https://github.com/BlueBrain/NeuroMorphoVis) and manually added to the add-on directory of Blender. Similarly, loading H5 files requires an additional step to install the python binding of the HDF5 library and loading morphologies in BBP circuits would also require a further step for installing Brion. 

+ Users can installed Blender as a system package (depending on the operating system) and follow the rest of the steps mentioned in the previous approach.

### Notes

+ We do not recommend compiling Blender from source. This step might be cumbersome. 

+ If the users are not familiar with Blender installation, this [page](https://docs.blender.org/manual/en/latest/getting_started/installing/introduction.html#download-blender) can help them installing Blender easily. 

### Installing NeuroMorphoVis 

We have prepared a little guide to install _NeuroMorphoVis_ on the following platforms 

+ on [Linux](install-linux.md)

+ on [Mac](install-macosx.md)

+ on [Windows](install-windows.md)

## Loading NeuroMorphoVis

To verify the installation procedure, the users can load _NeuroMorphoVis_ from the user interface and visualize a sample neuronal morphology that is available in the data directory on the repository. The procedure is described in this [page](loading.md).     