.. _create-a-swf-deployment:

Create a SWF deployment
***********************

This howto describes how to practically go about creating a new instance
of a software factory by configuring git, creating directories and
indexes.

Create a git repo for the SWF Deployment
========================================

To create a new SWF Deployment, you first need to create a new repository
on your project git server and call it something meaningful, most
probably with the name of the project in it like: "example-software-factory".

.. code-block:: bash

    mkdir example-software-factory
    cd example-software-factory
    git init
    git remote add origin <git-url>
    echo "# example-software-factory" > README.md
    git add .
    git commit -m "Initial commit"
    git push -u origin master

Add SWF Platform Blueprint as submodule
=======================================

The blueprint contains a lot of articles of general nature, those can be
used to pre-populate the SWF Deployment. To do that the SWF Platform
Blueprint needs to be added as a git submodule.

.. code-block:: bash

    mkdir docs
    cd docs
    git submodule add https://github.com/Pelagicore/software-factory-blueprint.git swf-blueprint
    git add .
    git commit -m "Add SWF-Blueprint as submodule"

This will create a directory named 'software-factory-blueprint' and check
the SWF-Blueprint code out there. By adding and committing this, the
checked out version (in this case head of the master branch of the
SWF-blueprint) will be used.

Next time when cloning, it will need an additional step like this:

.. code-block:: bash

    git clone --recursive <git-url>

Create skeletal index file
==========================

One file which needs special attention is the docs/index.rst file, which
is the entry point of the new SWF Deployment.

.. code-block:: rst

    Welcome to the Example SWF documentation
    ****************************************
    
    Revision: |release|
    
    .. toctree::
        :caption: Table of contents
        :maxdepth: 3
    
        chapters/example/index
    
    .. toctree::
        :caption: Categories
        :maxdepth: 1
    
        categories/howto.rst

This is just a skeleton which needs to be populated with links to all
the articles which should show up.

Set variables and "substitutions"
=================================

Throughout the SWF Blueprint sometimes words and variables are used
which need to be substituted with something else in the SWF Deployment.
To be able to use this functionality those variables need to be defined
in the docs/swf-substitutions.txt file:

.. code-block:: bash

    # Key=Value. Don't keep '=' in the value
    # Blank lines and lines starting with # are ignored
    # Example: proj_name=PELUX
    
    proj_name=Example Software Factory
    example-sdk-binary=test-binary

Add needed files
================

Normally you only the files config.py and index.rst to create a Sphinx
documentation, but we recommend a file structure like this:

.. code-block:: bash

    example-software-factory
    ├── CMakeLists.txt
    ├── docs
    │   ├── categories
    │   │   ├── howto.rst
    │   │   ├── instruction.rst
    │   │   └── process.rst
    │   ├── chapters
    │   │   └── example
    │   │       ├── index.rst
    │   │       └── my-example.rst
    │   ├── CMakeLists.txt
    │   ├── cmake_modules
    │   │   └── FindSphinx.cmake
    │   ├── conf.py.in
    │   ├── index.rst
    │   ├── swf-blueprint
    │   └── swf-substitutions.txt
    └── README.md

The content of the files can be copied and adapted from the PELUX Baseline
Software Factory which is one such SWF Deployment. The README.md should
contain a description on how to build the project with CMake.

.. tags:: howto
