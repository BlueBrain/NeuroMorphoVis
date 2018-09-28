# Morphology Reconstruction Toolbox Panel

<p align="center">
  <img src="images/morphology-panel.png">
</p>

## Summary

This panel gives access to the parameters of the __Morphology Reconstruction Toolbox__. By reconstruction in the context, we mean generating a three-dimensional skeleton from a dendrogram (a tree diagram frequently used to illustrate the arrangement of the clusters produced by hierarchical clustering, for further details refer to this [link](https://en.wikipedia.org/wiki/Dendrogram)). 

### What is a Morphology Skeletion?

Neuronal morphologies are reconstructed from imaging stacks obtained from different microscopes. These morphologies can be digitized either with semi-automated or fully automated tracing methods. The digitization data can be stored in multiple file formats such as SWC and the Neurolucida proprietary formats. For convenience, the digitized data are loaded, converted and stored as a tree data structure (a data structure representing the dendrogram). 

### Morphology Components

The skeletal tree of a neuron is defined by the following components: a cell body (or soma), sample points, segments, sections, and branches. The soma, which is the root of the tree, is usually described by a point, a radius and a two-dimensional contour of its projection onto a plane or a three-dimensional one extracted from a series of parallel cross sections. Each sample represents a point in the morphology having a certain position and the radius of the corresponding cross section at this point. Two consecutive samples define a connected segment, whereas a section is identified by a series of non-bifurcating segments and a branch is defined by a linear concatenation of sections.  

Neuronal branches are, in general, classified based on their types into 
 
 + axons, 
 + apical dendrites and 
 + basal dendrites. 
 
### Important Note

Note that the three-dimensionap profile of the soma that is reconstructed in this skeleton -- if requested -- is based on the parameters set in the _Soma Toolbox panel_.

## Opening the Morphology Toolbox Panel

When you toggle (or click on) the _Morphology Toolbox_ tab highlighted in red above, the following panel, or a similar one depending on the version of NeuroMorphoVis, will appear.

<p align="center">
  <img src="images/morphology-panel-detailed.png">
</p>

In the following sections we will detail all the parameters shown in each section in this panel.
 
## Morphology Skeletion Parameters

In this section the user can select which components of the morphology skeletion will be reconstructed and generated in the scene.

### Soma 

The soma can be _ignored_ , represented symbolically by a _sphere_, or represented by an accurate _three-dimensional profile_ that can approximate its actual shape. The user can select one of the following options:

+ __Ignore__
The soma is totally ignored.  

+ __Sphere__ 
The soma is symbolically represented by a sphere whose center is _usually_ set to the origin and radius is set to the mean radius reported in the morphology file.  

+ __Profile__ 
The soma is usually described in the morphology file by a point, a radius and a two-dimensional contour of its projection onto a plane. We use this data and reconstruct a three-dimensional profile of the soma using Hooke's law and the physics engine of Blender. If this option is selected, a realistic shape of the soma will be reconstructed and added to the scene.  Note that this profile is reconstructed based on the parameters set in the _Soma Toolbox panel_.







             
| A | B | C | D | E | F | G |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| ![](images/morphology-1.png)  | ![](images/morphology-2.png)  | ![](images/morphology-3.png)|![](images/morphology-4.png)|![](images/morphology-5.png) | ![](images/morphology-6.png) | ![](images/morphology-7.png) |
