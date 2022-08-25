# System imports 
import random 

# Blender imports 
from mathutils import Vector 


####################################################################################################
# @get_exact_locations
####################################################################################################
def get_exact_locations():
    return [Vector((0.0, 0.0, 0.0)), 
            Vector((0.25, 0.25, 0.25)),
            Vector((0.5, 0.5, 0.5)),
            Vector((0.75, 0.75, 0.75)),
            Vector((1.0, 1.0, 1.0))]

####################################################################################################
# @get_random_locations
####################################################################################################
def get_random_locations(extent=5.0):
    random_locations = list()
    for i in range(5):
        x = random.uniform(-extent, extent)
        y = random.uniform(-extent, extent)
        z = random.uniform(-extent, extent)
        random_locations.append(Vector((x, y, z)))
    return random_locations
