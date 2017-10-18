#
# Copyright (C) 2017 Pelagicore AB
#
# Permission to use, copy, modify, and/or distribute this software for
# any purpose with or without fee is hereby granted, provided that the
# above copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL
# WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR
# BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES
# OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS,
# WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION,
# ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS
# SOFTWARE.
#
# For further information see LICENSE

import os
import os.path
import string

# What directory is this script in?
THISDIR=os.path.dirname(os.path.realpath(__file__))

# Python way of writing ../../
KEYVALUEFILE=os.path.join(os.path.dirname(os.path.dirname(THISDIR)), "swf-substitutions.txt")

def substitutions(keyvaluefile=KEYVALUEFILE):
    """
    Read a file with key=value pairs, one on each line. Returns an empty dict on errors and a dict
    corresponding to those pairs on success.
    """
    subs = dict()
    if not os.path.exists(keyvaluefile):
        print("No substitution file found: {}".format(keyvaluefile))
        return subs

    with open(keyvaluefile, 'r') as f:
        for line in f:
            if line.startswith("#"): # Comments
                continue
            elif line.strip() == "": # Empty lines
                continue
            sp = line.split('=', 1)
            if len(sp) != 2:
                print("Malformed key/value store")
                return dict()
            subs[sp[0]] = sp[1].strip()
    return subs

