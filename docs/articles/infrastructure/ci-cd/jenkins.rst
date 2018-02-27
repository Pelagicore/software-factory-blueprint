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

nginx configuration
-------------------
.. code-block:: none

    # Nginx configuration specific to Jenkins
    # Note that regex takes precedence, so use of "^~" ensures earlier evaluation
    location ^~ /jenkins/ {

        # Convert inbound WAN requests for https://domain.tld/jenkins/ to
        # local network requests for http://127.0.0.1:8080/jenkins/
        proxy_pass http://127.0.0.1:8080/jenkins/;

        # Rewrite HTTPS requests from WAN to HTTP requests on LAN
        # proxy_redirect http:// https://;

        # The following settings from https://wiki.jenkins-ci.org/display/JENKINS/Running+Hudson+behind+Nginx
        sendfile off;

        proxy_set_header   Host             $host:$server_port;
        proxy_set_header   X-Real-IP        $remote_addr;
        proxy_set_header   X-Forwarded-For  $proxy_add_x_forwarded_for;
        proxy_max_temp_file_size 0;

        # this is the maximum upload size
        client_max_body_size       10m;
        client_body_buffer_size    128k;

        proxy_connect_timeout      90;
        proxy_send_timeout         90;
        proxy_read_timeout         90;

        proxy_buffer_size          4k;
        proxy_buffers              4 32k;
        proxy_busy_buffers_size    64k;
        proxy_temp_file_write_size 64k;

        # Required for new HTTP-based CLI
        proxy_http_version 1.1;
        proxy_request_buffering off;
    }


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

After that you can also set up a nginx instance as a proxy so you don't need the port number in the URL, but you don't need to do that on your development machine.

Plugins
-------

Normally we use the proposed plugins during installation and then add the following:

- Copy Artifact Plugin
- Build Monitor View

.. [#dockerinstall]  https://docs.docker.com/engine/installation/
