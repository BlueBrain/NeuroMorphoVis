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
