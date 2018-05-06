"""modules.py:
    All project modules will be registered in this file.
"""

__author__      = "Marwan Abdellah"
__copyright__   = "Copyright (c) 2016 - 2017, Blue Brain Project / EPFL"
__version__     = "0.1.0"
__maintainer__  = "Marwan Abdellah"
__email__       = "marwan.abdellah@epfl.ch"
__status__      = "Production"

# System imports
import os, sys

# Append the internal scripts directories into the system paths
current_path = os.path.dirname(os.path.realpath(__file__))

# The paths of the different modules of the project
blender_module_path = "%s/../blender" % current_path
bmesh_module_path = "%s/../bmesh" % current_path
builders_module_path = "%s/../builders" % current_path
common_module_path = "%s/../common" % current_path
shared_module_path = "%s/../shared" % current_path
execution_module_path = "%s/../execution" % current_path
file_module_path = "%s/../file" % current_path
geometry_module_path = "%s/../geometry" % current_path
interface_module_path = "%s/../interface" % current_path
mesh_module_path = "%s/../mesh" % current_path
modules_module_path = "%s/../modules" % current_path
morphologies_module_path = "%s/../morphologies" % current_path
options_module_path = "%s/../options" % current_path
physics_module_path = "%s/../physics" % current_path
rendering_module_path = "%s/../rendering" % current_path
scene_module_path = "%s/../scene" % current_path
sketching_module_path = "%s/../sketching" % current_path
slurm_module_path = "%s/../slurm" % current_path
textures_module_path = "%s/../textures" % current_path

# Append the framework modules paths
sys.path.append(blender_module_path)
sys.path.append(bmesh_module_path)
sys.path.append(builders_module_path)
sys.path.append(common_module_path)
sys.path.append(shared_module_path)
sys.path.append(execution_module_path)
sys.path.append(file_module_path)
sys.path.append(interface_module_path)
sys.path.append(geometry_module_path)
sys.path.append(mesh_module_path)
sys.path.append(modules_module_path)
sys.path.append(morphologies_module_path)
sys.path.append(morphologies_module_path + '/readers')
sys.path.append(morphologies_module_path + '/skeleton')
sys.path.append(rendering_module_path)
sys.path.append(physics_module_path)
sys.path.append(options_module_path)
sys.path.append(scene_module_path)
sys.path.append(slurm_module_path)
sys.path.append(sketching_module_path)
sys.path.append(textures_module_path)
