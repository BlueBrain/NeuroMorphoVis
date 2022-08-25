import sys 
import os 
import unittest

sys.path.append(('%s/.' % (os.path.dirname(os.path.realpath(__file__)))))

# Import all the tests here 
# bmeshi
from test_bmesh_objects import * 
from test_bmesh_vertex_ops import * 
from test_bmesh_face_ops import * 


####################################################################################################
# @__main__
####################################################################################################
if __name__ == '__main__':

    # Verify the args
    sys.argv = [__file__] + (sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else [])
    
    # Run all the unit tests 
    print('\n\n* Running All NeuroMorphoVis Tests')
    unittest.main(verbosity=2)