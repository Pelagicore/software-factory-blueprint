:orphan:

Creating a release process
==========================

In order to ensure a high quality software release that is traceable,
reproducible and so on, it is important to have a well-defined release process.
We describe a simple process for how to create a release process.

It is important to document the process and the various steps in it. In order to
be able to improve the actual process, and to keep it transparent we suggest
that the release process is kept together with the rest of the documentation for
the project.

Create a list of artifacts
--------------------------
Once released, it is important to know what was part of that specific release.
For that, a list of artifacts is required. These artifacts constitute the
product of the release, i.e. the matter that is released. This means that the
recipient of the release should need nothing more than the artifacts (except
readily available tooling, et cetera) in order to be able to use the release.

We recommend having a file with release notes as one of the artifacts, so a user
only needs one file to read up on the release contents.

Create a list of component attributes for the release
-----------------------------------------------------
These attributes are mostly useful internally for being able to tie the various
components of the release to the actual release. Such an attribute could be a
tag that points out a specific revision of the source code, if components are
stored in source code repositories. Other types of attributes could be naming
schemes or file name patterns.

Create a list of tasks that needs to be done for the release
------------------------------------------------------------
Given the list of artifacts and the attributes required to point out the
components, one has a simple way of pointing out a release. But before
releasing, one has to make sure the released matter is of high quality. A
checklist of tasks to be done before releasing will make sure nothing is
overlooked.

Such a list would typically involve creating the needed attributes, but also
things like release-testing (if any), deciding on a version number and so on.

Populate the how-tos for the release process
--------------------------------------------
These how-tos would contain the most hands-on instructions for actually
performing a release. It can be seen as an extension of the checklist, but it
would also add the ordering of what to do and when.

Make sure the how-tos contain steps to improve the process. The release process
is not static but should evolve over time and adapt according to experiences of
running it.

.. tags:: howto process
