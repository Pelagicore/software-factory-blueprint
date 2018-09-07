:orphan:

.. _arch-vertical-configurations:

Vertical configurations
***********************

Each vertical configuration describes a sub-system of the product.

Update management
=================

The software update components are responsible for platform level software
update. This sub-system is critical in an automotive context since it allows to
deploy new functionalities, fix important bugs and security issues or update
assets such as driving data. A well designed update sub-system can save a lot
of money to car manufacturers by avoiding products recalls and to end-users by
not having to go to a mechanic to fix software problems.

Use cases
---------

A platform developer should be able to deploy :term:`rootfs`, :term:`kernel`,
:term:`bootloader`, :term:`ECU`'s flash memory, configuration and/or system
design modifications to a fleet of devices currently running the platform.

End-users should be able to apply those modifications using their Internet
connectivity: for example with LTE or WiFi, using Over The Air (OTA)
mechanisms. They (or their mechanics) should also have the possibility to
install updates from physical devices such as USB keys or SD cards.

Requirements
------------

In order to meet safety concerns, an update mechanism has to be fault
resilient. For instance, if a power failure happens during an update, the
system should not end up in an inconsistent state. This requirement implies that
updates have to be atomic/transactional. (i.e: never partially applied)

In order to modify the rootfs without affecting the system execution, the
update solution can proceed with one of those two mechanisms:

 - A/B symmetric partitioning where two different versions of the system are
   deployed on two distinct partitions (that could even be located on two
   different memory chips). This has the benefit of always having one working
   partition. When the partition A is upgrading, it modifies the partition B
   and, when done, switches the default bootloader entry to B. This solution
   only requires a downtime when rebooting, however it is expensive both in
   terms of components and disk space.

 - Normal+recovery asymmetric partitioning where a large partition includes the
   normal system and a secondary small partition can boot into a minimal
   working system able to update the main partition. This solution is cheaper
   but introduces a longer downtime than a symmetric partitioning.

 - In-place upgrading where a single partition is capable of modifying itself in
   an atomic way. This is notably used by OSTree. This requires less space than
   the previous methods and a short downtime.

If an update introduces regressions, the system should be able to revert
automatically to a previous working state. This can be achieved using different
mechanisms. Typical solutions include:

 - With A/B symmetric partitioning, if one partition fails booting, the
   bootloader can detect the error and boot the other partition.

 - With a normal+recovery partitioning, if an error is detected, the bootloader
   can reboot into recovery mode and fix the problem.

 - With an in-place upgrading solution, specifically OSTree, different boot
   entries can deploy different versions of the rootfs.

The above requirement underlines the fact that an update mechanism can
sometimes constrain the design of the rest of the system. An ideal update
solution should make few assumptions on the rest of the system's architecture.
(for instance: bootloader dependencies, number of partitions, read-only or
read-write partitions etc...) This would limit the complexity of integration of
the solution. Some update solutions also support several update mechanism
schemes and give more flexibility to the platform developer.

An update mechanism should limit the resources (i.e: Disk space, RAM usage,
Bandwidth consumption etc...) usage on end-devices but also on the update
servers. Typical solutions are:

 - Differential updates: avoid too large downloads and processing. However,
   this can cause problems if a local data block is corrupted.

 - Full downloads: alternatively, downloading complete images solves the issue
   of local corrupted data but is much more resource intensive.

On a different side, updates can also be file or block based which affect the
portability of update data across devices and also the size of downloaded
information.

An OTA server should propose various fleet and deployment management scenarios.
For example, a car manufacturer should be able to deploy updates on a certain
range of devices. (for example by car models and/or geographically and/or
following a schedule)

An update mechanism has to guarantee fundamental security capabilities. The two
mainly expected features are:

 - Integrity: this guarantees that data haven't been modified from the server
   to the client. (for example, by man-in-the-middle attacks)

 - Authentication: this guarantees that update have been created by an
   authorized entity. (for example, by a Tier-1 or OEM vendor) This can be
   achieved using digital signatures, CMAC or HMAC.

In order to implement those checks correctly, it would be interesting to rely
on a deep root of trust with :term:`TPM` or :term:`TEE`.

An automotive update mechanism should strive to minimize downtimes when
updating and should not run while the car is driving.

An update solution should easily be integrated to a given Graphical User
Interface. This can be achieved with APIs such as D-Bus interfaces or C++
libraries.

A plus for an update solution in the context of an automotive Linux platform
would also be to have an integration with Yocto.
