:orphan:

.. _measuring_startup_perf_with_systemd_analyze:

Measuring startup performance with systemd-analyze
==================================================

`systemd` provides a tool called `systemd-analyze` that can be used to retrieve statistics
and other state and tracing information from the system and service manager, and then build
an SVG plot showing units waiting for their dependencies.

You can see which unit files are causing your boot process to slow down. You can then optimize
your system accordingly.

Using systemd-analyze
---------------------

To retrieve statistics information from systemd, run:

.. code:: bash

    $ systemd-analyze

.. tip::
    If you boot via UEFI and use a boot loader which implements systemd's Boot Loader Interface
    (e.g GRUB that is used by PELUX on Intel and ARP platforms), systemd-analyze can additionally
    show you how much time was spent in the EFI firmware and the boot loader itself.

To list the started unit files, sorted by the time each of them took to start up:

.. code:: bash
    $ systemd-analyze blame

At some points of the boot process, things can not proceed until a given unit succeeds.
To see which units find themselves at these critical points in the startup chain, do:

.. code:: bash
    $ systemd-analyze critical-chain

To generate SVG file which describes the boot process graphically, run:

.. code:: bash
    $ systemd-analyze plot > plot.svg

Citations
---------
.. [#] https://wiki.archlinux.org/index.php/Improving_performance/Boot_process
.. [#] https://www.freedesktop.org/software/systemd/man/systemd-analyze.html
