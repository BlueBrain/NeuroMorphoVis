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
import time


####################################################################################################
# @Timer
####################################################################################################
class Timer:

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self):
        """Constructor
        """

        # Starting time
        self.starting_time = 0.0

        # Ending time
        self.ending_time = 0.0

    ################################################################################################
    # @start
    ################################################################################################
    def start(self):
        """Start the timer.
        """

        # Start the timer
        self.starting_time = time.time()

    ################################################################################################
    # @end
    ################################################################################################
    def end(self):
        """End the timer.
        """

        # End the timer
        self.ending_time = time.time()

    ################################################################################################
    # @duration
    ################################################################################################
    def duration(self):
        """Get the duration of the timer in milliseconds.
        """

        # Return the duration in milliseconds.
        return self.ending_time - self.starting_time


####################################################################################################
# @profile_function
####################################################################################################
def profile_function(function, *args):
    """Runs a function and profiles it.
    :param function:
        Function object.
    :param args:
        Arguments to the function
    :return:
        Function result, Profiling string.
    """

    # Start the timer
    starting_time = time.time()

    # Run the function
    function_return = function(*args)

    # Stop the timer
    ending_time = time.time()

    # Compute the execution time
    execution_time = ending_time - starting_time

    # Construct the profiling string
    profiling_string = '\tStats. @%s: [%.3f]\n' % (function.__name__, execution_time)
    return function_return, profiling_string
