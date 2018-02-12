:orphan:

.. _booting-a-qemu-image:

Booting up a QEMU image
=======================

Images for QEMU target can be booted up using KVM [#kvm]_ to utilize hardware
virtualization feature if found on the host system and run the virtual
machine in better performance.
See KVM feature for QEMU [#qemu_kvm_feature]_.

Installing KVM and its dependencies
-----------------------------------

On Debian-based systems, the following command can be used to install
the emulator tool and its dependencies:

.. code-block:: bash

    $ sudo apt-get install qemu-kvm libvirt-clients libvirt-daemon-system


Launching the virtual machine
-----------------------------
QEMU can be launched with different network backend configurations.


.. _boot-qemu-port-forward:

Port forwarding configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
QEMU emulator can be launched with serial console support and port forwarding
using the following command:

.. code-block:: bash

   sudo kvm -kernel tmp/deploy/images/qemux86-64/bzImage \
      -net nic \
      -net user,hostfwd=tcp::1234-:22 \
      -cpu Broadwell \
      -smp 4 \
      -hda tmp/deploy/images/qemux86-64/core-image-pelux-minimal-qemux86-64.ext4 \
      -vga qxl \
      -no-reboot \
      -soundhw ac97 \
      -m 512 \
      -append "vga=0 uvesafb.mode_option=1280×720-32 root=/dev/hda console=ttyS0 rw mem=512M oprofile.timer=1 " -serial stdio

Static IP address configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
A static IP address facilitates development of automation and testing scripts.
The next commands assume the QEMU target ip address is ``192.168.7.2`` and the
host machine address is ``192.168.7.1``.

1. Launch QEMU with static IP address and a tap device [#qemu_tap_network]_
using the following command:

.. code-block:: bash

   sudo kvm -kernel tmp/deploy/images/qemux86-64/bzImage \
      -device virtio-net-pci,netdev=net0,mac=52:54:00:12:34:02 -netdev tap,id=net0,ifname=tap0,script=no,downscript=no \
      -cpu Broadwell \
      -smp 4 \
      -hda tmp/deploy/images/qemux86-64/core-image-pelux-minimal-qemux86-64.ext4 \
      -vga qxl \
      -no-reboot \
      -soundhw ac97 \
      -m 512 \
      -append "vga=0 uvesafb.mode_option=1280×720-32 root=/dev/hda console=ttyS0 rw mem=512M oprofile.timer=1 ip=192.168.7.2::192.168.7.1:255.255.255.0" -serial stdio

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
