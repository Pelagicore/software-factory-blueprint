GPLv3 in automotive
-------------------

Car makers prioritize safety and security of vehicle software.
Car makers won't let users modify vehicle software because they carefully test
and certify their software and any change can compromise safety. GPLv3 software
explicitly states that users must be able to modify software, and installation
information provided even if that includes private encryption keys. Car makers
currently would rather prevent GPLv3 software from being introduced into their
systems than allow users to modify vehicle software.

Fortunately, Yocto provides a means to screen licenses based on different
parameters.

Screening GPLv3 licensed software in Yocto
------------------------------------------

1. Add layer **meta-gplv2**
2. Remove `initramfs-live-install` and `initramfs-module-install` from
   environment variable PACKAGE_INSTALL.
   *(file: core-image-minimal-initramfs.bbappend)*

   .. code-block:: bash

      PACKAGE_INSTALL_remove = "initramfs-live-install initramfs-module-install"
3. Remove `grub-efi` from WKS_FILE_DEPENDS_BOOTLOADERS for x86-64 arch.
   *(file: image_types_wic.bbclass)*

   .. code-block:: bash

     WKS_FILE_DEPENDS_BOOTLOADERS_remove_x86-64 = "grub-efi"
4. Remove `parted` from RDEPENDS_${PN}.
   *(file: initramfs-module-install-efi_1.0.bb)*

   .. code-block:: bash

     RDEPENDS_${PN}_remove = "parted"
5. Select `system-boot` as the bootloader instead of default `grub-efi`.
   *(file: systemd-boot.bbclass)*

   .. code-block:: bash

     EFI_PROVIDER = "systemd-boot"
6. Blacklist GPLv3 license 

   .. code-block:: bash

     INCOMPATIBLE_LICENSE = "\
        GPL-3.0 \
        LGPL-3.0 \
        AGPL-3.0 \
      "
7. Remove `cairo`

   .. code-block:: bash

    PACKAGECONFIG_remove = "cairo"

Impact of removing GPLv3 licensed software
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
SWUpdate feature for Raspberry Pi currently requires `partprobe`, a GPLv3 tool,
for re-partitioning. So as of now it will be non-functional with the removal of
`parted` package.

