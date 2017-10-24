:orphan:

Reproducible Yocto builds
=========================

Intro
-----

This document describes how to configure a Yocto build so that it can be reproduced,
and how to reproduce such build.
The reproduction requires that additional artifacts are archived.


The AUTOREV problem
-------------------

A bitbake recipe specifies where the source code of a package should be downloaded from.
Because there are several ways to do this, a recipe might not specify a specific version but rather
the head of some branch or a latest release.

Even though this is not recommended, there is no guarantee that developers will not write recipes
to use ``AUTOREV`` to point to latest source revision.
This of course affects reproducibility as the maintainer of some upstream project may update the
head of the branch or the latest release between builds so that bitbaking the same version of
a recipe yields different results.
In addition, in cases when reproducibility of a Yocto build is required, the actual availability of
the upstream source code packages might cause a problem, e.g. if a tar archive is moved to some
other URL.

The general solution to guarantee reproducibility is to let the Yocto build environment create tar
archives of the downloaded sources and place these in a local mirror during a build.
This local mirror can then be used when reproducing the build, a solution that works in most cases.
The exception is when a package's source code is stored in a git repository and the recipe for the
package does not point to a specific commit but a tag, then Yocto won't create a tar archive for it since it has to fetch the latest revision that the tag points to.

Building with BB_NO_NETWORK
---------------------------

Setting the ``BB_NO_NETWORK`` variable to "1" in build/conf/local.conf disables network access for
bitbake during the build so that source code can only be fetched from specified local mirrors.
This is a good way to guarantee that only specific sources will be used. However, this also means
that bitbake will fail when issuing certain commands, for instance git ls-remote, and that it is
therefore important to use the ``SRC_REV`` variable instead of pointing to a tag in git-based
bitbake recipes. A typical failure could look like this:

.. code-block:: none

    Function failed: Network access disabled through BB_NO_NETWORK (or set indirectly due to use of BB_FETCH_PREMIRRORONLY) but access requested with command git ls-remote http://git.projects.genivi.org/ipc/common-api-dbus-runtime.git refs/heads/2.1.6 refs/tags/2.1.6^{} (for url None)
    ERROR: Task 715 (/mnt/ssd/yocto/the-reproduced-build/sources/meta-pelagicore/recipes-core/common-api/common-api-c++-dbus_2.1.6.bb, do_fetch) failed with exit code '1'

The poky layers do not allow recipes that cannot be built with ``BB_NO_NETWORK`` set to "1",
but other upstream layers might. If such a recipe is found in some other bitbake layer repository,
a bbappend file overriding the ``SRC_URL`` variable can be created so that the recipe instead will
point to a specific commit.


Configuring Yocto builds for reproducibility
--------------------------------------------

To create a local mirror, the following configuration needs to be added to build/conf/local.conf
(note that this is not a default configuration):

.. code-block:: none

    BB_GENERATE_MIRROR_TARBALLS = "1"

During the Yocto build process, packages are downloaded and stored in the downloads/ directory
(or whatever directory has been specified in build/conf/local.conf) of the Yocto build's
root directory.
When set to "1", ``BB_GENERATE_MIRROR_TARBALLS`` forces bitbake to create tar-balls for all the
sources that are fetched using git.
Note that the build must be done from scratch otherwise some source code packages may not be
packaged into tar-balls. In other words, the build cache needs to be wiped clean before the build
is started. When everything is set up, start the build as usual with bitbake.


Saving the repo manifest
------------------------

The above instructions describe how to create the local mirror.To be able to reproduce a build,
the manifest file used must also be saved.
The manifest with the exact commits used needs to be generated.
This can be done with the repo tool from the root of the Yocto build directory after the repo sync
command has been issued:

.. code-block:: bash

    $ repo manifest -o - -r >> example-manifest.xml

Reproducing the Yocto build
---------------------------

The instructions in this section describe how a Yocto build may be reproduced given that the
instructions in the above sections have been followed.
The download directory previously populated should be made available to the build environment to
be used during build reproduction, e.g. by copying the download directory from the archive to
a source directory in the root directory of the new Yocto build. The build directory should now
look like this:

.. code-block:: none

    .
    └── source-mirror/

When initializing the build directory, use a manifest that has been previously associated with
the release to be reproduced:

.. code-block:: bash

    $ repo init -u ssh://git@git.example.net/example-group/example-manifest-repository.git -b releases -m example-manifest.xml
    $ repo sync

Then follow the build instructions to export the TEMPLATECONF and source the build environment.

The build directory should now be initialized and look like this:

.. code-block:: none

    .
    ├── build/
    ├── source-mirror/
    └── sources/

Once the recipes have been fetched and the environment set up, add the following
lines to build/conf/local.conf:

.. code-block:: none

    SOURCE_MIRROR_URL ?= "file://${BSPDIR}/source-mirror/"
    INHERIT += "own-mirrors"
    BB_NO_NETWORK = "1"

The ``SOURCE_MIRROR_URL`` variable adds the local mirror to the list of mirrors.
When used in conjunction with the ``BB_NO_NETWORK``, bitbake is forced to turn to the local mirror
when fetching the source code packages because bitbake is not allowed network access.
Given that everything has been set up as described above, the build can be started as usual with
the bitbake command.
