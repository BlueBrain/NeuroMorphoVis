####################################################################################################
# Copyright (c) 2025, Open Brain Institute
# Author(s): Marwan Abdellah <marwan.abdellah@openbraininstitute.org>
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

import nmv
import nmv.enums 

####################################################################################################
# @draw_morphology_in_position
####################################################################################################
def draw_morphology_in_position(circuit_config, gid, population, 
                                unified_radii_value=0.0,
                                color=(0, 0, 0), location=None, scale=1.0):
    
    # Create default NMV options with fixed radius value for the visualization
    nmv_options = nmv.options.NeuroMorphoVisOptions()
    nmv_options.morphology.bevel_object_sides = 2
    nmv_options.morphology.gid = gid
    nmv_options.morphology.libsonata_config = circuit_config
    nmv_options.morphology.libsonata_population = population
    nmv_options.shading.morphology_coloring_scheme = nmv.enums.ColorCoding.HOMOGENEOUS_COLOR
    nmv_options.shading.morphology_soma_color = color 
    nmv_options.morphology.axon_branch_order = 1
    nmv_options.morphology.resampling_method = nmv.enums.Skeleton.Resampling.FIXED_STEP
    nmv_options.morphology.resampling_step = 1.0
    nmv_options.shading.morphology_material = nmv.enums.Shader.FLAT
    
    if (unified_radii_value > 0.0):
        nmv_options.morphology.sections_radii_scale = 1.0
        nmv_options.morphology.arbors_radii = nmv.enums.Skeleton.Radii.UNIFIED
        nmv_options.morphology.samples_unified_radii_value = unified_radii_value
    else:
        nmv_options.morphology.arbor_style = nmv.enums.Skeleton.Style.TAPERED
        nmv_options.morphology.sections_radii_scale = 1.15
        nmv_options.morphology.arbors_radii = nmv.enums.Skeleton.Radii.SCALED
    
    # Create a morphology object 
    morphology_object = nmv.file.readers.read_morphology_from_libsonata_circuit(options=nmv_options)
    
    # Create a builder         
    builder = nmv.builders.ConnectedSectionsBuilder(
                    morphology=morphology_object, options=nmv_options, disable_illumination=True)
    
    # Draw the morphology skeleton 
    morphology_objects = builder.draw_morphology_skeleton()
    
    for obj in morphology_objects:
        obj.scale[0] = scale 
        obj.scale[1] = scale 
        obj.scale[2] = scale 

    if location is not None:    
        for obj in morphology_objects:
            obj.location = location
        
    # Convert the objects into meshes 
    for object in morphology_objects:
        nmv.scene.convert_object_to_mesh(object)
        
    # Group them into a single object 
    neuron_mesh = nmv.scene.join_objects(morphology_objects)
    neuron_mesh.name = f'{gid}'
    
    return neuron_mesh