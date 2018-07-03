:orphan:

Configuring QtCreator to use the SDK
====================================

After :ref:`the installation of the SDK <installing-sdk>` and :ref:`the sourcing of
its environment <sourcing-the-environment>`, there are a couple of steps needed to
integrate the QtCreator IDE with the SDK. This document will guide you with the
configuration of QtCreator for a remote target using a different architecture than
your development machine and also help you getting started with the compilation and
remote execution of a simple service.

.. warning::

    All of the commands in this page (including QtCreator) shall be ran in a shell
    with :ref:`the SDK environment sourced <sourcing-the-environment>`. It is then
    advised to keep a terminal window open with the environment set up all along
    this tutorial. We will refer to this terminal as "an SDK terminal".

Opening QtCreator
-----------------

Always start QtCreator from a shell with the environment of the SDK using:

.. code-block:: bash

    $ qtcreator

Configuring a target (only done once)
-------------------------------------

QtCreator can automatically deploy and run services onto your PELUX target using sftp.
In order to do that, you first need to create a device configuration.

* Open the ``Tools->Options`` window and go to the ``Devices`` tab
* Click the ``Add`` button on the right side of the window
* Choose ``Generic Linux Device`` in the window that opens and click ``Start Wizard``
* Choose a ``name to identify this configuration`` such as "``PELUX Raspberry Pi``" for
  instance
* Enter the IP address of your PELUX machine in the next field
* Use ``root`` as username
* Choose Password authentication
* Let the password field empty
* You should not need to touch the private key path

After having filled in this pane, click ``Next >`` and ``Finish``. QtCreator will try
to connect over SSH to your PELUX machine. If your machine is reachable, that test should
show the version of the kernel you are using on PELUX.

Adding a new kit (only done once)
---------------------------------

QtCreator can use a cross-compilation toolchain like the one provided in the PELUX SDK to
compile software for an architecture different from the one it is running on. Configuring
the entire toolchain takes a bit of time but only has to be done once.

* Open the ``Tools->Options`` window and go to the ``Build & Run`` tab

Compilers
^^^^^^^^^

.. image:: screenshots/add_gcc.png

* Select the ``Compilers`` tab
* Click the ``Add`` button on the right and go to *GCC -> C*
    * In the bottom part of the window, name your C Compiler with something like *GCC
      PELUX Raspberry Pi*
    * For the path of the compiler, use the results of the ``which `echo ${CC} | awk
      '{print $1}'``` command ran in an SDK terminal
* Click the ``Add`` button and go to *GCC -> C++*
    * In the bottom part of the window, name your C++ Compiler with something like *G++
      PELUX Raspberry Pi*
    * For the path of the compiler, use the result of the ``which `echo ${CXX} | awk
      '{print $1}'``` command ran in an SDK terminal

Debugger
^^^^^^^^

.. image:: screenshots/sdk_gdb.png

* Select the ``Debuggers`` tab
* Click the ``Add`` button on the right
* In the bottom part of the window, name your Debugger with something like *GDB
  PELUX Raspberry Pi*
* For the path of the debugger, use the result of the ``which $GDB``` command ran in
  an SDK terminal

CMake
^^^^^

.. image:: screenshots/sdk_cmake.png

* Select the ``CMake`` tab
* Click the ``Add`` button on the right
* In the bottom part of the window, name your CMake with something like *CMake PELUX
  Raspberry Pi*
* For the path of the debugger, use the result of the ``which cmake``` command ran in
  an SDK terminal

Qt (optional)
^^^^^^^^^^^^^

This part can be skipped if you are not working with qmake or with a UI component.
However, if you want to be able to use Qt:

* Select the ``Qt Versions`` tab
* Click the ``Add...`` button on the right
* In the window that opens, select the qmake whose path is the result of the ``which
  qmake``` command ran in an SDK terminal
* In the bottom part of the window, name your Qt version with something like *Qt 5.10.1
  PELUX Raspberry Pi*

Kit
^^^

.. image:: screenshots/add_new_kit.png

* Select the ``Kits`` tab and click the ``Add`` button.
* Name your new kit with something like "PELUX Raspberry Pi"
* As ``Device type`` choose ``Generic Linux Device``
* As ``Device`` choose the target you defined earlier
* For ``Sysroot``, use the ``Browse...`` button and select the folder whose path is
  the result of the ``echo ${SDKTARGETSYSROOT}`` command ran in an SDK terminal
* Choose the previously defined PELUX C and C++ compilers from the corresponding combo boxes
* Change the environment of this kit to the result of the ``env`` command ran in an SDK terminal
    * If ``CC`` and ``CXX`` have default compiler flags, those should be added in ``CFLAGS`` and ``CXXFLAGS``
      To replace ``CFLAGS`` and ``CXXFLAGS``, use the result of the below command ran in
      an SDK terminal

      ``echo $CC | awk -v c="$CFLAGS" '{first = $1; $1 = ""; print "CFLAGS="$0, c;}'``
      ``echo $CXX | awk -v c="$CXXFLAGS" '{first = $1; $1 = ""; print "CXXFLAGS="$0, c;}'``
* Choose the previously defined debugger from the corresponding combo box
* Choose the previously defined CMake from the corresponding combo box
* Change the ``CMake Configuration`` to add a ``CMAKE_SYSROOT:STRING=<sysroot path>``
  line with ``<sysroot path>`` replaced by the actual sysroot path (result of ``echo
  ${SDKTARGETSYSROOT}``)

Click OK and you should now have your Kit ready for development!

How to open the template service project with QtCreator
-------------------------------------------------------

* Open QtCreator from an SDK terminal
* From the ``File`` menu choose ``New File or Project``

.. image:: screenshots/sdk_newprj.png

* Select ``Import Project`` from the ``Projects`` section
* Click ``Git Clone`` and then click the ``Choose`` button

.. image:: screenshots/sdk_gitclone.png

* In the window, which just opened, add the repository to the ``Repository section``.
  The git repo for the ``template-service`` is https://github.com/Pelagicore/template-service
* Select a proper path and add it to the ``Path`` section, then click ``Next``
* QtCreator will clone the project, then click ``Finish``
* Here you should select the kit to use to build project
* Select the kit you have already created in the previous step and click ``Configure``
* You can now compile and deploy to your target using the green arrow on the left of your screen


.. tags:: howto
