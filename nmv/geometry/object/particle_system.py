####################################################################################################
# Copyright (c) 2016 - 2023, EPFL / Blue Brain Project
# Author: Marwan Abdellah <marwan.abdellah@epfl.ch>
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
import nmv.mesh
import nmv.shading


####################################################################################################
# @create_particle_system_for_vertices
####################################################################################################
def create_particle_system_for_vertices(mesh_object,
                                        name='Particle System',
                                        vertex_radius=1,
                                        particle_quality=4,
                                        display_method='RENDER',
                                        material=None):

    base_object = nmv.mesh.create_ico_sphere(name='%s Base' % name, subdivisions=particle_quality)
    nmv.mesh.shade_smooth_object(base_object)
    nmv.shading.set_material_to_object(mesh_object=base_object, material_reference=material)

    # Construct a particle system modifier
    particle_system_modifier = mesh_object.modifiers.new('%s PS' % name, 'PARTICLE_SYSTEM')

    # Create the particle system
    particle_system = mesh_object.particle_systems[particle_system_modifier.name]

    # Use a particle count equivalent to the same number of vertices of the mesh object
    particle_system.settings.count = len(mesh_object.data.vertices)

    # Timing
    particle_system.settings.frame_start = 1
    particle_system.settings.frame_end = 1
    particle_system.settings.lifetime = 1

    # Emit from the vertices
    particle_system.settings.emit_from = 'VERT'

    # Don't use the random emissions to avoid display issues
    particle_system.settings.use_emit_random = False

    # Adjust the size of the particle
    particle_system.settings.particle_size = vertex_radius
    particle_system.settings.display_size = vertex_radius

    # Display dots for the performance
    particle_system.settings.display_method = display_method # 'DOT'

    # Render objects since we cannot render Halos in the current version of Blender
    particle_system.settings.render_type = 'OBJECT'

    # Create a base object
    particle_system.settings.instance_object = base_object

    # Return a reference to the particle system
    return particle_system
