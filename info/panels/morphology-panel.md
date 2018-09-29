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
 
## Morphology Skeleton Parameters

In this section the user can select which components of the morphology skeletion will be reconstructed and generated in the scene.

### Soma 

The soma object can be _ignored_, represented symbolically by a _sphere_, or represented by an accurate _three-dimensional profile_ that can approximate its actual shape. 

<p align="center">
  <img src="images/morphology-panel-soma.png" width=700>
</p>

The user can select one of the following options:

+ __Ignore__
The soma is totally ignored. 

<p align="center">
  <img src="images/morphology-panel-soma-ignore.png" width=300>
</p>

+ __Sphere__ 
The soma is symbolically represented by a sphere whose center is _usually_ set to the origin and radius is set to the mean radius reported in the morphology file. 

<p align="center">
  <img src="images/morphology-panel-soma-sphere.png" width=300>
</p>

+ __Profile__ 
The soma is usually described in the morphology file by a point, a radius and a two-dimensional contour of its projection onto a plane. We use this data and reconstruct a three-dimensional profile of the soma using Hooke's law and the physics engine of Blender. If this option is selected, a realistic shape of the soma will be reconstructed and added to the scene.  Note that this profile is reconstructed based on the parameters set in the _Soma Toolbox panel_.

<p align="center">
  <img src="images/morphology-panel-soma-profile.png" width=300>
</p>

### Branches 

The user can add arbitrarly any branch of a specific type - if exists in the original morphology file - or remove it from the reconstructed skeleton. For example, in certain cases, the axon might not be that important to visualze. The user can remove the axon from the reconstructed object by unchecking the _Build Axon_ checkbox. 

<p align="center">
  <img src="images/morphology-panel-ignore-axon.png" width=300>
</p>

The user can also select or highlight a specific branch type to visualize, for example basal dendrites. In this case the _Build Basal Dendrites_ checkbox must be checked and the _Build Axon_ and _Build Apical Dendrites_ checkboxes must be unchecked. 

<p align="center">
  <img src="images/morphology-panel-buidl-basal-dendrites.png" width=300>
</p>

The maximum branching order of each type (axon, basal dendrite or apical dendrite) can be controled from the _Branch Order_ slider that corresponds to each branch type. For example, in the image below, the maximum branching order of the axon is set to 5, while the maximum branching orders of the apical and basal dendrites are set to 100. In general, setting the maximum branching order to 100 guarantees that all the branches will be reconstructed in the scene.  

<p align="center">
  <img src="images/morphology-panel-branching-order.png" width=300>
</p>

 
## Morphology Reconstruction Parameters
  
### Reconstruction Method

### Skeleton Style 

### Branching 

+ __Radii__
This option is the default. 

<p align="center">
  <img src="images/morphology-panel-branching-radii.png" width=300>
</p>
 
+ __Angles__  

<p align="center">
  <img src="images/morphology-panel-branching-angles.png" width=300>
</p>

### Arbor Quality 

### Sections Radii 
<p align="center">
  <img src="images/morphology-panel-section-radii.png" width=300>
</p>


+ __As Specified in Morphology__

+ __At a Fixed Diamater__

+ __With Scale Factor__



## Morphology Colors and Shading Parameters

## Let's Reconstruct the Morphology 

<p align="center">
  <img src="images/morphology-panel-reconstruction-button.png" width=300>
</p>

## Rendering Parameters 

<p align="center">
  <img src="images/morphology-panel-render-wideshot.png" width=300>
</p>

<p align="center">
  <img src="images/morphology-panel-render-midshot.png" width=300>
</p>

<p align="center">
  <img src="images/morphology-panel-render-closeup.png" width=300>
</p>


## Let's Render the Morphology

<p align="center">
  <img src="images/morphology-panel-rendering-view.png" width=300>
</p>

<p align="center">
  <img src="images/morphology-panel-rendering-animation.png" width=300>
</p>



## Morphology Export 

+ __Export as a Blender File__

<p align="center">
  <img src="images/morphology-panel-save-blender-format.png" width=300>
</p>

| A | B | C | D | E | F | G |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| ![](images/morphology-1.png)  | ![](images/morphology-2.png)  | ![](images/morphology-3.png)|![](images/morphology-4.png)|![](images/morphology-5.png) | ![](images/morphology-6.png) | ![](images/morphology-7.png) |
