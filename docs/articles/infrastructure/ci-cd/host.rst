:orphan:

Infrastructure host
===================

Because we run all the parts of the infrastructure like code hosting, cache,
documentation, on different software and probably in docker containers there
needs to be one host server which will work as a proxy server to give easy
access to all the applications in the infrastructure in a easy way. It might
also be responsible to serve static files like documentation and cache.

Host nginx configuration
------------------------

This is a example nginx configuration which can be reused to set up a proxy server host:

.. code-block:: none

    worker_processes  1;

    events {
        worker_connections  1024;
    }

    http {

        include            mime.types;
        default_type       application/octet-stream;
        sendfile           on;
        keepalive_timeout  65;
        gzip               on;

        server {
            listen       80;
            server_name  localhost pelux.io;

            # Just the general site
            location / {
                root   /var/www/pelux.io;
                index  index.html index.htm;
            }

            # When using yocto-cache over www
            location /yocto-cache/ {
                alias     /var/www/yocto-cache/archive/;
                index     index.html index.htm;
                autoindex on;
            }

            # Documentation
            location /software-factory/ {
                alias /var/www/software-factory/
                index index.html index.htm
            }

            error_page   500 502 503 504  /50x.html;
            location = /50x.html {
                root   /usr/share/nginx/html;
            }
        }
    }

The Jenkins jobs later need to be directed to write the yocto-cache and other
artifacts to ``/var/www/`` so that this Nginx instance will be able to serve
them via http(s).

Host docker configuration
-------------------------
Make sure to create a docker config file to make sure the file systems are large
enough and work as intended. Make sure ``/etc/docker/daemon.json`` contains at
least the following.

.. code-block:: json

    {
      "storage-driver": "overlay2"
    }
