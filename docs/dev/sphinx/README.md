# Developer reference

## Building the documentation

To build the developer reference you need Sphinx. For generating the html
pages go into `docs/dev/sphinx` and type `make html` if your are under a
Unix-style systems or run `make.bat html` in case of a Window system.

## Updating the documentation stubs

The source files for Sphinx rely on the autodoc extensions to generate the
documentation directly from NeuroMorphoVis' modules. However the process
is not fully automatic, as the stub `.rst` files with the modules to be
documented need to be generated before Sphinx is run. These stubs can be
automatically generated with `sphinx-autodoc`.

If you are adding new modules/packages or renaming any of the existing ones, you
will have to update the stubs before generating the documentation. For that
purpose go to `docs/dev/sphinx` and then run
`sphinx-apidoc -o . ../../../neuronmorphovis`. Make sure that `.rst` sources
that are no more needed are removed after you run the previous command.
Afterwards you can generate the documentation as usual.
