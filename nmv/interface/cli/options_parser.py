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

# Internal imports
import nmv


####################################################################################################
# @OptionsParser
####################################################################################################
class OptionsParser:
    """Convert the parsed command line arguments into a structure that will be passed directly to
    the interface functions.
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self,
                 arguments):
        """Constructor

        :param arguments:
            Input command line arguments.
        """

        # Input arguments
        self.arguments = arguments

        # System options
        import nmv.options
        self.options = nmv.options.NeuroMorphoVisOptions()

    ################################################################################################
    # @get_bool
    ################################################################################################
    @staticmethod
    def get_bool(args,
                 flag):
        """Loop over all the items in the 'args' list, if found return True, else returns False!

        :param args: Input arguments to the application.
        :param flag: The identifier of a string option.
        :return: True or False.
        """
        for arg in args:
            if arg == flag:
                return True

        return False

    ################################################################################################
    # @get_string
    ################################################################################################
    @staticmethod
    def get_string(args,
                   flag):
        """Loop over all the items in the 'args' list, if found returns the value of the following
        item. If the flag is not found, return None!

        :param args:
            Input arguments to the application.
        :param flag:
            The identifier of a string option.
        :return:
            String (if found) or None (if not found).
        """
        for i, arg in enumerate(args):
            if arg == flag:
                return args[i + 1]

        return None

    ################################################################################################
    # @get_int
    ################################################################################################
    @staticmethod
    def get_int(args,
                flag):
        """Loop over all the items in the 'args' list, if found returns the int (value) of the
        following item. If the flag is not found, return None!

        :param args:
            Input arguments to the application.
        :param flag:
            The identifier of a string option.
        :return:
            Integer or None.
        """
        for i, arg in enumerate(args):
            if arg == flag:
                return int(args[i + 1])

        return None

    ################################################################################################
    # @get_float
    ################################################################################################
    @staticmethod
    def get_float(args,
                  flag):
        """Loop over all the items in the 'args' list, if found returns the float (value) of the
        following item. If the flag is not found, return None!

        :param args:
            Input arguments to the application.
        :param flag:
            The identifier of a string option.
        :return: Float or None.
        """
        for i, arg in enumerate(args):
            if arg == flag:
                return float(args[i + 1])

        return None
