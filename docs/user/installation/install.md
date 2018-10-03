# How to Install NeuroMorphoVis

NeuroMorphoVis is designed and written as a Blender _add-on_ or _plug-in_. This add-on can be loaded from its GUI or even called in its python console relying on its API. Therefore, a recent Blender version must be installed properly on your system to be able to use _NeuroMorphoVis_. 

## Supported Platforms 

_NeuroMorphoVis_ has been depolyed and tested on the following platforms:
 
+ Linux (Ubunut 16.04, Ubuntu 17.04, Ubunut 18.04 and RedHat) 

+ Mac (OS X 10.11, macOS 10.12, macOS 10.13 and macOS 10.14)

+ Windows (Windows 7, Windows 8 and Windows 10)

## NeuroMorphoVis Requirements 

https://www.blender.org/download/requirements/ 

## Blender Installation 
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
