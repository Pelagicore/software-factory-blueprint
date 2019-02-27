# Software Factory Blueprint
PELUX Software Factory Blueprint documentation

Software Factory Blueprint is maintained at https://github.com/Pelagicore/software-factory-blueprint

## Note
You probably don't want to build the blueprint on its own, but rather use it as part of a deployment
Software Factory. This approach is described in the intro chapter of these docs.

## Dependencies
* cmake
* Sphinx
* sphinxcontrib-seqdiag
* sphinxcontrib-blockdiag
* sphinxcontrib-actdiag
* sphinxcontrib-manpage
* sphinxcontrib-spelling
* sphinx\_rtd\_theme
* texlive-latex-base (when building PDF)
* texlive-latex-extra (when building PDF)
* texlive-latex-recommended (when building PDF)

###  Install build dependencies on Debian

```
sudo apt install cmake python-pip
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
* `PERFORM_SPELL_CHECK` - Performs a spell check on files. Set to ON by default

Configure and build from the git top dir like so:

    cmake -H. -Bbuild
    cd build
    make

After a successful build you can find the documentation in `build/docs/html/`
if you open the `index.html` in your browser you will see the entry point.

## Structure
The project is intended to be used as a submodule in another project, in
which case that project should take care of configuring, building, generating,
etc. If the cmake file in this project is not the one invoked explicitly,
e.g. when it is not the top level project cmake file, nothing will happen. This
is to make sure this project does not interfere with the using project.

In order to not interfere with how the sidebar toctree is constructed in a
project using this as a submodule, all files in this repo that contain a
toctree need to have the suffix `.trst` instead of just `.rst`. This project
is configured to include `.trst` files while projects using this as a
submodule should ignore that suffix.

### Understanding Spell Check
A spell check is performed during the build step by default. It uses in-built
language specific dictionaries and project specific dictionaries
(spelling_wordlist.txt) to verify the spellings and causes the build to fail in
case of any typos.

The project, which uses this blueprint, should have its own custom dictionary,
similar to the one in blueprint (spelling_wordlist.txt). One can supply
multiple word lists to the spell-checker plugin, by providing a list instead
of a string.

The spell checker is added as a custom target, so to run it manually, simply
type (after running cmake):

    make spelling

To build the docs without checking the spelling, type:

    make sphinx-html

# License and Copyright
Copyright &copy; 2017 Pelagicore AB
Copyright &copy; 2018-2019 Luxoft Sweden AB

This work is licensed under the Creative Commons
Attribution-ShareAlike 4.0 International License. To view a copy of
this license, visit http://creativecommons.org/licenses/by-sa/4.0/ or
send a letter to Creative Commons, PO Box 1866, Mountain View, CA
94042, USA.

Code and scripts are licensed under LGPL 2.1

SPDX-License-Identifier: CC-BY-SA-4.0

