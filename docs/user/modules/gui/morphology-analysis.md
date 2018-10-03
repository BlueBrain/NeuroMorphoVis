# Morphology Analysis Panel

<p align="center">
  <img src="images/morphology-analysis-panel-selected.png" width=300>
</p>

## Summary
This panel gives access to the parameters of the Soma Toolbox.      

## Why this Toolbox?
This toolbox helps the users to analyze and validate the morphology before using it for any reconstructions.  

## Opening the Morphology Analysis Toolbox

When you toggle (or click on) the Morphology Analysis Toolbox tab highlighted in yellow above, the following panel, or a similar one depending on the version of NeuroMorphoVis, will appear. 

<p align="center">
  <img src="images/morphology-analysis-panel-overview.png" width=300>
</p>

### Analysis Options 

+ __Number of Samples per Section__
This kernel computes the number of samples per section on each section in the morphology.  

+ __Number of Segments per Section__
This kernel computes the number of segments per section on each section in the morphology. 

+ __Number of Sections per Arbor__
This kernel computes the number of sections per arbor for each arbor in the morphology. 

+ __Branching Angles__
This kernel computes all the angles between the different branches at bifurcation and trifurcation points along each arbor in the morphology. 

+ __Branching Radii__
This kernel computes the radii of the samples located at the bifurcation and trifurcation points along each arbor in the morphology. 

+ __Sections Length__
This kernel computes the lengths of all the sections in the morphology. 

+ __Short Sections__
This kernel identifies if the morphology has any short sections or not. 

+ __Duplicate Samples__
+ This kernel identifies if the morphology has any duplicate sample or not. 

+ __Disconnected Axons__
This kernel identifies if the axons are connected to the soma or not. 

+ __Branches with Negative Samples__
This kernel identifies if any of the branches have negative samples that intersect with the soma or not. 

### Let's Analyze the Morphology

After selecting all the analysis filters that are neccessary, the user can generate the analysis files by clicking on the _Analyze Morphology_ button at the end of the _Morphology Analysis_ panel. 

## Extensions

We are currently extending this module by adding further analysis filters. The next release will have the following options:

+ Segments Length 
+ Total Arbor Length
+ Total Morphology Length
+ Number of Bifurcations 
+ Number of Trifucations 
+ Sections Volumes
+ Arbor Volumes 
