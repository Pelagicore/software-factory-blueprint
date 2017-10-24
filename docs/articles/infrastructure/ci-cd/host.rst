:orphan:

Infrastructure host
===================

Because we run all the parts of the infrastructure like code hosting, cache, documentation, on different software and probably in docker containers there needs to be one host server which will work as a proxy server to give easy access to all the applications in the infrastructure in a easy way. It might also be responsible to serve static files like documentation and cache.

Host Nginx configuration
------------------------

This is a example Nginx configuration which can be reused to set up a proxy server host:

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

            location / {
                root   /var/www/pelux.io;
                index  index.html index.htm;
            }

            location /yocto-cache/ {
                alias     /var/www/yocto-cache/archive/;
                index     index.html index.htm;
                autoindex on;
            }

            location /software-factory/ {
                alias /var/www/software-factory/
                index index.html index.htm
            }

            error_page   500 502 503 504  /50x.html;
            location = /50x.html {
                root   /usr/share/nginx/html;
            }

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
        }
    }

The Jenkins jobs later need to be directed to write the yocto-cache and other artifacts to ``/var/www/`` so that this Nginx instance will be able to serve them via http(s).
