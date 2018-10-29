:orphan:

Reading System Logs with DLT
============================

Introduction
------------

PELUX uses a component from GENIVI called `DLT`_ (for Diagnostic Log and Trace)
which enables distant computers to access the system logs of a machine running
PELUX.

DLT is split into two parts:

- **dlt-daemon**: running on PELUX, collecting logs and distributing them on
  a network
- **dlt-viewer**: running on a developer machine, accessing distant logs from
  dlt-daemon

Compiling dlt-viewer
--------------------

Since dlt-daemon is already present on PELUX, you only need to compile
dlt-viewer on your development machine. For that, you need to have installed:
- `git`
- `cmake`
- the Qt SDK.

Clone the dlt-viewer repository:

.. code-block:: bash

    git clone https://github.com/GENIVI/dlt-viewer

Compile it with cmake:

.. code-block:: bash

    cmake -H. -Bbuild
    cmake --build build

Running dlt-viewer
--------------------

You can now run dlt-viewer from its build directory

 .. code-block:: bash

    build/bin/dlt-viewer
 
Configuring dlt-viewer for your target
--------------------------------------

dlt-viewer must be configured to point to your PELUX machine. You can do that
from "*Config -> ECU Add*". On the first tab, named "ECU", feel free to use an
Id and Description that describe your target but make sure the "Interface Type"
is set to TCP.  On the second tab, named "IP", use the IP address of your
target and and make sure the port is set to 3490. You can then hit the "OK"
button and your machine should appear in the "Project" part of the main window.

.. note:: If you do not know the IP address of your target, the `Raspberry Pi
          documentation`_ describes how to find a new device on the network.
          This can be used for any target, not just Raspberry Pi

Select your target in the dlt-viewer's main window and connect to it using
"*Config -> ECU Connect*". You should now have DLT logs shown on the right pane
of dlt-viewer. Be careful though that the actual payload of those logs might
be out of your screen, far at the right of the screen.

Going further
-------------

Filtering
^^^^^^^^^

System logs are usually long and tedious to read. Fortunately, dlt-viewer comes
with a filtering capability that can search patterns in logs.

You can use the line edit in the top action bar to search for words such as
"*set_default*". You can also, enable regular expression search and filter with
requests such as "*set\_.*_trace_status*"

Logging data
^^^^^^^^^^^^

From a shell
""""""""""""

On PELUX, DLT comes with a couple of tools that make life easier. One of those
tools is called `dlt-adaptor-stdin`_ and it can be used to log data from the
command line. It reads strings from its standard input so you can use it with
UNIX pipes. For example:

 .. code-block:: bash

    echo "PELUX rocks!" | dlt-adaptor-stdin

Should append "*PELUX rocks!*" to the system logs you can read from dlt-viewer.

From a service
""""""""""""""

DLT provides a library to services so that they can log information. You can
get started with `a simple service example in the dlt-daemon repository`_.

For a detailed tutorial on how to get started, follow the `DLT cheatsheet`_.

.. _`DLT`: https://at.projects.genivi.org/wiki/display/PROJ/Diagnostic+Log+and+Trace
.. _`Raspberry Pi documentation`: https://www.raspberrypi.org/documentation/remote-access/ip-address.md
.. _`dlt-adaptor-stdin`: https://github.com/GENIVI/dlt-daemon/blob/master/src/adaptor/dlt-adaptor-stdin.c
.. _`a simple service example in the dlt-daemon repository`: https://github.com/GENIVI/dlt-daemon/tree/master/examples/example1
.. _`DLT cheatsheet`: https://at.projects.genivi.org/wiki/display/PROJ/DLT+cheatsheet
