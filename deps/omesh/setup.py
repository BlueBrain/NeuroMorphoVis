####################################################################################################
# Copyright (c) 2023 - 2024 Marwan Abdellah < abdellah.marwan@gmail.com >
# Copyright (c) 1994 - Michael Holst and Zeyun Yu
#
# This file is part of OMesh, the OptimizationMesh library.
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
#
# OMesh is based on the GAMer (Geometry-preserving Adaptive MeshER) library, which is
# redistributable and is modifiable under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation as published by the Free Software
# Foundation; either version 2.1 of the License, or any later version.
####################################################################################################

# Imports
import setuptools
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
from setuptools.command.test import test as TestCommand
import glob
import os
import sys

####################################################################################################
# OMesh, the OptimizationMesh library.
####################################################################################################
__project_name__    = 'omesh'
__version__         = "0.1.0"
__author__          = 'Marwan Abdellah, Blue Brain Project (EPFL)'
__author_email__    = 'marwan.abdellah@epfl.ch'
__license__         = 'GNU GPL v3.0'


####################################################################################################
# @create_ext_modules
####################################################################################################
def create_ext_modules():

    # Get the base path of the project
    base_path = os.path.dirname(__file__)

    # Get all the *.cpp source file in the 'src' directory
    src_paths = ['src']
    src_files = list()
    for src in src_paths:
        src_files.extend(glob.glob(os.path.join(base_path, src, '*.cpp')))

    include_dirs = list()
    include_dirs.append(os.path.join(base_path, 'include'))

    # For OpenMP support
    if sys.platform == 'darwin':
        include_dirs.append('/opt/local/include')
        include_dirs.append('/usr/local/include')

    extra_compile_args = list()
    if sys.platform == 'unix':
        extra_compile_args.append('-fopenmp')
    elif sys.platform == 'darwin':
        extra_compile_args.append('-fopenmp')

    extra_link_args = list()
    if sys.platform == 'unix':
        extra_link_args.append('-lgomp')
    elif sys.platform == 'darwin':
        extra_link_args.append('-L/usr/local/lib')
        extra_link_args.append('-lomp')

    # Extra modules for the compilation
    ext_modules = [
        Extension(
            __project_name__,
            sources=src_files,
            extra_compile_args=extra_compile_args,
            extra_link_args=extra_link_args,
            include_dirs=include_dirs,
            language='c++',
            define_macros=[('VERSION_INFO', __version__),
                           ('PYBIND', None),],
            undef_macros=["NDEBUG"],
        ),
    ]

    return ext_modules


####################################################################################################
# @has_flag
####################################################################################################
def has_flag(compiler, flagname):
    """Return a boolean indicating whether a flag name is supported on the specified compiler.

    As of Python 3.6, CCompiler has a `has_flag` method (cf http://bugs.python.org/issue26689).
    """
    import tempfile
    with tempfile.NamedTemporaryFile('w', suffix='.cpp') as f:
        f.write('int main (int argc, char **argv) { return 0; }')
        try:
            compiler.compile([f.name], extra_postargs=[flagname])
        except setuptools.distutils.errors.CompileError:
            return False
    return True


####################################################################################################
# @cpp_flag
####################################################################################################
def cpp_flag(compiler):
    """Return the -std=c++[11/14/17] compiler flag.

    The c++14 is prefered over c++11 (when it is available).
    """
    if has_flag(compiler, '-std=c++17'):
        return '-std=c++17'
    if has_flag(compiler, '-std=c++14'):
        return '-std=c++14'
    elif has_flag(compiler, '-std=c++11'):
        return '-std=c++11'
    else:
        raise RuntimeError('Unsupported compiler -- at least C++11 support is needed!')


####################################################################################################
# @BuildExt
####################################################################################################
class BuildExt(build_ext):
    """A custom build extension for adding compiler-specific options."""
    c_opts = {
        'msvc': ['/EHsc'],
        'unix': [],
    }

    if sys.platform == 'darwin':
        c_opts['unix'] += ['-stdlib=libc++', '-mmacosx-version-min=10.7']

    def build_extensions(self):
        ct = self.compiler.compiler_type
        opts = self.c_opts.get(ct, [])
        if ct == 'unix':
            opts.append(cpp_flag(self.compiler))
            if has_flag(self.compiler, '-fvisibility=hidden'):
                opts.append('-fvisibility=hidden')

            # Adding the OpenMP compilation flag
            if sys.platform == 'darwin':
                opts.append('-fopenmp')
            else:
                opts.append('-fopenmp')
        for ext in self.extensions:
            ext.extra_compile_args = opts
        build_ext.build_extensions(self)


####################################################################################################
# @PyTest
####################################################################################################
class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def run_tests(self):
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


####################################################################################################
# @setup
####################################################################################################
setup(
    name=__project_name__,
    version=__version__,
    author=__author__,
    author_email=__author_email__,
    license=__license__,
    long_description=open('README.md').read(),
    ext_modules=create_ext_modules(),
    cmdclass={'build_ext': BuildExt},
    zip_safe=False,
)
