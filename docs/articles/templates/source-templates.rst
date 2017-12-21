Template library
================

The template library provides an example CMake_ shared library project for
service developers.

To acquire the template service source code the user needs to fetch the
code from GitHub.

.. code-block:: bash

    git clone https://github.com/Pelagicore/template-library.git

Compilation and installation
----------------------------

.. code-block:: bash

    cd template-library
    mkdir build && cd build
    cmake -DCMAKE_INSTALL_PREFIX=/path/to/install/dir .. && make -j4
    make install

.. note:: The example above presents how to compile and install the template library natively on
          your host machine.


Template service
================

The template service serves as an example CMake_ project for service
developers that should be used as a starting point while creating platform
services.

To acquire the template service source code the user needs to fetch the
code from GitHub.

.. code-block:: bash

    git clone https://github.com/Pelagicore/template-service.git

Dependencies
------------

The template service depends on the template library. That is reflected in its `CMakeLists.txt`
file. The build system will check if the required dependencies are installed on the system through
pkg-config_.

Compilation and installation
----------------------------

.. code-block:: bash

    cd template-service
    mkdir build && cd build
    PKG_CONFIG_PATH=/path/to/install/dir/lib/pkgconfig \
    cmake -DCMAKE_INSTALL_PREFIX=/path/to/install/dir .. && make -j4
    make install

Running the template service
----------------------------

.. code-block:: bash

    LD_LIBRARY_PATH=/path/to/install/dir/lib \
    path/to/install/dir/bin/template-service

.. note:: The example above presents how to compile, install and run the template service natively
          on your host machine.

Install directory structure
===========================

Once the template service and library are installed, the layout of the installation will be as shown
below.

.. code-block:: bash

    .
    ├── bin
    │   └── template-service
    ├── include
    │   └── template-library
    │       └── templatepublicclass.h
    └── lib
        ├── libtemplate-library.so
        └── pkgconfig
            └── template-library.pc

.. _CMake: https://cmake.org/
.. _pkg-config: https://www.freedesktop.org/wiki/Software/pkg-config/
