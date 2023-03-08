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

import sys 
import os 
import unittest

sys.path.append(('%s/.' % (os.path.dirname(os.path.realpath(__file__)))))

# Import all the tests here 
from tests.bmeshi import * 
from tests.consts import * 
#from tests.geometry import * 
from tests.mesh import * 


####################################################################################################
# @__main__
####################################################################################################
if __name__ == '__main__':

    # Verify the args
    sys.argv = [__file__] + (sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else [])
    
    # Run all the unit tests 
    print('\n\n* Running All NeuroMorphoVis Tests')
    unittest.main(verbosity=2)