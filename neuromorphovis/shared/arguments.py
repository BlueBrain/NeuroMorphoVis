"""arguments.py:
    Command line arguments
"""

__author__      = "Marwan Abdellah"
__copyright__   = "Copyright (c) 2016 - 2017, Blue Brain Project / EPFL"
__version__     = "0.1.0"
__maintainer__  = "Marwan Abdellah"
__email__       = "marwan.abdellah@epfl.ch"
__status__      = "Production"

####################################################################################################
# Circuit arguments
####################################################################################################
BLUE_CONFIG_ARG                     = '--blue-config'
INPUT_ARG                           = '--input'
INPUT_MESHES_DIRECTORY_ARG          = '--input-meshes-directory'
RENDERING_TARGET_FILE_ARG           = '--rendering-target-file'
GID_ARG                             = '--gid'
CELL_TARGET_ARG                     = '--cell-target'

####################################################################################################
# Morphology arguments
####################################################################################################
__ignore_soma_args__                = '--ignore-soma'
__ignore_axon_args__                = '--ignore-axon'
__ignore_dendrites_args__           = '--ignore-dendrites'
__ignore_basal_dendrites_args__     = '--ignore-basal-dendrites'
__ignore_apical_dendrite__          = '--ignore-apical-dendrite'
__build_spines_arg__                = '--build-spines'
__max_axon_level_arg__              = '--max-axon-level'
__max_dendrites_level_arg__         = '--max-dendrites-level'
__max_basal_dendrites_level_arg__   = '--max-basal-dendrites-level'
__max_apical_dendrite_level_arg__   = '--max-apical-dendrite-level'

####################################################################################################
# Meshes arguments
####################################################################################################
__save_ply_format_arg__             = '--ply'
__save_obj_format_arg__             = '--obj'
__save_stl_format_arg__             = '--stl'
__save_blend_format_arg__           = '--blend'
__tessellation_level_arg__          = '--tessellation-level'
__export_single_mesh_arg__          = '--export-single-mesh'
__export_separate_meshes_arg__      = '--export-separate-meshes'
__global_coordinates_arg__          = '--global'
__meshing_technique_arg__           = '--meshing-technique'

####################################################################################################
# Rendering arguments
####################################################################################################
__render_soma_skeleton_arg__        = '--render-soma-skeleton'
__render_morphology_skeleton_arg__  = '--render-morphology-skeleton'
__render_soma_profile_arg__         = '--render-soma-profile'
__render_soma_mesh_arg__            = '--render-soma-mesh'
__render_mesh_arg__                 = '--render-mesh'
__render_close_up_arg__             = '--render-close-up'
__resolution_arg__                  = '--resolution'
__render_individual_neurons_arg__   = '--render-individual-neurons'
__render_group_neurons_arg__        = '--render-group-neurons'

####################################################################################################
# Rendering arguments
####################################################################################################
__output_directory_arg__            = '--output-directory'
__blender_executable_arg__          = '--blender-executable'
__execution_node_arg__              = '--execution-node'
__number_cores_arg__                = '--number-cores'
__execution_cluster_arg__           = '--execution-cluster'
__granularity_arg__                 = '--granularity'
