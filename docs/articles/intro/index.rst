:orphan:

Introduction
************

This is the Software Factory Blueprint.

How to use the blueprint
========================
The blueprint is not intended to be particularly useful on its own, rather it is a collection of
generic descriptions, processes, how-tos et cetera.

The typical user of the blueprint is someone who wants to run a project where a Software Factory is
part of the project. The blueprint can then be used as a base and then be extended with
project-specific info, or one can just pick and choose the relevant parts from the blueprint.

We recommend using the blueprint in a project-specific setting as a *git submodule* from whichever
git contains the project-specific Software Factory. Our reference deployment `PELUX Baseline SWF
Deployment`_ does exactly that.

.. code-block:: bash

    pelux-software-factory
    ├── CMakeLists.txt
    ├── CONTRIBUTING.md
    ├── docs
    │   ├── chapters
    │   │   ├── baseplatform
    │   │   ├── ci-and-cd
    │   │   ├── intro
    │   │   ├── licensing
    │   │   ├── sdk
    │   │   └── workflow
    │   ├── CMakeLists.txt
    │   ├── cmake_modules
    │   │   └── FindSphinx.cmake
    │   ├── conf.py.in
    │   ├── index.rst
    │   ├── swf-blueprint
    │   │   ├── CMakeLists.txt
    │   │   ├── CONTRIBUTING.md
    │   │   ├── docs
    │   │   │   ├── articles
    │   │   │   ├── CMakeLists.txt
    │   │   │   ├── cmake_modules
    │   │   │   ├── conf.py.in
    │   │   │   ├── index.rst
    │   │   │   ├── python_modules
    │   │   │   └── swf-substitutions.txt
    │   │   ├── LICENSE
    │   │   └── README.md
    │   └── swf-substitutions.txt
    ├── Jenkinsfile
    ├── LICENSE
    ├── README.md
    └── scripts
        └── publish_docs.sh


Note that in the above file structure, the ``swf-blueprint`` is a git submodule that points to the
blueprint repository from the PELUX software factory repository.

.. _`Pelux Baseline SWF Deployment`: http://github.com/Pelagicore/software-factory/
