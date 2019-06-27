:orphan:

Deploying the image
===================

This section describes how to deploy the build output, a ready disk-image, to a removable media.
Further information can be found in the `Poky documentation`_.

Bmap-tools
----------

Bmap prerequisites
^^^^^^^^^^^^^^^^^^
You will need to install the bmap tools.

.. code-block:: bash

    sudo apt-get install bmap-tools

Using bmap-tools
^^^^^^^^^^^^^^^^
Use bmap-tools to write an Intel image to a disk more than twice faster than ``dd``. Bmap-tools, supports flashing of compressed images too.

You will need two files, both of them will be found on
``/tmp/deploy/images/<architecture>/``.

The compressed image name and bmap file will have these suffixes:

- <image>.rootfs.wic.bz2
- <image>.rootfs.wic.bmap 

To flash the image, run:

.. code-block:: bash

    sudo bmaptool copy <compressed-image-name> --bmap <bmap-filename> <host-device>

.. note:: In case bmap gives the error "[Errno 16] Device or resource
          busy", make sure the disk partitions are unmounted. 




General instructions
--------------------
Use the ``dd`` utility to write the image to the raw block device. For example:

.. code-block:: bash

    dd if=<image-name> of=<host-device> bs=4M
    sync

.. note:: The <image-name> depends on your arch and image recipe name. You can
          find all images in ``tmp/deploy/images/<arch>/`` in your build directory.

.. note:: The ``<host-device>`` is the SD-card or other removable media device
          on the host, e.g.  ``/dev/mmcblk0`` or ``/dev/sdc``. More information
          on how to discover the SD-card or other media device can be found in
          the `following documentation`_.

.. _Poky documentation: http://git.yoctoproject.org/cgit.cgi/poky/tree/README.hardware
.. _following documentation: https://www.raspberrypi.org/documentation/installation/installing-images/linux.md

