.. _create-an-initial-index:

Create an initial index
***********************

The actual structure of the documentation might be quite different of the file
structure of the restructured text files. To set up a useful structure the
docs/index.rst file is used, which in it self points to articles and deeper
index files for chapters, etc. This file makes it also possible to reuse the
content from the SWF Blueprint. Let's look at a example implementation:

.. code-block:: rst

    .. toctree::
      :caption: Table of contents
      :maxdepth: 3
 
      chapters/example/index
      swf-blueprint/docs/articles/licensing/index

This will create a table of contents which will show headlines 3 levels deep.
The index files referenced here can have their own toctrees, those will show
up as children.

It takes a little bit of time to get the feeling on how to create meaningful
toctrees from different sources but it has a big advantage where you can
compile a coherent documentation from different sources.

.. note:: Every toctree in the initial index file will show up as a caption
          in the sidebar.

.. tags:: howto
