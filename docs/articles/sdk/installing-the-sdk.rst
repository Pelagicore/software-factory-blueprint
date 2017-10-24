:orphan:

.. only:: blueprint

    With Yocto, one can create a Software Development Kit (SDK), for quick and easy development of
    software components that works well with the target system.

.. _installing-sdk:

Installing the SDK
------------------

The SDK file is not executable by default. This needs to be changed with `chmod`. If you downloaded
the SDK from the internet, the ``<SDK location>`` is typically ``~/Downloads``.

.. code-block:: bash

    cd <SDK location>
    chmod +x poky-glibc-x86_64-<image-name>-<arch>-toolchain-<version>.sh

It is a self extracting shell script which can be executed. This will start an interactive program
which first asks where to install the SDK. The easiest way is to install it in your `home` directory
in it's own directory, like `~/sdk`, instead of the default which is `/opt`. `/opt` is most probably
not prepared for your user to install anything into.

Example:

.. code-block:: bash

    ➜ jdoe@tux Downloads ./poky-glibc-x86_64-core-image-pelux-qt-corei7-64-toolchain-2.2.1.sh
    Poky (Yocto Project Reference Distro) SDK installer version 2.2.1
    =================================================================
    Enter target directory for SDK (default: /opt/poky/2.2.1): ~/sdk
    You are about to install the SDK to "/home/jdoe/sdk". Proceed[Y/n]? Y
    Extracting SDK.............done
    Setting it up...done
    SDK has been successfully set up and is ready to be used.

Now the SDK is installed and can be used.

.. tags:: howto
