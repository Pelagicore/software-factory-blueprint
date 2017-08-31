
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

