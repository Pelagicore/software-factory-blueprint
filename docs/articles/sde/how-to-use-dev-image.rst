:orphan:

How to use development image
============================
.. tags:: howto

Introduction
-------------
The dev image is a superset of its corresponding production image for each
variant, furthermore, it includes some more packages and tools, e.g. gdb,
strace, etc. for the sake of developing an debugging convenience. Therefore,
the dev image will be delivered together with the production image for each
variant in the end.

Get dev image:
--------------
There are two ways to get the dev image:

#. Download pre-build image from CI server 
#. Build locally


Boot up QEMU dev image
----------------------

The handy QEMU launch script ``qemu_launcher`` is used to boot up dev image


.. code-block:: bash

   ./qemu_launcher -f FOLDER -i core-image-pelux-minimal-qemux86-64.ext4 --dev

Note that the SSH port 22 is forwarded to 1234 by default, and an extra port
3333 is also exposed by the command for remote debugging later.
To learn more about boot up QEMU see :ref:`booting-a-qemu-image` or check the
usage of the script

.. code-block:: bash

    ./qemu_launcher -h

The QEMU dev image can be accessed via SSH now

.. code-block:: bash

    $ ssh root@127.0.0.1 -p 1234


The instructions above covered how to obtain the SDK and boot up QEMU dev image,
steps below will show cross-compiling an example service (template-service) for
the target, and then run a remote debugger on it.

Cross compile template-service
------------------------------

SDK can be fetched from pre-build CI server or local build, the same as way
fetching images. 

- Install SDK

.. code-block:: bash

    cd <SDK location>
    chmod +x pelux-glibc-x86_64-<image-name>-<arch>-toolchain-<version>.sh
    ./pelux-glibc-x86_64-<image-name>-<arch>-toolchain-<version>.sh

More details see :ref:`installing-sdk`

- Cross Compiling

.. code-block:: bash

    cd <SDK location>
    source environment-setup-<arch>-poky-linux

Note that template-service should be cloned into your local disk

.. code-block:: bash

    cd <template-service folder>
    mkdir build && cd build
    cmake ..
    make

More details see :ref:`sourcing-the-environment`

- Deploy to target

.. code-block:: bash

    scp build/template-service root@<ip address>:

Now the binary file has been copied to the target and it can be run there.

.. code-block:: bash

    ssh root@<ip address>
    ./template-service


Remote Debugging
-----------------

The script ``gdb_helper`` has wrapped the functions needed to deal with gdb and gdbserver


.. code-block:: bash

	./gdb_helper -h
	usage: ./gdb_helper [options]
	[options] is any of the following:
	  -f | --file            	Transfer the executable file to the target and start gdb
	  -d | --dest            	The destination folder on target where the file will be transferred
	  -P | --PID             	The PID on target to be attached
	  -i | --target_ip       	The target IP address. Defaults to 127.0.0.1
	  -p | --ssh_port        	SSH port to connect to QEMU. Defaults to 1234
	  -t | --gdb_port        	The port for remote debugging. Defaults to 3333
	  -s | --server          	Start gdbserver on target
	  -g | --gdb             	Start gdb on development machine
	  -h | --help            	Display this help


- Start gdbserver

.. code-block:: bash

    ./gdb_helper --server

It will start gdbserver on target to listen connection from port 3333, which is exposed previously

.. code-block:: bash

    ./gdb_helper --gdb

- Start gdb and connect to target


If the executable program is not deployed to target yet, the script can be used
to transfer the file to destination folder on target

.. code-block:: bash

    ./gdb_helper --file exe_file --dest DEST
