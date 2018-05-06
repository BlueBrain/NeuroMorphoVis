"""consts.py:
    Constants
"""

__author__      = "Marwan Abdellah"
__copyright__   = "Copyright (c) 2016 - 2017, Blue Brain Project / EPFL"
__version__     = "0.1.0"
__maintainer__  = "Marwan Abdellah"
__email__       = "marwan.abdellah@epfl.ch"
__status__      = "Production"

# System imports
import os

# Keep a reference to the current directory
current_directory = os.path.dirname(os.path.realpath(__file__))

####################################################################################################
# Math parameters
####################################################################################################
__infinity__ = 1e30
__epsilon__ = 0.99

####################################################################################################
# Morphology parameters
####################################################################################################
__origin_sample_radius__ = 0.1
__first_sample_radius__ = 0.1
__last_sample_radius__ = 0.05
__first_sample_radius_scale_factor__ = 0.5
__last_sample_radius_scale_factor__ = 0.5

####################################################################################################
# Meshing parameters
####################################################################################################
__max_tessellation_value__ = 0.1
__bevel_object_sides__ = 16

####################################################################################################
# Simulation parameters
####################################################################################################
__min_simulation_frame__ = 0
__max_simulation_frame__ = 100

####################################################################################################
# Output relative paths
####################################################################################################
__data_folder__ = 'data'
__images_folder__ = 'images'
__morphologies_folder__ = 'morphologies'
__meshes_folder__ = 'meshes'
__sequences_folder__ = 'sequences'
__slurm_folder__ = 'slurm'
__slurm_jobs_folder__ = '%s/jobs' % __slurm_folder__
__slurm_logs_folder__ = '%s/logs' % __slurm_folder__

####################################################################################################
# Default spines folders
####################################################################################################
__spines_meshes_directory__ = '%s/../data/spines' % current_directory
__spines_morphologies_directory__ = '%s/../data/spines-morphologies' % current_directory

####################################################################################################
# Soft body parameters
####################################################################################################
__soft_body_gravity__ = 0.0
__soft_body_goal_max__ = 0.1
__soft_body_goal_min__ = 0.7
__soft_body_goal_default__ = 0.5
__soft_body_subdivisions_default__ = 0.4
__soft_body_simulation_steps_default__ = 100


####################################################################################################
# Images resolutions
####################################################################################################
__image_full_view_resolution__ = 1024
__image_close_up_resolution__ = 512
__image_min_resolution = 256
__image_max_resolution = 1024 * 10

####################################################################################################
# View
####################################################################################################
__view_close_up_dimensions__ = 20 # In microns

####################################################################################################
# Messages
####################################################################################################
__msg_path_not_set__ = "Output directory is not set, update it in the Input / Output Data panel"
__msg_invalid_output_path__ = "Invalid output directory, update it in the Input / Output Data panel"

####################################################################################################
# Morphology types
####################################################################################################
mtypes = ['L1_DAC',             ### layer 1
          'L1_NGC-DA',
          'L1_NGC-SA',
          'L1_HAC',
          'L1_DLAC',
          'L1_SLAC',
          'L23_PC',             ### layer 2/3
          'L23_MC',
          'L23_BTC',
          'L23_DBC',
          'L23_BP',
          'L23_NGC',
          'L23_LBC',
          'L23_NBC',
          'L23_SBC',
          'L23_ChC',
          'L4_PC',              ### layer 4
          'L4_SP',
          'L4_SS',
          'L4_MC',
          'L4_BTC',
          'L4_DBC',
          'L4_BP',
          'L4_NGC',
          'L4_LBC',
          'L4_NBC',
          'L4_SBC',
          'L4_ChC',
          'L5_TTPC1',           ### layer 5
          'L5_TTPC2',
          'L5_UTPC',
          'L5_STPC',
          'L5_MC',
          'L5_BTC',
          'L5_DBC',
          'L5_BP',
          'L5_NGC',
          'L5_LBC',
          'L5_NBC',
          'L5_SBC',
          'L5_ChC',
          'L6_TPC_L1',          ### layer 6
          'L6_TPC_L4',
          'L6_UTPC',
          'L6_IPC',
          'L6_BPC',
          'L6_MC',
          'L6_BTC',
          'L6_DBC',
          'L6_BP',
          'L6_NGC',
          'L6_LBC',
          'L6_NBC',
          'L6_SBC',
          'L6_ChC']