:orphan:

C/C++ templates
***************

The templates serve as example CMake_ projects for service developers
that should be used as a starting point while creating platform services
or shared libraries, as well as as a set of guidelines to follow in source
repositories. The guidelines described are not set-in-stone. Also, in
general, consistency is better than getting stuck on difficult-to-apply
guidelines so please use these to an extent which is reasonable. The point
is to support a common pattern within the project.

In order to compile the templates natively the user needs to use the CMake
build system. The CMake build system can be installed by following the
instructions on the `CMake install webpage`_ or by using your Linux
distribution's package manager.

.. include:: directory-structure.rst
.. include:: source-templates.rst
.. include:: yocto-templates.rst

.. _CMake: https://cmake.org/
.. _CMake install webpage: https://cmake.org/install/
