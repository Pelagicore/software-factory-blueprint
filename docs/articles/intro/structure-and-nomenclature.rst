.. _structure-and-nomenclature:

Structure and nomenclature
**************************

Nomenclature
============

* **SWF Platform Blueprint** - Contains the overall roles, responsibilities,
  process, and instructions involved in working with a Yocto based Linux
  platform in the IVI domain. A project is intended to use the Blueprint
  as-is and extend it with a project specific Deployment. Imagine a layered
  view, where this is the bottom and most generic layer.
* **SWF Platform Deployment** - A concrete SWF that describes and documents
  how the project's platform is developed. A SWF Platform Deployment re-uses
  the SWF Platform Blueprint for the generic parts that are not project
  specific, i.e. it extends the Blueprint.
* **Software Factory (SWF)** - This is a term used within the SWF Platform
  Deployment to refer to itself. This is not additional documentation, but
  rather a convenient term.
* **Platform** - The exact content and definition of what a platform is, is
  project specific.

Structure
=========

Incorrect documentation is worse than no documentation at all in many cases,
and the requirement on correct content makes the maintenance of the SWF
important. The maintenance complexity is assumed to be the most important
problem to mitigate, and this affects the way the content is structured
and written.

The SWF is written and structured in different abstraction levels. The most
abstract and over-arching parts are *Processes*. These typically refers
various *Instructions* which in turn typically refers to a set of
*How-To*'s. *Processes*, *Instructions*, and *How-To*'s could be seen as
structured in layers with the most abstract content as top tier. There
should be references downwards, e.g. from *Instructions* to *How-To*'s,
but as few references upwards as possible. References between articles on
the same level are sometimes needed but should be kept to a minimum as
well. The reason is that an over-arching process should be possible to
change by modifying which *Instructions* and *How-To*'s are referenced
and in what order, without needing to modify any (or at least as little
as possible) of the less abstract content. Likewise, modifying a *How-To*
should not affect any more abstract content that references it, more than
absolutely necessary.

This is not strictly enforced in any way but it is a guideline for any
contribution of content in order to mitigate future maintenance issues.

.. blockdiag::

   diagram {
     orientation = portrait;

     A [label="Process"];
     B [label="Instruction"];
     C [label="Instruction"];
     D [label="How-To"];
     E [label="How-To"];
     F [label="How-To"];

     group {
        color = red;
        A;
     }

     group {
        color = blue;
        B;
        C;
     };

     group {
        color = green;
        D;
        E;
        F;
     }

     A -- B;
     A -- C;
          C -- D;
          C -- E;
          C -- F;
   }

* Red block is the *highest* level of abstraction
* Green block is the next *highest* level of abstraction
* Blue block is the *lowest* level of abstraction, and thus the most
  concrete level.

.. tags:: instruction
