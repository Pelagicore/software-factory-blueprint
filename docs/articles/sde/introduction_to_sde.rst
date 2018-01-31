:orphan:

Software Development Environment
********************************

The Software Development Environment (SDE) is a tool that creates a virtual
machine with all the tools needed when developing towards a PELUX platform.
More specifically the SDE is setup using vagrant to generate a VirtualBox
instance. In order to facilitate this, the SDE requires an instance of
the SDK to be present in the root directory (same level as Vagrantfile) while
provisioning the VM.

Starting the SDE
----------------
Dependencies:

* Vagrant
* VirtualBox

To start the SDE VM, check out the repository, put the SDK into it's root
directory and from that directory (the same directory as the Vagrantfile is
located in) run:

.. code-block:: bash

    vagrant up

If this is the first time the SDE is started then the machine has
to be provisioned as well. Meaning downloading the Ubuntu base and installing
all software. As stated above, during provisioning an instance of the SDK is
required in the root directory.

Used environment variables
^^^^^^^^^^^^^^^^^^^^^^^^^^
Following is a list of environment variables used by vagrant when provisioning
the SDE.

* SDK_FILE_NAME: Name of the self-extracting SDK package to install into the
  SDE. Can include bash wildcards. Defaults to `oecore*toolchain*sh`.
* NO_GUI: Will create a headless SDE when set.


Developing and Extending the SDE
--------------------------------

Adding new tools
^^^^^^^^^^^^^^^^

To add a new tool to the SDE create a new directory in `sde-cookbook` with
the name of that tool, add your installation and configuration scripts there
and configure the `Vagrantfile` to run them in the right order.

The SDE is developed using TDD, so first write some tests and then write
the code which will make them pass. It's really important to have automatic
tests which will test for any regressions if someone changes parts of the
code.

Test framework
^^^^^^^^^^^^^^
The test framework is used to ensure that no existing functionality is broken
while developing new features for the PELUX SDE. All tests are located in the
test directory and are run through pytest.

Dependencies:

* pytest

To run the test framework, run the following command in the root directory:

.. code-block:: bash

    test/run-tests.sh

.. note:: In order to do clean tests, this script will tear down and destroy
   the VM if it is already created

Adding new tests
================

The tests are divided in base tests and the rest, the idea is to create a
new directory in `scripts` if you add a new tool or functionality and have
those tests in that directory so they can be run independently.

Stubbed SDK
^^^^^^^^^^^
Since the SDK takes a long time to download and a long time to extract the
tests use stubbed versions of a SDK. The stubbed version sets mock values for
everything that is needed during the setup but nothing is actually installed.
For instance is cmake setup by the stubbed SDK as a symlink to /bin/true.

Keep in mind that the stubbed SDK is intended to be minimal. Meaning it will
not set all environment variables and provide fake installations of all tools
installed by a real SDK. Therefore when developing new features for the SDE,
it is likely necessary to extend the stubbed SDK with more environment
variables or stubbed instances of tools.
