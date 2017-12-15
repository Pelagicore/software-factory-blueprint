:orphan:

Code reviews
************

Code reviews are essential for maintaining a high quality in a code base.

Code reviews can take place in a multitude of ways, for instance by reviewing
the code during a meeting, by reading through a patch received via email, or by
using a code review tool such as GitLab merge requests, or Gerrit code review.

Regardless of the setting in which the code review is done, it is often good to
have a checklist for what to check during a code review. In
:ref:`code-review-checklist` you can find a list of recommended topics to cover
during a code review. It is difficult to make such a list complete, so it is
important to not assume that the code review is done simply because the list
has been exhausted. Each project and each situation will require a context
sensitive review in addition to any generic list.

.. _code-review-checklist:

Code review checklist
=====================

Fog Creek have created a nice checklist for code reviews, which we recommend
following. The list is available here: [#checklist]_.

In addition to this checklist, the list given below can also be used.

Checklist
---------

.. note::

    Topics that prove to be controversial, or more difficult to understand will
    be outlined further in the :ref:`rationales` section.

General
^^^^^^^

* Verify that the license of all dependencies are respected
  (:ref:`rationale<licenses-of-dependencies>`)

.. _rationales:

Rationales
----------

.. _licenses-of-dependencies:

Licenses of dependencies
^^^^^^^^^^^^^^^^^^^^^^^^

Some licenses prevent usage of the licensed software under certain conditions.
It is important to ensure the software being written complies with the licenses
of the software it uses - failure to do so may cause legal issues.

When checking for license violations, ensure you understand the licenses of all
the software used by the software being reviewed, and check that the licensed
software is only used in permitted ways.

It is very difficult to perform automatic checks of license compliance, since
this would require a very complex license checker, which is why this is
recommended as a manual step.

.. [#checklist] https://blog.fogcreek.com/increase-defect-detection-with-our-code-review-checklist-example/

.. tags:: process
