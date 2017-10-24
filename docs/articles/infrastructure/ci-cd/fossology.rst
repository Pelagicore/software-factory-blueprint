:orphan:

FOSSology
=========

FOSSology is a open source license compliance software system and toolkit.
As a toolkit you can run license, copyright and export control scans from
the command line. As a system, a database and web ui are provided to give
you a compliance workflow. License, copyright and export scanners are
tools available to help with your compliance activities.

This mini-tutorial explains how to use FOSSology together with PELUX.

systemd service
---------------

FOSSology comes with a Dockerfile allowing the containerized execution
both as single instance or in combination with an external PostgreSQL database.
Note: It is strongly recommended to use an external database for production
use, since the the standalone image does not take care of data persistency.

A pre-built Docker image is available from Docker Hub and can be run using following command:

.. code-block:: bash

   $ docker run -p 8081:80 fossology/fossology

Systemd service file running Docker container with FOSSology:

.. code-block:: bash

   [Unit]
   Description=Fossology Container
   After=docker.service
   Requires=docker.service
   
   [Service]
   TimeoutStartSec=0
   Restart=always
   ExecStartPre=-/usr/bin/docker stop %n
   ExecStartPre=-/usr/bin/docker rm %n
   ExecStart=/usr/bin/docker run -p 8081:80 fossology/fossology
   
   [Install]
   WantedBy=multi-user.target


Using FOSSology
---------------

Once Docker container up and running, it can be used using http://IP_ADDRESS:8081/repo

User 'fossy'
Password 'fossy'
