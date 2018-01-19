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

QEMU emulator can be launched with a serial console support using the
following command: 

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
      --append "vga=0 uvesafb.mode_option=1280×720-32 root=/dev/hda console=ttyS0 rw mem=512M oprofile.timer=1 " -serial stdio


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

The machine can be accessed via SSH for development purposes using the
following command:

.. code-block:: bash

    $ ssh root@127.0.0.1 -p 1234

.. [#kvm] https://en.wikipedia.org/wiki/Kernel-based_Virtual_Machine
.. [#qemu_kvm_feature] https://wiki.qemu.org/Features/KVM

.. tags:: howto, experimental
