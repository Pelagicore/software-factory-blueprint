:orphan:

.. _running-qemu-tests:

Running tests on QEMU
=====================

To enable the tests to run on QEMU, the local.conf file of the QEMU variant must inherit the following classes,

.. code-block:: bash

	# Enable testing
	INHERIT += " \
	    testimage \
	    testexport \
	"

An ordered list of the tests to run must be appended in local.conf. These can be core tests provided by yocto like
ping, ssh, scp etc. or your own tests. The tests can be added as follows,

.. code-block:: bash

	# All test suites to run
	TEST_SUITES = " \
	    ping \
	    ssh \
	    scp \
	    mytest \
	"

To run tests on QEMU target, proceed as follows,

.. code-block:: bash

	# Bitbake core-image-pelux-minimal-dev for qemu-x86-64_nogfx target
	TEMPLATECONF=`pwd`/sources/meta-pelux/conf/variant/qemu-x86-64_nogfx source sources/poky/oe-init-build-env build
	bitbake core-image-pelux-minimal-dev

	# Make sure we have the required utilities
	bitbake qemu-helper-native

	# Set up networking for qemu
	sudo ../sources/poky/scripts/runqemu-gen-tapdevs 1000 1000 4 tmp/sysroots-components/x86_64/qemu-helper-native/usr/bin

	# Give qemu permissions to access tun interfaces
	sudo setcap cap_net_admin+ep $(find tmp/work/ -name qemu-system-x86_64 | grep qemu-helper-native)

	# Run tests
	bitbake core-image-pelux-minimal-dev -c testimage

.. tags:: howto
