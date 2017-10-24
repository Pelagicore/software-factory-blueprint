:orphan:

Deploying and running a binary executable on target
===================================================

Once you have a cross compiled binary file, it needs to be installed on the target. To do so the
easiest way is to use SSH. For that to work you need to know the IP address of your target.

.. note:: If you don't know the IP address of your target, the `Raspberry Pi documentation`_ describes how to find a new device on the network. This can be used for any target, not just Raspberry Pi

.. _`Raspberry Pi documentation`: https://www.raspberrypi.org/documentation/remote-access/ip-address.md

The default user on the |proj_name| image is `root` and it doesn't ask for a password logging in via SSH.
Use `scp` to copy your binary to the target.

.. code-block:: bash

    scp build/|example-sdk-binary| root@<ip address>:

Now that the binary file has been copied to the target it can be run there.

.. code-block:: bash

    ssh root@<ip address>
    ./|example-sdk-binary|
