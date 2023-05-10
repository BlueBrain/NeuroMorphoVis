####################################################################################################
# Copyright (c) 2016 - 2023, EPFL / Blue Brain Project
#               Marwan Abdellah <marwan.abdellah@epfl.ch>
#
# This file is part of NeuroMorphoVis <https://github.com/BlueBrain/NeuroMorphoVis>
#
# This program is free software: you can redistribute it and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation, version 3 of the License.
#
# This Blender-based tool is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.
# If not, see <http://www.gnu.org/licenses/>.
####################################################################################################

# Internal imports
import nmv.options

# If this flag is set, this means that the system has been initialized and all the icons, fonts
# and other relevant data have been loaded into the system.
nmv_initialized = False

# NeuroMorphoVisOptions ############################################################################
# A global variable for the system options.
# All the parameters of the system are stored in this global variable and updated following the
# execution of an active element in the GUI.
# You can access all the parameters of the system as follows:
#   ui.globals.options.io.VARIABLE : for the input/output directories
#   ui.globals.options.soma.VARIABLE : for the soma options
#   ui.globals.options.morphology.VARIABLE : for the morphology options
#   ui.globals.options.mesh.VARIABLE : for the mesh options
#   ui.globals.options.analysis.VARIABLE : for the analysis options
#   ui.globals.options.rendering.VARIABLE : for the rendering options
#   ui.globals.options.shading.VARIABLE : for the shading options
#   ui.globals.options.synaptics.VARIABLE : for the synaptics options
ui_options = nmv.options.NeuroMorphoVisOptions()

####################################################################################################
# Morphology IO ####################################################################################
####################################################################################################
# The morphology skeleton object loaded after UI interaction.
ui_morphology = None

# A reference to the circuit loaded in NMV, if any.
ui_circuit = None

# All the icons loaded for the UI.
ui_icons = None

####################################################################################################
# Morphology Analysis ##############################################################################
####################################################################################################
# This flag is set after the analysis of the morphology.
ui_morphology_analyzed = False

####################################################################################################
# Morphology Editing ###############################################################################
####################################################################################################
# A reference to the editor used to edit and modify the skeleton of the neuronal morphology.
ui_morphology_editor = None

# A flag to indicate that the morphology has been edited and ready for update
ui_is_skeleton_edited = False

# A flag that indicates if we are in the edit mode or not
ui_in_edit_mode = False

####################################################################################################
# Soma Meshing #####################################################################################
####################################################################################################
# A reference to the mesh object of the reconstructed soma.
ui_soma_mesh = None

# This flag is set to True if the soma mesh is reconstructed in the UI.
ui_soma_reconstructed = False

# This flag is set if the soma is rendered.
ui_soma_rendered = False

####################################################################################################
# Morphology Reconstruction ########################################################################
####################################################################################################
# A reference to the morphology builder used to build the morphology skeleton.
ui_morphology_builder = None

# A list of all the objects that correspond to the reconstructed morphology skeleton
ui_reconstructed_skeleton = list()

# If this flag is set, this means that a morphology is already reconstructed, and we can display the
# morphology export options to be able to save the morphology to disk. If this flag is not set,
# this means that the morphology reconstruction operator has never been executed.
ui_morphology_reconstructed = False

# If this flag is set, this means that the reconstructed morphology is rendered at least once.
ui_morphology_rendered = False

####################################################################################################
# Synaptics ########################################################################################
####################################################################################################
# This flag is set if a valid synaptics file is loaded in the UI.
ui_synaptics_file_loaded = False

# This flag is set if a synaptics scene is reconstructed.
ui_synaptics_reconstructed = False

# This flag is set if a synaptics scene is rendered.
ui_synaptics_rendered = False

####################################################################################################
# Mesh Reconstruction ##############################################################################
####################################################################################################
# A list of all the objects that correspond to the reconstructed mesh of the neuron
# NOTE: If this list contains a single mesh object, then it accounts for the entire mesh after
# joining all the mesh objects together
ui_reconstructed_mesh = list()

# If this flag is set, this means that a mesh is already reconstructed, and we can display the
# mesh export options to be able to export the mesh. If this flag is not set, this means that the
# mesh reconstruction operator has never been executed.
ui_mesh_reconstructed = False

# If this flag is set, this means that the reconstructed mesh is rendered at least once.
ui_mesh_rendered = False
