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
import os, platform
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
    def __init__(self,
                 path=None,
                 print_stdout=True):
        """Constructor

        :param path:
            Log file path, by default None. If the path is not given, the log file will be
            created in the current directory.
        :param print_stdout:
            Print the messages to the standard output stream, True by default.
        """

        # Use the current working directory if no path is given
        if path is None:

            # MAC
            if str(platform.system()) == "Darwin":
                self.path = os.getenv("HOME")
            elif str(platform.system()) == "Windows":
                self.path = os.path.dirname(os.path.realpath(__file__))
            else:
                self.path = os.getenv("HOME")
        else:
            self.path = path

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
            print(log_string.replace('(\'', '').replace('\',)', ''))

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

    ################################################################################################
    # @header
    ################################################################################################
    def header(self,
               *args):
        """Log a header.

        :param args:
            Input arguments.
        """
        print("")  # Add a new line
        self.line()
        log_string = ''.join(map(str, args))
        self.log('    * %s' % log_string)
        self.line()

    ################################################################################################
    # @info
    ################################################################################################
    def info(self,
             *args):
        """Log a sub-header.

        :param args:
            Input arguments.
        """

        # Make a string from the log args
        log_string = ''.join(map(str, args))

        # Log the string
        self.log('\t* %s' % log_string)

    ################################################################################################
    # @detail
    ################################################################################################
    def detail(self,
               *args):
        """Log a sub-header.

        :param args:
            Input arguments.
        """

        # Make a string from the log args
        log_string = ''.join(map(str, args))

        # Log the string
        self.log('\t\t* %s' % log_string)
