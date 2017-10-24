:orphan:

Writing the image
=================

This section describes how to write the build output, a ready disk-image, to a removable media.
Further information can be found in the `Poky documentation`_.

General instructions
--------------------
Use the ``dd`` utility to write the image to the raw block device. For example:

.. code-block:: bash

    dd if=<image-name> of=<host-device> bs=4M

.. note:: The <image-name> depends on your arch and image recipe name. You can find all images in ``tmp/deploy/images/<arch>/`` in your build directory.

.. note:: The ``<host-device>`` is the SD-card or other removable media device on the host, e.g.  ``/dev/mmcblk0`` or ``/dev/sdc``. More information on how to discover the SD-card or other media device can be found in the `following documentation`_.

.. _Poky documentation: http://git.yoctoproject.org/cgit.cgi/poky/tree/README.hardware
.. _following documentation: https://www.raspberrypi.org/documentation/installation/installing-images/linux.md

