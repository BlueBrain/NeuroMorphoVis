####################################################################################################
# Copyright (c) 2016 - 2018, EPFL / Blue Brain Project
#               Marwan Abdellah <marwan.abdellah@epfl.ch>
#
# This file is part of NeuroMorphoVis <https://github.com/BlueBrain/NeuroMorphoVis>
#
# This library is free software; you can redistribute it and/or modify it under the terms of the
# GNU Lesser General Public License version 3.0 as published by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License along with this library;
# if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301 USA.
####################################################################################################

__author__      = "Marwan Abdellah"
__copyright__   = "Copyright (c) 2016 - 2018, Blue Brain Project / EPFL"
__credits__     = ["Ahmet Bilgili", "Juan Hernando", "Stefan Eilemann"]
__version__     = "1.0.0"
__maintainer__  = "Marwan Abdellah"
__email__       = "marwan.abdellah@epfl.ch"
__status__      = "Production"

# System imports
import sys

# Blender imports
import bpy

# Internal imports
import neuromorphovis as nmv
import neuromorphovis.consts
import neuromorphovis.utilities


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
        sys.stdout.write('%s:  [100 %%]%s\n' % (message, nmv.consts.Messages.SPACES))

    else:

        # In progress message
        progress = 100.0 * (float(current) / float(total))
        sys.stdout.write('%s:  [%2.2f %%]\r' % (message, progress))


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
