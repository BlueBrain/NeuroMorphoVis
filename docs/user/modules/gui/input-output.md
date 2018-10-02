# Input / Output Panel

<p align="center">
  <img src="images/gui-loading-toolboxes.jpg">
</p>

## Function

The _Input / Output_ panel allows the users to select the _input morphologies_ and the _output directories_ where the different results (morphologies, images, sequences, meshes and analysis reports) will be generated.    

## Input Data Options 
The current version of NeuroMorphoVis can read morphologies stored in the following file formats:

+ The standard [.SWC](http://www.neuronland.org/NLMorphologyConverter/MorphologyFormats/SWC/Spec.html) file format. 

+ [H5](https://developer.humanbrainproject.eu/docs/projects/morphology-documentation/0.0.2/index.html) file format. This format is specific to the [Blue Brain Project (BPP)](https://bluebrain.epfl.ch/) and [Human Brain Project (HBP)](https://www.humanbrainproject.eu/en/), but the python bindings of HDF5 library must be installed to the system to load it.

### Note

We are currently extending _NeuroMorphoVis_ to add support to read standrd [Neurolucida](https://www.mbfbioscience.com/neurolucida) ASCII morphologies that are directly generated from microscopic reconstruction software solutions.   

### Input Source
+ The users can load morphologies from individual .SWC or .H5 files based on their absolute pathes in the file system. In this case, the _Input Source_ option should be set to _H5 or SWC File_, and the path to the morphology file should be set in the _Morphology File_ text box. You can also use the button on the right of the text box to open a file dialog and select the file from a specific path.

<p align="center">
  <img src="images/io-1.png">
</p>

+ The users can also load a morphology of a certain neuron reconstructed in a BBP circuit using its GID. In this case, the _Input Source_ option should be set to _BBP Circuit (GID)_, and then the path to the circuit configuration should be set in the _Circuit File_ text box (replace _Select Circuit File_ by the absolute path of the circuit, for example: /gpfs/WHATEVER_PROJECT/config.circuit) and the GID of the neuron should be set in the _GID_ field (replace _Add a GID_ by the GID of the neuron, for example: 1000).  

<p align="center">
  <img src="images/io-2.png">
</p>

### Output Options
NeuroMorphoVis can be only used to load and visualize morphologies. But if the users would like create any output, for example images, videos or meshes, then the _Output Directory_, where there artifacts will be generated, _must_ be set (replace _Select Directory_ by the absolute path of the output directory).

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

If the user wants to change the name any of these subdirectories, then the checkbox _Use Default Output Paths_ must be unchecked. 

<p align="center">
  <img src="images/io-3.png">
</p>
