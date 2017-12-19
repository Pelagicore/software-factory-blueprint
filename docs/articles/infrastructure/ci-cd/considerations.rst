:orphan:

Considerations for Continuous Integration jobs
==============================================

General strategy
----------------
Continuous integration and continuous delivery jobs serve the purpose of quick
turn-around time for developers, providing easy feedback on work in a controlled
environment. As such, our jobs are designed with some basic properties:

* Build on-commit
* Fail builds early
* Make build status visible
* Make sure latest build is available to users

Yocto builds
------------
Yocto jobs generally takes a long time to run, and use lots of disk space. To
mitigate running time, consider :ref:`storing old builds in a cache
<setting-up-yocto-cache>` in a way that yocto can access. That way, the time of
a full build is reduced from 4 hours to about 30 minutes. Consider running parts
of the Yocto jobs in parallel on different machines, if possible.
