:orphan:

How to cross compile using Qt Creator and PELUX SDE
===================================================
.. taglist:: howto

Prerequisites:
--------------
#. Hardware target is running PELUX
#. Hardware target has an sftp server installed

Steps
-----
#. Start PELUX SDE
#. Start Qt Creator
#. Open up tools->build & run->kits and verify that the PELUX SDE installed a
   kit successfully
#. Under devices, create a Generic Linux Device with the IP Address and login to
   your hardware target
#. Open any Qt/C++ application that you want to run on the hardware target.
#. Under project->run settings add all arguments required to run
   the application. Do not forget `--platform` if the application is graphical.
#. Click build. This will cross compile the application using the PELUX SDK.
#. Click run. This will copy and run the compiled application to the hardware
   target using sftp.
#. The compiled application should now run on your target.

.. note:: This may require that any previously running graphical
   applications are shutdown before hand.

