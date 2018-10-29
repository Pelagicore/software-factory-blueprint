Template library
================

The template library provides an example CMake_ shared library project for
service developers.

To acquire the template service source code the user needs to fetch the
code from GitHub.

.. code-block:: bash

    git clone https://github.com/Pelagicore/template-library.git

The library also uses the googletest_ and googlemock_ projects for unit testing.

Compilation and installation
----------------------------

.. code-block:: bash

    cd template-library
    mkdir build && cd build
    cmake -DCMAKE_INSTALL_PREFIX=/path/to/install/dir .. && make -j4
    make install

.. note:: The example above presents how to compile and install the template library natively on
          your host machine.

Using googletest in your project
--------------------------------

The template library can also serve as a good example on how to add googletest_
and googlemock_ to your own projects.
It provides a couple of CMake modules which greatly simplify the deployment of
those packages:

* AddGMock_: provides the `add_gmock()` macro which takes care of downloading
  `googletest` and adding it as a subproject of your project. Note that
  `googlemock` is part of `googletest`, so it will also be available when
  `googletest` is downloaded. Just add the following lines to your
  `CMakeLists.txt`:

  .. code-block:: cmake

    include(AddGMock)
    add_gmock()

* AddGTestTest_: provides the `add_gtest_test()` macro, which you can use to
  add a test binary to your build. The macro takes three parameters:

  1. Name of the test executable to be created;
  2. List of source files for the test (the macro takes care of adding the
     googletest and googlemock related files, so you do not have to worry
     about them);
  3. Any additional libraries needed by your test. If none, use `""`.

These modules need to be saved into the `cmake_modules` directory located at
the root of your project (if it does not exist, create it).

A practical example of how `googletest` can be added to your existing project
can be found in `this commit
<https://github.com/Pelagicore/template-library/commit/6318ef12754de503e34d16121ccf3597bf48360b>`_.

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
.. _googletest: https://github.com/google/googletest
.. _googlemock: https://github.com/google/googletest/tree/master/googlemock
.. _AddGMock: https://github.com/Pelagicore/template-library/blob/master/cmake_modules/AddGMock.cmake
.. _AddGTestTest: https://github.com/Pelagicore/template-library/blob/master/cmake_modules/AddGTestTest.cmake
