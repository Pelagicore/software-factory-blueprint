Yocto Project integration
=========================

This section describes how to include a shared library or platform service in the target image using
the `Yocto Project`_. A key part of this is an open source build system, based around the
OpenEmbedded architecture, that enables developers to create their own Linux distribution specific
to their environment. BitBake_ is the build tool used in this setup:

    BitBake executes tasks according to provided metadata that builds up the tasks. Metadata is
    stored in recipe (.bb) and related recipe "append" (``.bbappend``) files, configuration
    (``.conf``) and underlying include (``.inc``) files, and in class (``.bbclass``) files. The
    metadata provides BitBake with instructions on what tasks to run and the dependencies between
    those tasks.

The developed software components are added to the project through a BitBake recipe file that, as
mentioned above, stores the component metadata. Guidelines on how to write BitBake recipes can be
found in the `Yocto reference manual`_ and the reference structure is described in the `OpenEmbedded
style guide`_.

Template recipes
----------------

Below is a template Yocto recipe for the template-service. See inline comments for description of
the different fields available.

.. code-block:: bash

    # Various meta-data. Description is the only mandatory field here.
    SUMMARY = "A template C/C++ service"
    DESCRIPTION = "A C/C++ source code repository blueprint"
    AUTHOR = "Gordan Markuš <gordan.markus@pelagicore.com>"
    HOMEPAGE = "https://github.com/Pelagicore/template-service"

    # Short license name and where to find the license file plus its checksum. This is so that yocto
    # can check if the license text changes in newer versions of the software
    LICENSE = "MPL-2.0"
    LIC_FILES_CHKSUM = "file://LICENSE;md5=815ca599c9df247a0c7f619bab123dad"

    # Dependencies for building this software.
    DEPENDS = "template-library"

    # Version and revision. It is in general possible to have several versions of the same software
    # on the same system
    PV = "1.0+git${SRCREV}"
    PR = "r0"

    # Where to find the sources and, in the case the source is at a cvs, what revision to build
    SRCREV = "5bce3d20f996dac7e3882f48f5057abb7e1d05f5"
    SRC_URI = "git://github.com/Pelagicore/template-service.git;protocol=https;branch=master"

    # Where the sources are placed
    S = "${WORKDIR}/git/"

    # What classes to use. The template-service is a cmake project that uses pkgconfig. In general,
    # just inheriting these classes makes building completely automatic without any need to tinker.
    inherit cmake pkgconfig


Target image integration
------------------------

To include the template service in the target image, the following line has to be added to the
target image BitBake recipe:

.. code-block:: bash

    IMAGE_INSTALL += "template-service"

Observe that there is no need to add the template library explicitly. The template library will be
included implicitly because the template service depends on it.

.. _Yocto Project: https://www.yoctoproject.org/
.. _BitBake: https://www.yoctoproject.org/docs/current/bitbake-user-manual/bitbake-user-manual.html
.. _Yocto reference manual: http://www.yoctoproject.org/docs/current/ref-manual/ref-manual.html
.. _OpenEmbedded style guide: http://www.openembedded.org/wiki/Styleguide
