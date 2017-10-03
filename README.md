
# Software Factory Blueprint
PELUX Software Factory Blueprint documentation

Software Factory Blueprint is maintained at https://github.com/Pelagicore/software-factory-blueprint

Maintainer: Joakim Gross <joakim.gross@pelagicore.com>

## Note
You probably don't want to build the blueprint on its own, but rather use it as part of a deployment
Software Factory. This approach is described in the intro chapter of these docs.

## Dependencies
* Sphinx
* sphinxcontrib-seqdiag
* sphinxcontrib-blockdiag
* sphinxcontrib-actdiag
* sphinxcontrib-manpage
* sphinx\_rtd\_theme
* texlive-latex-base (when building PDF)
* texlive-latex-extra (when building PDF)
* texlive-latex-recommended (when building PDF)

###  Install build dependencies on Debian

```
sudo apt-get install python-pip
sudo pip install \
    sphinxcontrib-seqdiag \
    sphinxcontrib-blockdiag \
    sphinxcontrib-actdiag \
    sphinxcontrib-manpage \
    sphinx_rtd_theme
```


## Building
The project uses cmake to configure the build. Supported options are:

* `ENABLE_PDF` - Enables building the docs in PDF format. Set to OFF by default

Configure and build from the git top dir like so:

    cmake -H. -Bbuild
    cd build
    make

After a successfull build you can find the documentation in `build/docs/html/`
if you open the `index.html` in your browser you will see the entry point.

The project is intended to be used as a submodule in another project, in
which case that project should take care of configuring, building, generating,
etc. If the cmake file in this project is not the one invoked explicitly,
i.e. it is not the top level project cmake file, nothing will happen. This
is to make sure this project does not interfere with the using project.

And because of the fact how Sphinx creates toctrees in sidebars all the files
which contain a toctree need to have the suffix `.trst` instead of just `.rst`.
This way the projects which use this as a submodule are able to ignore the
toctrees and build their own instead.

# License and Copyright
Copyright (C) Pelagicore AB 2017

This work is licensed under the Creative Commons
Attribution-ShareAlike 4.0 International License. To view a copy of
this license, visit http://creativecommons.org/licenses/by-sa/4.0/ or
send a letter to Creative Commons, PO Box 1866, Mountain View, CA
94042, USA.

Code and scripts are licensed under LGPL 2.1

SPDX-License-Identifier: CC-BY-4.0

