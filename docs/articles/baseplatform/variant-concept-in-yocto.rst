:orphan:

Variant concept in Yocto
========================

A Yocto project often has to support several variations in software and
hardware composition, such as supporting a graphical software stack as well as
a non-graphical software stack on several different CPU architectures.

A variation in either hardware of software is in the Software Factory referred
to as a *variant*.

Each variant potentially needs its own set of Yocto configuration files (most
notably, its own ``bblayers.conf`` and ``local.conf``). Yocto has a built-in
way to handle deployment of configuration files with its ``TEMPLATECONF``
variable which can be supplied to the ``oe-init-build-env`` script
[#templateconf]_, and this scheme is also used in the Software Factory.

.. _recommended-variant-management:

Recommended variant management
------------------------------

The recommended way to handle variants is to keep one directory per variant in
your layer. The variant directories should go into
``<meta-yourlayer>/conf/variant/<variant name>``. Each variant should supply a
``README``, ``bblayers.conf.sample`` and ``local.conf.sample``.

* ``README`` contains a short description of the variant, such as the hardware
  it supports and the software variation it supports. For instance, if this
  variant only supports a non-graphical system on a Raspberry Pi 3, this is
  where this should be noted.
* ``bblayers.conf.sample`` contains the sample ``bblayers.conf`` which will be
  copied into the users' ``build/conf`` directory when initializing a new
  build. This ``bblayers.sonf.sample`` is specific to the current variant, and
  should be written to include the layers needed to build the current variant.
* ``local.conf.sample`` is also specific to the current variant in the same way
  as ``bblayers.conf.sample``, but should contain the ``local.conf`` needed for
  the current variant.

If many variants are using the same directives, it is recommended to have a
``common`` directory with these directives in. The files that contain those
common directives can then be included by the more specific variants that add
the specific settings.

.. note:: BitBake searches paths that are listed in the ``BBPATH`` variable, so
          before including any files in ``bblayers.conf`` or ``local.conf``, one
          has to make sure that those files can be found by setting ``BBPATH``
          to include the layer in which they are located.

Recommended usage of variants
-----------------------------

A variant is selected using the ``TEMPLATECONF`` variable when issuing the
``oe-init-build-env`` script from the ``poky`` project. The scheme described in
:ref:`recommended-variant-management` is fully compatible with the
``oe-init-build-env`` script, all the user needs to do is to specify the full
path to the desired variant directory when running the script. More information
on the ``TEMPLATECONF`` variable is available in [#templateconf]_.

.. [#templateconf] http://www.yoctoproject.org/docs/latest/dev-manual/dev-manual.html#creating-a-custom-template-configuration-directory
