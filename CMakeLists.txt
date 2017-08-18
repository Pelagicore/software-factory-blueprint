# This file is part of the Software Factory Blueprint project
# Copyright (C) Pelagicore AB
# SPDX-License_identifier: LGPL-2.1
# This file is subject to the terms of the LGPL-2.1 license.
# Please see the LICENSE file for details.

# The project is buildable in it self but is intended to be used
# as a submodule in a "Deployment" in which case we should not
# build anything here, but rather let the using project do that
# work. If we are not currently the top level cmake file, we do
# nothing.
if(CMAKE_SOURCE_DIR STREQUAL CMAKE_CURRENT_SOURCE_DIR)

cmake_minimum_required(VERSION 3.0.2)

project(software-factory-blueprint VERSION 0.1.0)

add_subdirectory(docs)

endif(CMAKE_SOURCE_DIR STREQUAL CMAKE_CURRENT_SOURCE_DIR)
