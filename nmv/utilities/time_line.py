####################################################################################################
# Copyright (c) 2016 - 2018, EPFL / Blue Brain Project
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

# System imports
import sys

# Blender imports
import bpy

# Internal imports
import nmv
import nmv.consts
import nmv.utilities


####################################################################################################
# @show_progress
####################################################################################################
def show_progress(message,
                  current,
                  total,
                  done=False):
    """Show the progress of a process in a loop.

    :param message:
        The output message.
    :param current:
        The current step.
    :param total:
        Total number of steps
    :param done:
        Is it the last step or not?
    """

    if done:

        # Done message
        sys.stdout.write('\t%s: [100 %%]%s' % (message, nmv.consts.Messages.SPACES))
        sys.stdout.write('\n')
    else:

        # In progress message
        progress = 100.0 * (float(current) / float(total))
        sys.stdout.write('\t%s: [%2.2f %%]\r' % (message, progress))


####################################################################################################
# @show_iteration_progress
####################################################################################################
def show_iteration_progress(message,
                            current,
                            total,
                            done=False):
    """Show the progress of a process in a loop.

    :param message:
        The output message.
    :param current:
        The current step.
    :param total:
        Total number of steps
    :param done:
        Is it the last step or not?
    """

    if done:

        # Done message
        sys.stdout.write('%s: [%d/%d]\n' % (message, current, total))

    else:

        # In progress message
        sys.stdout.write('%s: [%d/%d]\r' % (message, current, total))


####################################################################################################
# @play_simulation
####################################################################################################
def play_simulation(first_frame_index=1,
                    last_frame_index=100):
    """Run the physics simulations by proceeding through the time-line.

    :param first_frame_index:
        The index of the first frame in the simulation.
    :param last_frame_index:
        The index of the last frame in the simulation.
    """

    # Set the time-line frame, one by one, where the simulation will be activated
    simulation_timer = nmv.utilities.timer.Timer()
    simulation_timer.start()

    for frame in range(first_frame_index, last_frame_index):

        # Show progress
        show_progress('Simulation', frame, last_frame_index)

        # Update the time-line
        bpy.context.scene.frame_set(frame)

    simulation_timer.end()
    show_progress('Simulation', last_frame_index, last_frame_index, done=True)

    # Display the simulation time
    nmv.logger.log('Simulation time [%f] seconds' % simulation_timer.duration())
