:orphan:

FreeIPA
=======

FreeIPA is an identity management system which comes with an LDAP server,
kerberos and a web UI built in. It has the ability to "Manage Linux users and
client hosts in your realm from one central location with CLI, Web UI or RPC
access." It can thus be used to centrally manage accounts and allow users to
login to multiple servers and websites with the same credentials.

Server setup
------------

This guide assumes you are running Ubuntu server 16:04 but should work for most
major linux distributions.

Prerequisites
^^^^^^^^^^^^^

Choose a domain to use for your deployment. It is important that you have control
over it. Never use an example domain or a top domain which does not exist, it
will only cause problems later on. It is okay to use a subdomain which is not
public though.

.. warning::

    It is recommended to use a dedicated host or VM (not docker) for running
    FreeIPA, with a dedicated IPv4 address. FreeIPA server integrates into a lot
    of services on the host and running other services on the same host will
    eventually cause problems.

It is important that the server has a fully qualified domain name. You can either
set the hostname when you create the server or set it from the command line
after the server is created, using the hostname command:

.. code-block:: bash

    hostname ipaserver.example.com

Then set up ``/etc/hosts`` file with the fully qualified domain name pointing to
the servers IP:

.. code-block:: none
    :caption: Example /etc/hosts

    # Replace with your own values
    198.51.100.5 ipaserver.example.com ipaserver

Then use dig to check the A record for your server:

.. code-block:: bash

    dig +short ipaserver.example.com A

This should return the ipv4 address of the server.

Installation
^^^^^^^^^^^^

.. code-block:: bash
    :caption: Install the packages

    apt install freeipa-server freeipa-server-dns

.. code-block:: bash
    :caption: Setup the FreeIPA server

    # Replace the values below with your own. Never use example.com in a real deployment.
    ipa-server-install --setup-dns --hostname=ipaserver.example.com --realm=EXAMPLE.COM --domain=example.com --no_hbac_allow 

During installation you will be asked to setup forwarding DNS servers. Either
set them to the DNS provided by your organization, internet provider or public
ones like Google ``8.8.8.8`` ``8.8.4.4`` or Cloudflare ``1.1.1.1`` ``1.0.0.1``.

You will also be asked to provide an admin password and Directory Manager
password. The admin is a regular user with admin privileges. The Directory
Manager is a special user like root in Linux or MySQL.

You can manage FreeIPA using the web client by going to
``https://ipaserver.example.com/ipa/ui/`` and using the admin user you setup
during installation.

.. tip::

    If the installation fails, use the uninstall command before trying again and
    refer to the :ref:`troubleshooting` section.

    .. code-block:: bash

        ipa-server-install --uninstall

.. warning::

    If you want to run Docker containers on the same machine as FreeIPA, be
    aware of how Docker configures DNS by looking at the :ref:`freeipa-docker`
    section.

Enroll a client
---------------

A client installation allows for users to login with password or public key over
SSH to a linux computer. Who is allowed to login and use resources on the
machine is controlled centrally from FreeIPA through policies.

.. tip::

    A FreeIPA server is already a client. The ``ipa-server-install`` command
    also set up the host as a client.

.. warning::

    If the client was previously connected to OpenLDAP, first disconnect it from
    LDAP using the instructions in the troubleshooting section:
    :ref:`remove-openldap`

.. code-block:: bash

    apt install freeipa-client

Set fully qualified hostname with

.. code-block:: bash

    # Example value
    hostname host.example.com

Edit ``/etc/resolvconf/resolv.conf/head`` and put the ipaserver first:

.. code-block:: none
    :caption: Example /etc/resolvconf/resolv.conf/head

    nameserver 192.0.2.5
    nameserver 192.0.2.6
    # Fallback DNS
    nameserver 8.8.8.8

Update resolv.conf using:

.. code-block:: none

    resolvconf -u

Enroll client and use autodiscovery through DNS to find all the settings

.. code-block:: none

    ipa-client-install --mkhomedir --enable-dns-updates --force-ntpd

If you did not install DNS with the FreeIPA server or cannot change the
nameserver on the client, you need to specify the server address and the logical
domain.

.. code-block:: none

    ipa-client-install --mkhomedir --enable-dns-updates --force-ntpd --server=host.example.com --domain=example.com

On Ubuntu 16.04 you need to enable home directory creation manually:

.. code-block:: none

    sed -i -r -e 's/Default:\s\w+/Default: yes/;' /usr/share/pam-configs/mkhomedir
    # and add the homedir option manually because it cannot be scripted.
    pam-auth-update

Verify connectivity
^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    id admin
    id someipauser

Should return uid, guid and groups of the ipa user. The numbers will be much
higher than local users. Check out the troubleshooting section if the command
fails.

.. code-block:: none
    :caption: Example output of 'id admin'

    uid=733200000(admin) gid=733200000(admins) groups=733200000(admins)

.. _troubleshooting:

Troubleshooting
---------------

Server
^^^^^^

Installation issues
"""""""""""""""""""

If the installation fails with "Unable to restart server", look in the logs for
the certificate server.

.. code-block:: bash

    journalctl -xe -u pki-tomcatd

If you find something like "Unable to stat /bin/java" it means that the java
path is misconfigured. Find java through 'which java' and create a symbolic link
in place of the missing binary.

.. code-block:: bash

    ln -s /path/to/java /bin/java

When an installation fails it may be necessary to delete the configuration for
the certificate server created during installation. Especially if it fails with
"Unable to restart server"

.. code-block:: bash

    # When the installation fails, delete all certificate server configuration
    rm -rf /var/log/pki/pki-tomcat
    rm -rf /etc/sysconfig/pki-tomcat
    rm -rf /etc/sysconfig/pki/tomcat/pki-tomcat
    rm -rf /var/lib/pki/pki-tomcat
    rm -rf /etc/pki/pki-tomcat
    rm -rf /etc/default/pki-tomcat
    rm -rf /etc/dogtag/tomcat/pki-tomcat
    ipa-server-install --uninstall -U

.. _freeipa-docker:

Running docker with FreeIPA server
""""""""""""""""""""""""""""""""""

If you are running Docker on the same machine as FreeIPA server you will have
issues with DNS. Since FreeIPA acts as a DNS server it will add ``nameserver
127.0.0.1`` to ``/etc/resolv.conf``. When setting up a new container, the
docker daemon copies ``/etc/resolv.conf`` and filters out all localhost IP
address ``nameserver`` entries. If there are no more ``nameserver`` entries
left, the daemon will then add Google DNS nameservers (8.8.8.8 and 8.8.4.4)
to the containers DNS configuration.

To avoid Google DNS servers, use the ``--dns`` option with ``docker run`` or
add an entry to ``/etc/docker/daemon.json``:

.. code-block:: json

    {
        "dns": ["198.51.100.5", "198.51.100.6"]
    }

Client
^^^^^^

If you cannot find a ipa user using the id command, it is most probably because
of a misconfigured nsswitch.conf Make sure to add 'sss' at the appropriate
places according to the example below. The ordering is important. 'sss' should
always be after 'compat' or 'files'. This dictates in which order the system
will lookup users. A misconfigured nsswitch.conf may result in the inability
to access the system.

.. note::

    "sss" refers to SSSD, a system daemon. Its primary function is to provide
    access to identity and authentication remote resource through a common
    framework that can provide caching and offline support to the
    system." [#SSSD]_

.. code-block:: none

    # /etc/nsswitch.conf
    #
    # Example configuration of GNU Name Service Switch functionality.
    # If you have the `glibc-doc-reference' and `info' packages installed, try:
    # `info libc "Name Service Switch"' for information about this file.

    passwd:         compat sss
    group:          compat sss
    shadow:         compat sss
    gshadow:        files

    hosts:          files dns
    networks:       files

    protocols:      db files
    services:       db files sss
    ethers:         db files
    rpc:            db files

    netgroup:       nis sss
    sudoers: files sss

Home directory
""""""""""""""

If no home directory is created upon loging in with an ipa user, use the
commands below. 

.. code-block:: none

    # Source: https://bgstack15.wordpress.com/2017/06/26/enabling-mkhomedir-on-ubuntu-for-freeipa/
    # Put 'yes' after 'Default:'
    sed -i -r -e 's/Default:\s\w+/Default: yes/;' /usr/share/pam-configs/mkhomedir
    pam-auth-update # and add the homedir option manually because it cannot be scripted.

.. _remove-openldap:

Remove OpenLDAP connection
""""""""""""""""""""""""""
.. code-block:: bash

    apt purge libnss-ldapd libpam-ldapd nslcd nscd
    # You may also want to
    apt autoremove

Edit nsswitch.conf and remove references to LDAP.

Check if LDAP users disappeared from the system:

.. code-block:: bash

    getent passwd

LDAP users will have a higher uid than system users.

Try to identify an LDAP user:

.. code-block:: bash

    # Should return "no such user"
    id someldapuser

.. [#SSSD] https://wiki.archlinux.org/index.php/LDAP_authentication#Online_and_Offline_Authentication_with_SSSD
