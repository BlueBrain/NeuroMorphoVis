####################################################################################################
# Copyright (c) 2016 - 2023, EPFL / Blue Brain Project
# Author: Marwan Abdellah <marwan.abdellah@epfl.ch>
#
# This file is part of NeuroMorphoVis <https://github.com/BlueBrain/NeuroMorphoVis>
#
# The code in this file is based on the Tesselator add-on, version 1.28, that is provided by
# Jean Da Costa Machado. The code is available at https://github.com/jeacom25b/Tesselator-1-28
# which has a GPL license similar to NeuroMorphoVis.
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

# Blender imports
import bpy
import bgl
import gpu
from gpu_extras.batch import batch_for_shader
from mathutils import Vector
from mathutils import Matrix

# Internal imports
import nmv.consts

####################################################################################################
# General vertex shader
####################################################################################################
vertex_shader = '''
uniform mat4 ModelViewProjectionMatrix;
in vec3 pos;
in vec4 color;
out vec4 finalColor;

void main()
{
    gl_Position = ModelViewProjectionMatrix * vec4(pos, 1.0);
    gl_Position.z -= 0.001;
    finalColor = color;
}

'''

####################################################################################################
# Vertex shader for the particle
####################################################################################################
point_vertex_shader = '''
uniform mat4 ModelViewProjectionMatrix;
in vec3 pos;
in vec4 color;
out vec4 finalColor;

void main()
{
    gl_Position = ModelViewProjectionMatrix * vec4(pos, 1.0);
    gl_Position.z -= 0.002;
    finalColor = color;
}

'''

####################################################################################################
# General fragment shader
####################################################################################################
fragment_shader = """
in vec4 finalColor;
in vec4 fragCoord;
out vec4 fragColor;
out float fragDepth;

void main()
{
    vec2 coord = gl_PointCoord - vec2(0.5, 0.5);
    fragColor = finalColor;
    fragDepth = 0;
}   
"""

####################################################################################################
# Fragment shader for the particle
####################################################################################################
point_fragment_shader = """
in vec4 finalColor;
in vec4 fragCoord;
out vec4 fragColor;
out float fragDepth;

void main()
{
    vec2 coord = (gl_PointCoord - vec2(0.5, 0.5)) * 2.0;
    float fac = dot(coord, coord);
    if (fac > 0.5){
        discard;
    }
    fragColor = finalColor;
    fragDepth = 0;
}   
"""


####################################################################################################
# DrawCallback
####################################################################################################
class DrawCallback:
    """Drawing call back to update the drawing of the particle system.
    This is a utility module for drawing lines in the 3D viewport on Blender 2.8 using the GPU API.
    The idea is to get rid of messy draw functions and data that is hard to keep track. This class
    works directly like a callable draw handler and keeps track of all the geometry data.
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self):
        """Constructor
        """

        # Useful for rendering in the same space of an object
        self.matrix = Matrix().Identity(4)

        # X-ray mode, draw through solid objects
        self.draw_on_top = False

        # Blend mode to choose, set it to one of the blend constants.
        self.blend_mode = nmv.consts.Drawing.BLEND

        # Line width for the edges
        self.line_width = nmv.consts.Drawing.LINE_WIDTH

        # Point size of the particle
        self.point_size = nmv.consts.Drawing.PARTICLE_SIZE

        # Handler Placeholder
        self.draw_handler = None

        # A list of the coordinates of the line
        self.line_coords = list()

        # A list of the colors of the line
        self.line_colors = list()

        # A list of the coordinates of the particle
        self.point_coords = list()

        # A list of the colors of the particle
        self.point_colors = list()

        # Shaders
        self._line_shader = gpu.types.GPUShader(vertex_shader, fragment_shader)
        self._point_shader = gpu.types.GPUShader(point_vertex_shader, point_fragment_shader)

        # Batches
        self._line_batch = batch_for_shader(
            self._line_shader, 'LINES', {"pos": self.line_coords, "color": self.line_colors})
        self._point_batch = batch_for_shader(
            self._line_shader, 'POINTS', {"pos": self.point_coords, "color": self.line_colors})

    ################################################################################################
    # @__call__
    ################################################################################################
    def __call__(self, *args, **kwargs):
        """ Makes this object behave like a function to add it like a draw handler.
        """

        self._draw()

    ################################################################################################
    # @setup_handler
    ################################################################################################
    def setup_handler(self):
        """Add the draw handler.
        """

        self.draw_handler = bpy.types.SpaceView3D.draw_handler_add(self, (), "WINDOW", "POST_VIEW")

    ################################################################################################
    # @remove_handler
    ################################################################################################
    def remove_handler(self):
        """Utility function to remove the handler.
        """

        self.draw_handler = bpy.types.SpaceView3D.draw_handler_remove(self.draw_handler, "WINDOW")

    ################################################################################################
    # @update_batch
    ################################################################################################
    def update_batch(self):
        """This takes the data rebuilds the shader batch. Call it every time you clear the data or
        add new lines, otherwise, you wont see changes in the viewport.
        """

        coords = [self.matrix @ Vector(coord) for coord in self.line_coords]
        self._line_batch = batch_for_shader(
            self._line_shader, 'LINES', {"pos": coords, "color": self.line_colors})

        coords = [self.matrix @ Vector(coord) for coord in self.point_coords]
        self._point_batch = batch_for_shader(
            self._point_shader, 'POINTS', {"pos": coords, "color": self.point_colors})

    ################################################################################################
    # @add_line
    ################################################################################################
    def add_line(self,
                 start,
                 end,
                 color1=(1, 0, 0, 1),
                 color2=None):
        """A simple add_line function, support color gradients, if only color1 is specified, it
        will be solid color (color1 on both ends).
        This doesnt render a line, it just adds the vectors and colors to the data so after calling
        update_batch(), it will be converted in a buffer object.

        :param start:
            Beginning of the line.
        :param end:
            End of the line.
        :param color1:
            Color 1
        :param color2:
            Color 2
        """

        # Coordinates
        self.line_coords.append(Vector(start))
        self.line_coords.append(Vector(end))

        # Colors
        self.line_colors.append(color1)
        if color2 is None:
            self.line_colors.append(color1)
        else:
            self.line_colors.append(color2)

    ################################################################################################
    # @add_point
    ################################################################################################
    def add_point(self,
                  location,
                  color=(1, 0, 0, 1)):
        """Adds a point for the particle.

        :param location:
            Point location.
        :param color:
            Point color.
        """

        # Location
        self.point_coords.append(location)

        # Color
        self.point_colors.append(color)

    ################################################################################################
    # @clear_data
    ################################################################################################
    def clear_data(self):
        """Clears all the data.
        """

        # Update the lists automatically clears all of them
        self.line_coords = list()
        self.line_colors = list()
        self.point_coords = list()
        self.point_colors = list()

    ################################################################################################
    # @_start_drawing
    ################################################################################################
    def _start_drawing(self):
        """Starts the drawing.
        """

        # This handles all the settings of the renderer before starting the draw stuff
        matrix = bpy.context.region_data.perspective_matrix
        self._line_shader.uniform_float("ModelViewProjectionMatrix", matrix)

        # GL_MULTISAMPLE
        bgl.glEnable(bgl.GL_MULTISAMPLE)

        # Blender mode
        if self.blend_mode == nmv.consts.Drawing.BLEND:
            bgl.glEnable(bgl.GL_BLEND)

        elif self.blend_mode == nmv.consts.Drawing.MULTIPLY_BLEND:
            bgl.glEnable(bgl.GL_BLEND)
            bgl.glBlendFunc(bgl.GL_DST_COLOR, bgl.GL_ZERO)

        elif self.blend_mode == nmv.consts.Drawing.ADDITIVE_BLEND:
            bgl.glEnable(bgl.GL_BLEND)
            bgl.glBlendFunc(bgl.GL_ONE, bgl.GL_ONE)

        if self.draw_on_top:
            bgl.glDisable(bgl.GL_DEPTH_TEST)

        # Line width
        bgl.glLineWidth(self.line_width)

        # Point size
        bgl.glPointSize(self.point_size)

    ################################################################################################
    # @update_batch
    ################################################################################################
    def _stop_drawing(self):
        """Stops drawing. It just reset some OpenGL stuff to not interfere with other drawings
        in the viewport # its not absolutely necessary but makes it safer.
        """

        # Disable blending
        bgl.glDisable(bgl.GL_BLEND)

        # Default line width
        bgl.glLineWidth(1)

        # Default point size
        bgl.glPointSize(1)
        if self.draw_on_top:
            bgl.glEnable(bgl.GL_DEPTH_TEST)

    ################################################################################################
    # @update_batch
    ################################################################################################
    def _draw(self):
        """This should be called by __call__, just regular routines for rendering in the viewport
        as a draw_handler.
        """

        self._start_drawing()
        self._line_shader.bind()
        self._line_batch.draw(self._line_shader)
        self._point_shader.bind()
        self._point_batch.draw(self._point_shader)
        self._stop_drawing()
