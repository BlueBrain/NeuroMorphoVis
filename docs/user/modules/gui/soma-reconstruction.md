# Soma Toolbox Panel

<p align="center">
  <img src="images/gui-soma-toolbox-open.jpg" width=800>
</p>

## Introduction
This panel gives access to the parameters of the __Soma Reconstruction Toolbox__.      

## Why this Toolbox?
Due to the fuzzy definition of the soma, the relevant information contained in generic morphology skeletons that describe the soma is usually insufficient to reconstruct a realistic representation of it. In those morphologies, the soma is merely represented by a centroid, a radius that approximates the average distance between this centroid and the initial segments of each neurite, and a projective profile that is traced along a two-dimensional plane. In certain studies, the soma is not modeled based on the reported data in the morphological skeleton, but rather represented by an implicit surface for convenience. Therefore, the reconstruction of even an approximation of the soma contour is quite challenging. Recent methods have been presented to provide a univocal definition of the somata, allowing automated characterization of neurons and accurate segmentation of three-dimensional somata profiles measured at multiple depths of fields during the tracing procedure.

The __Soma Reconstruction Toolbox__ is added to allow the generation of highly plausible somata profiles relying on their two-dimensional contours and the starting locations of their neurites. The process simulates the progressive reconstruction of the soma using _Hooke’s law_ and _mass spring models_. The idea has been adapted from a recent study ([Brito et al., 2013](https://www.frontiersin.org/articles/10.3389/fnana.2013.00015/full)) and implemented in Blender using its physics engine ([Abdellah et al., 2017b](https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-017-1788-4)). 

We extended the Blender-based implementation and integrated this module into _NeuroMorphoVis_ to provide a convenient tool to validate and compare the somata obtained by segmenting a microscopic stack with the ones extracted from three-dimensional contours.

## Opening the Soma Toolbox

<p align="center">
  <img src="images/panels-soma-closed.jpg" width=300>
</p>

When you toggle (or click on) the __Soma Toolbox__ tab highlighted above, the following panel, or a similar one depending on the version of _NeuroMorphoVis_, will appear.

<p align="center">
  <img src="images/panels-soma-open.jpg" width=300>
</p>

In the following sections, we will detail all the parameters shown in each section in this panel.

## Panel Options

### Soma Reconstruction Method
 
This version of _NeuroMorphoVis_ has implemented three different methods to reconstruct three-dimensional somata profiles:

+ __Profile__: This method uses only the profile points that are reported in the morphology files to reconstruct the soma from an ico-sphere, whose radius is set to the mean soma radius. 
   
<p align="center">
  <img src="images/soma-complex.png" width=200>
</p>

+ __Arbors__: This method uses the starting points of each root arbor to deform an ico-sphere. This is the deafult reconstruction method.
 
<p align="center">
  <img src="images/soma-arbors.png" width=200>
</p>

+ __Complex__: This is a combined method of the two previous ones. The pulling occurs towards the profiles points and the starting points of each neurite connected to the soma.

<p align="center">
  <img src="images/soma-profile.png" width=200>
</p>

### Soft Body Parameters 

Soft body simulation is used in general for simulating soft deformable objects. It was designed primarily for adding secondary motion to animation, like jiggle for body parts of a moving character. It also works for simulating more general soft objects that bend, deform and react to forces like gravity and wind, or collide with other objects. The simulation works by combining existing animation on the object with forces acting on it. There are exterior forces like gravity or force fields and interior forces that hold the vertices together. This way you can simulate the shapes that an object would take on in reality if it had volume, was filled with something, and was acted on by real forces.
_NeuroMorphoVis_ uses soft body simulation to deform an initial ico-sphere into an object that can reflect or approximate a three-dimensional profile of the soma. Further details about soft body simulation can be found in this [link](https://docs.blender.org/manual/ja/dev/physics/soft_body/introduction.html#typical-scenarios-for-using-soft-bodies).

### Stiffness 

The __Stiffness__ slider controls the spring stiffness of the soft body object. A low value creates very weak springs (more flexible "attachment" to the goal), a high value creates a strong spring (a stiffer "attachment" to the goal). This parameter can take values between 0.001 and 1.0. 


#### Notes 

+ We have gone through many trial and error iterations to test some other parameters of the soft body object to yield a plausible shape. However, the user does not have control to any of them. These values are as follows:

	+ __Garvity__ 0.0
	+ __Goal Max__ 0.1
	+ __Goal Min__ 0.7
	+ __Goal Default__ 0.5
 
+ Soft bodies work especially well if the objects have an even vertex distribution. You need enough vertices for good collisions. You change the deformation (via the stiffness slider) if you add more vertices in a certain region.

### Subdivisions 

This parameter control the number of vertices of the initial soft body object used in the simulation. It defines how many recursions are used to create the sphere. At level 1 the ico sphere is an icosahedron, a solid with 20 equilateral triangular faces. Each increase in the number of subdivisions splits each triangular face into four triangles. Further details about the ico-spheres can be found in this [link]
(https://docs.blender.org/manual/en/dev/modeling/meshes/primitives.html#icosphere).

#### Notes 

+ Subdividing an icosphere raises the vertex count very quickly even with few iterations (10 times creates 5,242,880 triangles), Adding such a dense mesh is a sure way to cause the program to crash. Therefore, we have limited the range of the __Subdividions__ from 3 to 7. 

### Irregular Subdivision 

### Colors & Materials 

#### Soma Base Color 

#### Material 

## Let's Reconstruct a 3D Soma Profile

## Render the Soma 

Normally, the extent of the reconstructed soma mesh cannot exceed 20-30 microns. However, the user can control the dimensions of the view in case a close up on a given part of the soma mesh is wanted. 

Orthographic 

### Frame Resolution 

This parameter defines the resolution of the rendered image of the soma mesh. This image have the same resolution in width and height and that's why the __Frame Resolution__ slider has only a single value.  

## Exporting the Soma Mesh

Finally, the users can export the reconstructed surface mesh of the soma. The users can exploit the native support of Blender to export meshes into different file formats. But since we assumed that end users might not have any Blender experience, we have addedd four buttons to export the reconstructed soma meshes into the following common file formats:

+ __Wavefront (.obj)__ 
The OBJ file format is a simple data-format that represents 3D geometry alone — namely, the position of each vertex, the UV position of each texture coordinate vertex, vertex normals, and the faces that make each polygon defined as a list of vertices, and texture vertices. Further details about this file format can be found [here](https://en.wikipedia.org/wiki/PLY_(file_format)).

+ __Stanford (.ply)__ 
PLY is a file format known as the Polygon File Format or the Stanford Triangle Format. It was principally designed to store three-dimensional data from 3D scanners. The data storage format supports a relatively simple description of a single object as a list of nominally flat polygons. A variety of properties can be stored, including: color and transparency, surface normals, texture coordinates and data confidence values. The format permits one to have different properties for the front and back of a polygon.
Further details about this file format can be found [here](https://en.wikipedia.org/wiki/STL_(file_format)). 

+ __Stereolithography CAD (.stl)__ 
The STL file describes a raw, unstructured triangulated surface by the unit normal and vertices (ordered by the right-hand rule) of the triangles using a three-dimensional Cartesian coordinate system. Further details about this file format can be found [here](https://en.wikipedia.org/wiki/STL_(file_format)). 

+ __Blender Format (.blend)__ 
The exported file can be opened _only_ in Blender and can be used for rendereing purposes. 
