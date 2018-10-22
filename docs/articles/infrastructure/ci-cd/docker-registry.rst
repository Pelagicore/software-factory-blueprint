:orphan:

.. _private-docker-registry:

Private Docker Registry
=======================

Sometimes it is of advantage to host a private docker registry to host docker
images which should be reused by the CI and/or developers in the project but
which one does not want to host on the public docker hub, because they might
contain proprietary code and binaries which should not be released to the
public.

There is documentation about the `deployment of a registry`_, here we document
the essence and some deviations to implement a registry which is read only for
non authenticated users but administrators are able to push changes to it.

Here is an example systemd service file which can be used to both set up and
start a docker container which has a preinstalled instance of a docker
registry.

.. code-block:: none
   :caption: docker.registry.service
   
   [Unit]
   Description=Docker Registry Container
   After=docker.service
   Requires=docker.service
   
   [Service]
   TimeoutStartSec=0
   Restart=always
   ExecStartPre=-/usr/bin/docker stop %n
   ExecStart=/usr/bin/docker run --rm --name %n \
             -e REGISTRY_HTTP_ADDR=0.0.0.0:80 \
             -p 8082:80 \
             -v docker_registry:/var/lib/registry \
             registry:2
   
   [Install]
   WantedBy=multi-user.target

The docker registry is run on port 80 inside of the docker container so that
users don't need to point to any special port, they would only use the domain,
image name and tag like ``example.com/ubuntu:16.04``.

This will save the content of the registry in a docker volume called
``docker_registry`` which can be easily back-upped.

Nginx configuration
-------------------

.. code-block:: none
   
   # This should go into the http {} part of the Nginx configuration
   ## Set a variable to help us decide if we need to add the
   ## 'Docker-Distribution-Api-Version' header.
   ## The registry always sets this header.
   ## In the case of nginx performing auth, the header is unset
   ## since nginx is auth-ing before proxying.
   map $upstream_http_docker_distribution_api_version $docker_distribution_api_version {
     '' 'registry/2.0';
   }


   # Docker Registry configuration according to
   # https://docs.docker.com/registry/recipes/nginx/
   # Using /v2/ 
   location ^~ /v2/ {

      proxy_pass http://127.0.0.1:8082/v2/;
      proxy_set_header X-Nginx-Proxy true;
      client_max_body_size 0; # disable any limits to avoid HTTP 413 for large image uploads

      # required to avoid HTTP 411: see Issue #1486 (https://github.com/moby/moby/issues/1486)
      chunked_transfer_encoding on;

      # Do not allow connections from docker 1.5 and earlier
      # docker pre-1.6.0 did not properly set the user agent on ping, catch
      # "Go *" user agents
      if ($http_user_agent ~ "^(docker\/1\.(3|4|5(?!\.[0-9]-dev))|Go ).*$" ) {
        return 404;
      }

      # To add basic authentication to v2 use auth_basic setting.
      limit_except GET HEAD {
        auth_basic "Registry realm";
        auth_basic_user_file /etc/nginx/conf.d/docker.registry.htpasswd;
      }


      ## If $docker_distribution_api_version is empty, the header is not added.
      ## See the map directive above where this variable is defined.
      add_header 'Docker-Distribution-Api-Version' $docker_distribution_api_version always;

      proxy_set_header  Host              $http_host;   # required for docker client's sake
      proxy_set_header  X-Real-IP         $remote_addr; # pass on real client's IP
      proxy_set_header  X-Forwarded-For   $proxy_add_x_forwarded_for;
      proxy_set_header  X-Forwarded-Proto $scheme;
      proxy_read_timeout                  900;
  }

Usage
-----

First, install docker according to the installation instructions for your
distribution. These instructions are available in the Docker website
[#dockerinstall]_.

.. code-block:: bash

   # Copy the Jenkins service file from the code block above into your
   # systemd service directory
   cp docker.registry.service /lib/systemd/system/

   # Make jenkins start up on boot and start it now too
   systemctl enable docker.registry.service
   systemctl start docker.registry.service

Starting it the first time can take a couple of minutes depending on your
internet connection because it then downloads the docker image and sets
everything up, so be patient.

Once it is started you should be able to access it via:

.. code-block:: none
                
   http://localhost:8082/v2/


After that you can also set up a nginx instance as a proxy so you don't
need the port number in the URL, but you don't need to do that on your
development machine.

In production you might want to add authentication for everything but GET and
HEAD requests. This ensures that only the administrators with a username and
password are able to update the repository, but a normal unauthenticated user
still is able to pull images from it. The example Nginx config above already
has this implemented. What you need to do is to create a ``.htaccess`` file by
running something like that:

.. code-block:: none
                
   docker run --rm --entrypoint htpasswd registry:2 \
                -Bbn testuser testpassword \
                > /etc/nginx/conf.d/docker.registry.htpasswd

The username and password should be different, and more users can be added to
that file too, or instead even LDAP or a different authentication method can
be used.

Pushing a custom image
----------------------

First a docker image needs to be build locally developer machine, then it
needs to be tagged with the domain, image name and tag like:
`example.com/ubuntu:16.04` only then it can be pushed into the registry. The
documentation should be consulted on how exactly to do that.

Special setup to run via HTTP
_____________________________

If the registry is run via HTTP instead of HTTPS, as described in
https://docs.docker.com/registry/insecure/ create `/etc/docker/daemon.json`
with this content and restart Docker on your developer machine or CI slave:

.. code-block:: json

   {
     "insecure-registries" : ["example.com"]
   }


.. _deployment of a registry: https://docs.docker.com/registry/deploying/
.. [#dockerinstall]  https://docs.docker.com/engine/installation/
