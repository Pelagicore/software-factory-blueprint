:orphan:

Software Development Environment
********************************

PELUX Software Development Environment (SDE) is a tool that creates a virtual
machine with all the tools needed when developing towards a PELUX platform.
More specifically the SDE is setup using vagrant to generate a VirtualBox
instance. In order to facilitate this, the PELUX SDE requires an instance of
PELUX SDK to be present in the root directory (same level as Vagrantfile) while
provisioning the VM.

Starting the SDE
----------------
Dependencies:

* Vagrant
* VirtualBox

To start the PELUX SDE VM, go to root directory (the same directory as the
Vagrantfile is located in) the SDE run

.. code-block:: bash

    vagrant up

If this is the first time the PELUX SDE is started then the machine has
to be provisioned as well. Meaning downloading the Ubuntu base and installing
all software. As stated above, during provisioning an instance of PELUX SDK is
required in the root directory.

Used environment variables:
^^^^^^^^^^^^^^^^^^^^^^^^^^
Following is a list of environment variables used by vagrant when provisioning
the SDE.

* SDK_FILE_NAME: Name of the self-extracting SDK package to install into the
  SDE. Can include wildcards. Defaults to `oecore*toolchain*sh`.
* NO_GUI: Will create a headless SDE when set.


Developing and Extending the SDE
--------------------------------

Test framework
^^^^^^^^^^^^^^
The test framework is used to ensure that no existing functionallity is broken
while developing new features for the PELUX SDE. All tests are located in the
test directory and are run through pytest.

Dependencies:

* pytest

To run the test framework, run the following command in the root directory:

.. code-block:: bash

    test/run-tests.sh

.. note:: In order to do clean tests, this script will tear down and destroy
   the VM if it is already created

Stubbed SDK
^^^^^^^^^^^
Since the SDK takes a long time to download and a long time to extract the tests
use a stubbed version of the SDK. The stubbed version sets mock values for
everything that is needed during the setup but nothing is actually installed.
For instance is cmake setup by the stubbed SDK as a symlink to /bin/true.

Keep in mind that the stubbed SDK is intended to be minimal. Meaning it will not
set all environment variables and provide fake installations of all tools
installed by a real SDK. Therefore when developing new features for the SDE, it
is likely necessary to extend the stubbed SDK with more environment variables or
stubbed instances of tools.

