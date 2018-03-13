:orphan:

.. _booting-a-qemu-image:

Booting up a QEMU image
=======================

Images for QEMU target can be booted up using KVM [#kvm]_ to utilize hardware
virtualization feature if found on the host system and run the virtual
machine in better performance.
See KVM feature for QEMU [#qemu_kvm_feature]_.

QEMU launch script
------------------

There is a QEMU launch script called ``qemu_launcher``, which is shipped with SDK and also available from yocto builds.

.. code-block:: bash

	$ ./qemu_launcher -h
	usage: ./qemu_launcher [options]
	[options] is any of the following:
        -f | --folder        Specify a source folder of the QEMU image
                             Defaults to tmp/deploy/images/qemux86-64
        -i | --hda           Specify rootfs file. Defaults to core-image-pelux-minimal-qemux86-64.ext4
        -p | --ssh_port      SSH port to connet to QEMU. Defaults to 1234
        -n | --smp           Number of cpu cores. Defaults to 4
        -k | --kernel_path   By default, kernel_path is the same as folder, but can be overwritten by using this option
        -c | --cmdline       Specify kernel command line. This would allow power users to change vga or root, etc.
                             Defaults to "vga=0 uvesafb.mode_option=1280×720-32 root=/dev/hda console=ttyS0 rw oprofile.timer=1"
        -m | --mem           Maximum amount of guest memory (Size is in megabytes)
                             Defaults to 512
        -t | --gdb_port      The port is forwarded so that gdbserver can listen on it
                             Then gdb can be run from develop machine to connect to the port for remote debugging
                             Defaults to 3333
        -d | --dev           Run QEMU development image instead of normal image
                             Defaults to core-image-pelux-minimal-dev-qemux86-64.ext4
        -s | --static        The switch to toggle running QEMU dev image with static IP (Defaults to false)
        -I | --target_ip     Specify the target static IP, must be 192.168.7.x (Defaults to 192.168.7.2)
                             Please aware that to change the default static IP, it is also needed to update the
                             STATIC_IP_ADDRESS in local.conf in meta layer and rebuild the image
        -g | --server_ip     Specify the gateway server IP, must be 192.168.7.x (Defaults to 192.168.7.1)
        -l | --list          List all available images from the default folder or folder user specified
        -h | --help          Display this help



Launching the virtual machine
-----------------------------
QEMU can be launched with different network backend configurations.


.. _boot-qemu-port-forward:

Port forwarding configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
QEMU emulator can be launched with serial console support and port forwarding
using the following command:

.. code-block:: bash

   ./qemu_launcher -f FOLDER -i core-image-pelux-minimal-qemux86-64.ext4

The above command will load kernel and the image ``core-image-pelux-minimal-qemux86-64.ext4`` from ``FOLDER``


Static IP address configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
A static IP address facilitates development of automation and testing scripts.
The next commands assume the QEMU target ip address is ``192.168.7.2`` and the
host machine address is ``192.168.7.1``.

1. Launch QEMU with static IP address and a tap device [#qemu_tap_network]_
using the following command:

.. code-block:: bash

   ./qemu_launcher -f FOLDER -i core-image-pelux-minimal-qemux86-64.ext4 -s

The above script will launch QEMU with a tap device ``tap0`` on the host machine
where guest networking can be routed through the tap interface.
To achieve that run the following command inside the guest machine console:

.. code-block:: bash

   route add default gw 192.168.7.1


2. Configure the ``tap0`` interface on host machine by executing the following
commands on the host machine:

.. code-block:: bash

   sudo ip address add 192.168.7.1/24 broadcast 192.168.7.255 dev tap0
   sudo ip link set dev tap0 up
   

3. (Optional) Enable the tap device to access internet by running the following
commands on the host machine:

.. code-block:: bash

   sudo ip route add to 192.168.7.1 dev tap0
   sudo iptables -A POSTROUTING -t nat -j MASQUERADE -s 192.168.7.1/24
   sudo iptables -P FORWARD ACCEPT

Instead of using the default target IP ``192.168.7.2`` and the server address
``192.168.7.1``, it is possible to specify the target IP and server IP as shown below:

.. code-block:: bash

   ./qemu_launcher -f FOLDER -i core-image-pelux-minimal-qemux86-64.ext4 -s --target_ip 192.168.11.18 --server_ip 192.168.11.1

Please aware that to make the new static IP work, it is also needed to update
``STATIC_IP_ADDRESS`` in ``local.conf`` in meta layer and rebuild the image.


Supported emulated hardware configuration
-----------------------------------------

============  ==============  ===========
KVM option    Value           Description
============  ==============  ===========
``-cpu``      Broadwell       Chipset
``-smp``      4               Number of cpu cores
``-m``        512M            Maximum amount of guest memory
``-vga``      qxl             QXL video graphics output
``-soundhw``  ac97            AC'97 audio audio codec
============  ==============  ===========

.. note:: The ``hostfwd`` option specifies TCP port configuration for ssh usage.
.. note:: If you build another image than ``core-image-pelux-minimal``, adapt the path passed to ``-hda`` accordingly.

Connecting to the virtual machine using SSH
-------------------------------------------

The machine can be accessed via SSH for development purposes.

SSH access via Port forwarding
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Boot the QEMU machine with port forwarding configuration
:ref:`boot-qemu-port-forward`, where QEMU target port ``22`` for the
its ``localhost`` interface is mapped to host machine port
``1234`` for its ``localhost`` interface.
Then Run the ``ssh`` command on host machine.

.. code-block:: bash

    $ ssh root@127.0.0.1 -p 1234


SSH access via static ip
^^^^^^^^^^^^^^^^^^^^^^^^
Boot the QEMU machine with static ip configuration, and then run the following
command on host machine.

.. code-block:: bash

    $ ssh root@192.168.7.2 -p 22


.. [#kvm] https://en.wikipedia.org/wiki/Kernel-based_Virtual_Machine
.. [#qemu_kvm_feature] https://wiki.qemu.org/Features/KVM
.. [#qemu_tap_network] https://wiki.qemu.org/Documentation/Networking#Tap
.. tags:: howto, experimental
