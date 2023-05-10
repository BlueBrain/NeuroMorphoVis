####################################################################################################
# Copyright (c) 2016 - 2023, EPFL / Blue Brain Project
#               Marwan Abdellah <marwan.abdellah@epfl.ch>
#
# Credits:      Ahmedt Bilgili
#               Juan Hernando
#               Stefan Eilemman
#               Henry Markram
#               Felix Shurmann
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

# System imports
import sys
import os
import imp

__author__      = "Marwan Abdellah"
__copyright__   = "Copyright (c) 2016 - 2023, Blue Brain Project / EPFL"
__credits__     = ["Ahmet Bilgili", "Juan Hernando", "Stefan Eilemann", "Nadir Roman"]
__maintainer__  = "Marwan Abdellah"
__email__       = "marwan.abdellah@epfl.ch"
__status__      = "Production"

####################################################################################################
# Add-on information
####################################################################################################
bl_info = {
    # The name of your add-on. This is shown in the add-on tab in Blender's user preferences
    "name": "NeuroMorphoVis",
    # The author of this add-on
    "author": "Marwan Abdellah",
    # A tuple, containing the add-on version
    "version": (1, 9, 0),
    # The earliest Blender version this add-on will work with. If you're not sure what versions of
    # Blender this add-on is compatible with, use the version of Blender you're developing
    # the add-on with.
    "blender": (3, 0, 0),
    # This is where users should look for this add-on.
    # "location": "View 3D > Edit Mode > Tool Shelf",
    # Description
    "description": "Morphology reconstruction, analysis and visualization to mesh reconstruction. "
                   "The Add-on was developed by the Blue Brain Project (BBP) at the Ecole "
                   "Polytechnique Federale de Lausanne (EPFL).",
    # Add-on category; shown on the left side of Blender's add-on list to make filtering simpler.
    # This must be one of the categories as listed in Blender's add-on tab; if it's not, it will
    # create a new category for your add-on (which may be good or bad.)
    # Don't create new categories to make your add-on stand out.
    "category": "3D View",
    # This support can be either 'OFFICIAL', 'COMMUNITY', or 'TESTING'. 'OFFICIAL' should only be
    # used if this add-on is included with Blender.
    # (If you're not sure, don't use 'OFFICIAL'.) 'COMMUNITY' and 'TESTING' are both fine to use.
    # Note that 'TESTING' add-ons aren't shown by default in Blender's add-on list.
    'support': 'COMMUNITY',
    # Optional: specifies the wiki URL for an add-on.
    # This will appear in this add-on listing as "Documentation".
    'wiki_url': 'https://github.com/BlueBrain/NeuroMorphoVis',
    # Bug tracker: specifies the bug-tracker URL for an add-on.
    'tracker_url': 'https://github.com/BlueBrain/NeuroMorphoVis/issues?utf8=%E2%9C%93&q=',
}

# Append the modules path to the system paths to be able to load the internal python modules
sys.path.append(os.path.dirname(os.path.realpath(__file__)))


####################################################################################################
# @register
####################################################################################################
def register():
    """Register the different modules of the interface"""

    # Import the modules
    import nmv.interface
    import nmv.utilities

    nmv.logger.header('Loading NeuroMorphoVis')
    nmv.logger.info('Version %s' % str(nmv.utilities.get_nmv_version()))
    nmv.logger.info('Copyrights (c) Blue Brain Project (BBP) / (EPFL) - 2023')
    nmv.logger.info('Principal Author: Marwan Abdellah')

    # Register panels
    nmv.interface.ui.register_common_operators()
    nmv.interface.ui.io.register_panel()
    nmv.interface.ui.analysis.register_panel()
    nmv.interface.ui.edit.register_panel()
    nmv.interface.ui.soma.register_panel()
    nmv.interface.ui.morphology.register_panel()
    nmv.interface.ui.synaptics.register_panel()
    nmv.interface.ui.mesh.register_panel()
    nmv.interface.ui.about.register_panel()
    nmv.logger.info_done('NeuroMorphoVis Loaded! Enjoy')


####################################################################################################
# @unregister
####################################################################################################
def unregister():
    """Unregister the different modules of the interface"""

    # Import the modules
    import nmv.interface

    nmv.logger.header('Unloading NeuroMorphoVis')

    # Un-register panels
    nmv.interface.ui.unregister_common_operators()
    nmv.interface.ui.io.unregister_panel()
    nmv.interface.ui.analysis.unregister_panel()
    nmv.interface.ui.edit.unregister_panel()
    nmv.interface.ui.soma.unregister_panel()
    nmv.interface.ui.morphology.registration.unregister_panel()
    nmv.interface.ui.synaptics.unregister_panel()
    nmv.interface.ui.mesh.unregister_panel()
    nmv.interface.ui.about.unregister_panel()
    nmv.logger.info_done('NeuroMorphoVis Unloaded!')


####################################################################################################
# __main__
####################################################################################################
if __name__ == "__main__":

    # Register the add-on, ENTRY POINT -> NeuroMorphoVis
    register()
