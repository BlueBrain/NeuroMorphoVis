"""enumerators.py:
    Enumerators
"""

__author__      = "Marwan Abdellah"
__copyright__   = "Copyright (c) 2016 - 2017, Blue Brain Project / EPFL"
__version__     = "0.1.0"
__maintainer__  = "Marwan Abdellah"
__email__       = "marwan.abdellah@epfl.ch"
__status__      = "Production"

# Blender imports
from mathutils import Vector

xxx = '111'
####################################################################################################
# @Input data options
####################################################################################################
__input_h5_swc_file__ = 'h5_swc_file'
__input_h5_swc_directory__ = 'h5_swc_directory'
__input_circuit_gid__ = 'circuit_gid'
__input_circuit_target__ = 'circuit_target'

####################################################################################################
# @Branching
####################################################################################################
__branching_angles__ = 'branching_angles'
__branching_radii__ = 'branching_radii'

####################################################################################################
# @Meshing techniques
####################################################################################################
__meshing_technique_union__ = 'union'
__meshing_technique_piecewise__ = 'piecewise'
__meshing_technique_watertight__ = 'watertight'
__meshing_technique_bridging__ = 'bridging'

####################################################################################################
# @Meshing soma connection
####################################################################################################
__meshing_soma_connected__ = 'soma_connected'
__meshing_soma_disconnected__ = 'soma_disconnected'

####################################################################################################
# @Meshing objects connection
####################################################################################################
__meshing_objects_connected__ = 'objects_connected'
__meshing_objects_disconnected__ = 'objects_disconnected'

####################################################################################################
# @Meshing smoothing
####################################################################################################
__meshing_hard_edges__ = 'hard_edges'
__meshing_smooth_edges__ = 'smooth_edges'

####################################################################################################
# @Mesh model
####################################################################################################
__meshing_model_reality__ = 'model_reality'
__meshing_model_beauty__ = 'model_beauty'

####################################################################################################
# @Sections Radii
####################################################################################################
__sections__radii__as_specified__ = 'as_specified'
__sections__radii__at_fixed_scale__ = 'at_fixed_scale'
__sections__radii__with_scale_factor__ = 'with_scale_factor'

####################################################################################################
# @Arbors Colors
####################################################################################################
__soma_color__ = Vector((0.05, 0.5, 0.75))
__axon_color__ = Vector((0.9, 0.5, 0.75))
__basal_dendrites_color__ = Vector((0.0, 0.9, 0.75))
__apical_dendrites_color__ = Vector((0.0, 0.0, 1.0))
__articulation_color__ = Vector((1.0, 1.0, 0.0))
__spines_color__ = Vector((1, 1, 1))

####################################################################################################
# @Morphology Reconstruction Techniques
####################################################################################################
__method_disconnected_skeleton__ = 'disconnected_skeleton'
__method_disconnected_skeleton_resampled__ = 'disconnected_skeleton_resampled'
__method_disconnected_segments__ = 'disconnected_segments'
__method_disconnected_sections__ = 'disconnected_sections'
__method_articulated_sections__ = 'articulated_sections'
__method_connected_sections__ = 'connected_sections'
__method_connected_sections_repaired__ = 'connected_sections_repaired'

####################################################################################################
# @Reconstructed Soma Representation
####################################################################################################
__soma_ignore__ = 'ignore_soma'
__soma_sphere__ = 'soma_sphere'
__soma_soft_body__ = 'soma_soft_body'
__max_branching_level__ = 100

####################################################################################################
# @Prefixes
####################################################################################################
__axon_prefix__ = 'axon'
__basal_dendrite_prefix__ = 'basal_dendrite'
__apical_dendrite_prefix__ = 'apical_dendrite'

####################################################################################################
# @Rendering Methods & Shaders
####################################################################################################
__rendering_lambert__ = 'lambert'
__rendering_super_electron_light__ = 'super_electron_light'
__rendering_super_electron_dark__ = 'super_electron_dark'
__rendering_electron_light__ = 'electron_light'
__rendering_electron_dark__ = 'electron_dark'
__rendering_shadow__ = 'shadow'
__rendering_flat__ = 'flat'
__rendering_full_view__ = 'full_view'
__rendering_to_scale__ = 'to_scale'
__rendering_close_up__ = 'close_up'
__rendering_whole_morphology__ = 'extent_whole_morphology'
__rendering_selected_components__ = 'extent_selected_arbors'
