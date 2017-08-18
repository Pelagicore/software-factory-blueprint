Build Slaves
============

Running a public slave
----------------------

In order to run a slave which the master can reach via SSH you still need to prepare some things:

.. code-block:: bash

   # Install prerequesits
   sudo apt install openjdk-8-jdk-headless docker.io vagrant

   # create a jenkins user and add it to the docker group so
   # it can run docker without becoming root
   sudo useradd jenkins
   sudo usermod -aG docker jenkins

Running a private slave
-----------------------

Sometimes it's necessary to run slaves from a private network. Then you need to run a java program which will connect to the master instead the master connecting to the slave. To do so, set up a new slave in Jenkins.

Prerequisites
_____________

You need to have the same Java version running on the slave as your Jenkins master runs. Nowadays the docker LTS version runs Java 8.

Best practice is also to create a unix user the slave will run with on your machine, you can call the user jenkins. If you will run Docker, make sure this user is in the ``docker`` group.

How to setup and install
________________________

Replace <URL> in the file with the real URL to the Jenkins server.

.. code-block:: none

   [Unit]
   Description=Jenkins slave for pelux.io
   
   [Service]
   User=%i
   Restart=always
   ExecStart=/usr/bin/java -jar /home/%i/slave.jar -jnlpUrl <URL>/slave-agent.jnlp -secret <SECRET>
   
   [Install]
   WantedBy=multi-user.target

1. Go to Jenkins -> Manage Jenkins -> Nodes -> New Node
2. Add the node name and set "Permanent Agent"
3. Put in the name and the remote root directory, you should have a special user like ``jenkins`` to run it so set ``/home/jenkins/``
4. Set the lables which this slave can run, for example ``DockerCI``
5. Have the Launch method set to Launch agent via Java Web Start
6. Save
7. Click on that slave in the list to get to the online/offline view of it
8. Copy the command line shown there and put it into the ``jenkins.slave.service`` file
9. Download the linked ``slave.jar`` and put it into the home directory of the jenkins user so that the service can find it
10. Copy the changed ``jenkins.slave@.service`` to ``/lib/systemd/system/``
11. Enable and start the service: ``sudo systemctl enable jenkins.slave@jenkins && sudo systemctl start jenkins.slave@jenkins``
12. Check if the slave connected without problems ``sudo journalctl -b -u jenkins.slave@jenkins``
