:orphan:

Jenkins
=======

Jenkins is the build server which utilizes build slaves to build code and to archive the artifacts from those builds.

The Jenkins project offers preinstalled Docker images which can be used to vastly shorten the setup time of such a server. Here is an example systemd service file which can be used to both set up and start a docker container which has a preinstalled instance of Jenkins. It will save the configuration in a docker volume called ``jenkins_home``.

.. code-block:: none
   :caption: docker.jenkins.service
   
   [Unit]
   Description=Jenkins Container
   After=docker.service
   Requires=docker.service
   
   [Service]
   TimeoutStartSec=0
   Restart=always
   ExecStartPre=-/usr/bin/docker stop %n
   ExecStartPre=-/usr/bin/docker rm %n
   ExecStartPre=/usr/bin/docker pull jenkinsci/jenkins:lts
   ExecStart=/usr/bin/docker run --rm --name %n -p 8080:8080 --env JENKINS_OPTS="--prefix=/jenkins" --env JENKINS_JAVA_OPTIONS="-Djava.io.tmpdir=$JENKINS_HOME/tmp" -v jenkins_home:/var/jenkins_home -v /var/www/:/var/www/ jenkinsci/jenkins:lts
   
   [Install]
   WantedBy=multi-user.target

This runs Jenkins and mounts ``/var/www`` into the Jenkins container at the same place which makes it possible for Jenkins to store some artifacts in a place where a http server can reach them and serve them.
   
Usage
-----
First, install docker according to the installation instructions for your distribution. These instructions are available in the Docker website [#dockerinstall]_.

.. code-block:: bash

   # Copy the Jenkins service file from the code block above into your systemd service directory
   cp docker.jenkins.service /lib/systemd/system/

   # Make jenkins start up on boot and start it now too
   systemctl enable docker.jenkins.service
   systemctl start docker.jenkins.service

Starting it the first time can take a couple of minutes depending on your internet connection because it then downloads the docker image and sets everything up, so be patient.

Once it is started you need the admin password which you can find in the logs:

.. code-block:: none

   journalctl -b -u docker.jenkins
   ...
   Jul 03 12:37:22 vps429458 docker[9553]: Jenkins initial setup is required. An admin user has been created and a password generated.
   Jul 03 12:37:22 vps429458 docker[9553]: Please use the following password to proceed to installation:
   Jul 03 12:37:22 vps429458 docker[9553]: 932c528c68d14e24aab036f2021e2dee
   Jul 03 12:37:22 vps429458 docker[9553]: This may also be found at: /var/jenkins_home/secrets/initialAdminPassword

Then you can open this jenkins instance in your browser and put this password there so you can set everything up:

.. code-block:: none

   http://localhost:8080/jenkins/

After that you can also set up a Nginx instance as a proxy so you don't need the port number in the URL, but you don't need to do that on your development machine.

Plugins
-------

Normally we use the proposed plugins during installation and then add the following:

- Copy Artifact Plugin
- Build Monitor View

.. [#dockerinstall]  https://docs.docker.com/engine/installation/
