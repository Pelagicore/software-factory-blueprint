:orphan:

Build Slaves
============

Running a public slave
----------------------

In order to run a slave which the master can reach via SSH you still need to
prepare some things. 

First install docker from `dockers own repositories`_. (The package in Ubuntu,
for example, is old and outdated):

.. _dockers own repositories: https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu/

Now install the other dependencies through apt and setup the jenkins user.

.. code-block:: bash

   # Instructions for Ubuntu
   # Install prerequisites
   sudo apt install openjdk-8-jdk-headless vagrant

   # create a jenkins user and add it to the docker group so
   # it can run docker without becoming root
   sudo useradd -m jenkins
   sudo usermod -aG docker jenkins

   # Configure docker to use overlay2 as storage driver
   sudo sh -c 'echo "{ \"storage-driver\": \"overlay2\" }" > /etc/docker/daemon.json'

There is currently a bug in the kernel of Ubuntu 16.04 which under certain
circumstances causes ``tar -x`` to fail on overlayfs with something like:

.. code-block:: none

  tar: ./deps/0/bin: Directory renamed before its status could be extracted

This can affect yocto builds inside of Vagrant. More information is available
in `the bug report`_. In short, this bug was fixed in the linux package for
Xenial (16.04) as of version 4.4.0-103.126. Install the patched kernel:

.. code-block:: bash

  # Installed the latest kernel patches for 16.04
  sudo apt-get install linux-generic

  # Reboot to use the updated kernel
  sudo reboot

.. _the bug report: https://bugs.launchpad.net/ubuntu/+source/linux/+bug/1728489

Connecting to the slave using SSH
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Generating SSH key pairs
""""""""""""""""""""""""

A private and public SSH key pair must be generated. The Jenkins master server will connect to the Jenkins build slaves using SSH. The Jenkins master server will have the SSH *private* key, in order to initiate the SSH connection, and the Jenkins build slaves will have *public* keys added to their respective ``jenkins`` users.

Generate one key pair per build slave using the following command:

.. code-block:: bash
    
    # Execute on the build slave
    sudo su jenkins
    cd $HOME
    mkdir .ssh && chmod 700 .ssh & cd .ssh
    ssh-keygen -t rsa -f build_slave_key
    cat build_slave_key.pub >> authorized_keys

Save the private key. It will be used when configuring Jenkins.

Configuring Jenkins
"""""""""""""""""""

1. Go to Jenkins -> Manage Jenkins -> Nodes -> New Node
2. Add the node name and set "Permanent Agent"
3. Put in the name and the remote root directory, you should have a special user like ``jenkins`` to run it so set ``/home/jenkins/``
4. Set the labels which this slave can run, for example ``DockerCI``
5. Have the Launch method set to "Launch slave agents via SSH"
6. Enter the address to the slave in the "Host" field
7. If you already have the credentials added for this slave, select them in the "Credentials" field, and skip steps 7a-7f. If not, press the "Add" button in the "Credentials" field, and follow steps 7a-7f.

    * 7a. Set "Domain" to "Global credentials (unrestricted)"
    * 7b. Set "Kind" to "SSH username with private key"
    * 7c. Set "Username" to "jenkins" (assuming that you use this UNIX username for your jenkins user)
    * 7d. Set "Private Key" to "Enter Directly", and supply the *private* key you generated previously
    * 7e. Set "Passphrase" as needed, or leave empty if no passphrase is set
    * 7f. Set "Description" to a suitable description

8. Select the correct key in "Credentials"
9. Set "Host Key Verification Strategy" to "Non verifying Verification Strategy"
10. Set "Availability" to "Keep this agent online as much as possible"
11. Press "Save"

You may verify the status of the build slave under the status page of the build slave.


Running a private slave
-----------------------

Sometimes it's necessary to run slaves from a private network. Then you need to run a java program which will connect to the master instead the master connecting to the slave. To do so, set up a new slave in Jenkins.

Prerequisites
^^^^^^^^^^^^^

You need to have the same Java version running on the slave as your Jenkins master runs. Nowadays the docker LTS version runs Java 8.

Best practice is also to create a UNIX user the slave will run with on your machine, you can call the user jenkins. If you will run Docker, make sure this user is in the ``docker`` group.

How to setup and install
^^^^^^^^^^^^^^^^^^^^^^^^

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
4. Set the labels which this slave can run, for example ``DockerCI``
5. Have the Launch method set to Launch agent via Java Web Start
6. Save
7. Click on that slave in the list to get to the online/offline view of it
8. Copy the command line shown there and put it into the ``jenkins.slave.service`` file
9. Download the linked ``slave.jar`` and put it into the home directory of the jenkins user so that the service can find it
10. Copy the changed ``jenkins.slave@.service`` to ``/lib/systemd/system/``
11. Enable and start the service: ``sudo systemctl enable jenkins.slave@jenkins && sudo systemctl start jenkins.slave@jenkins``
12. Check if the slave connected without problems ``sudo journalctl -b -u jenkins.slave@jenkins``
