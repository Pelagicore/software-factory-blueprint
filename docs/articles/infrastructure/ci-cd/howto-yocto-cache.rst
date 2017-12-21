:orphan:

.. _setting-up-yocto-cache:

Setting up and using a Yocto cache
==================================

This chapter explains how to set up a cache for use with yocto. While building
an image, yocto caches everything it builds and downloads. This is useful since
it enables incremental builds where one only has to re-build what was changed
since last build, but also this makes it possible to share this cache between
builds. When used properly, the cache will dramatically improve build times,
usually up to 50% faster.

Specifically, we will be talking about the ``downloads`` directory and the
``sstate-cache`` directory in this chapter. The ``downloads`` directory contains
all downloaded packages, including those downloaded over SVN or git or similar,
and ``sstate-cache`` contains everything that was built, so basically binaries
plus some meta-data stating that it has actually been built and what version and
so on. One reason why the meta-data is useful is because otherwise the system
might try to reuse binaries for x86 when building for armv7, which wouldn't
work.

In general, when using a cached build in yocto, there are two options that needs
to be set: ``SOURCE_MIRROR_URL`` and ``SSTATE_MIRRORS``. The first one points to
where source packages can be found, the second points to the cached binary
builds.

.. code-block: bash
    :caption: site.conf

    INHERIT += "own-mirrors"
    SOURCE_MIRROR_URL ?= "http://example.org/yocto-cache/downloads/"
    SSTATE_MIRRORS ?= "file://.* http://example.org/yocto-cache/sstate-cache/PATH"

Notice the PATH variable, which yocto will substitute automatically. Also notice
that one has to inherit ``own-mirrors`` in yocto for this to work. If we ignore
the details of how and where the cache comes from (in this case http), this is
really all that is needed in the build.

Cache over HTTP
---------------
Yocto accepts caches that are served over HTTP, one simply inputs the URL as
seen in the example above. Accessing such a cache is then done automatically.
But updating the cache can be trickier, but it depends on the setup. The general
scheme is to simply copy the files from one's build to the cache server. This
can be done through scp, ftp, or if the cache server is mounted - by simple
copy.

For the HTTP server, one needs to allow to serve a directory plain and simple.
For nginx it would look like this:

.. code-block:: none
    :caption: ``nginx.conf`` on ``example.org``

    http {
        server {
            location /yocto-cache/ {
                alias     /var/www/yocto-cache/;
                index     index.html index.htm;
                autoindex on;
            }
        }
    }

When one updates the cache, this means writing to /var/www/yocto-cache in some
way.

Cache over NFS
--------------
Setting up a cache over NFS requires more setup on the server-side, but on the
other hand everyone that is given access to the NFS share can update the cache.

NFS controls what is shared through ``/etc/exports``, where each line specifies
a path to share, a host/hosts that can access it, and settings for that share.

.. code-block:: none
    :caption: ``/etc/exports`` on ``10.0.0.2``

    /var/yocto-cache 10.0.0.3(rw,no_root_squash,no_subtree_check)

This example would give ``10.0.0.3`` read-write access to ``/var/yocto-cache``,
which that system could simply mount and use as any other mounted file system.
The host can also be a subnet such as ``10.0.0.1/24``.

Watch out! This setup requires user ID's to match on the server and client, or
the whole point of having read-write access will be lost. There are ways of
getting around this, NFS has options such as ``anonuid`` and ``anongid`` that
can help if needed. Depending on setup, it might make sense to have a yocto
user, or a dedicated user for the CI system, that is the same for everyone who
shares the cache.

The client setup requires a mounting of the NFS share. It is easiest to add the
line to ``/etc/fstab`` as follows:

.. code-block:: none
    :caption: ``/etc/fstab`` on ``10.0.0.3``

    # NFS for yocto-cache on 10.0.0.2
    10.0.0.2:/var/yocto-cache /var/yocto-cache nfs rsize=8192,wsize=8192,timeo=14

This setup would effectively mirror ``/var/yocto-cache`` on the server to
``/var/yocto-cache`` on the client. After this it is enough to tell yocto that
the URL for downloads is ``file:///var/yocto-cache/downloads`` and similar for
the sstate-cache.

.. tags:: howto
