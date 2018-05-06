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
import os
import datetime


####################################################################################################
# @Logger
####################################################################################################
class Logger:
    """System logger
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self, path=None, print_stdout=True):
        """Constructor

        :param path:
            Log file path, by default None. If the path is not given, the log file will be
            created in the current directory.
        :param print_stdout:
            Print the messages to the standard output stream, True by default.
        """

        # Use the current working directory if no path is given
        if path is None:
            self.path = os.getcwd()

        # Print to the standard output stream
        self.print_stdout = print_stdout

        # Log file path
        self.log_file_path = '%s/nmv.log' % self.path
        print('Log file [%s]' % self.log_file_path)

        # Open the log file in the write mode for the first time only
        log_file = open(self.log_file_path, 'w')

        # Starting message and time
        log_file.write('NeuroMorphoVis - Marwan Abdellah (C) Blue Brain Project / EPFL \n')
        log_file.write(datetime.datetime.now().strftime("%I:%M %p on %B %d, %Y\n"))

        # Close
        log_file.close()

    ################################################################################################
    # @log
    ################################################################################################
    def log(self, *args):
        """Logging and printing to stdout.

        :param args:
            Input arguments.
        """

        # Make a string from the log args
        log_string = ' '.join(map(str, args))

        # Print the log message to stdout
        if self.print_stdout:
            print(log_string)

        # Open the log file in the append mode.
        log_file = open(self.log_file_path, 'a')

        # Append this message to the log string
        log_file.write(log_string + '\n')

        # Close the log file
        log_file.close()

    ################################################################################################
    # @line
    ################################################################################################
    def line(self):
        """Add a line to stdout.
        :return:
        """

        # Print the line message to stdout
        stars = '*******************************************************************************'
        if self.print_stdout:
            print(stars)

        # Open the log file in the append mode.
        log_file = open(self.log_file_path, 'a')

        # Append this message to the log string
        log_file.write(stars + '\n')

        # Close the log file
        log_file.close()
