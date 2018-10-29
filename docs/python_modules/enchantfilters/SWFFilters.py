#
# Copyright (C) 2018 Pelagicore AB
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

from enchant.tokenize import Filter
import string

def all_match(string, allowed_chars):
    return all(c in allowed_chars for c in string)

class GitCommitFilter(Filter):
    """ If a word looks like a git commit hash (long or short), ignore it """

    # A git commit is only lowercase hex vars
    allowedchars = string.hexdigits.lower()

    def _skip(self, word):
        if len(word) == 40 or len(word) == 7:
            return word.lower() == word and all_match(word, self.allowedchars)
        else:
            return False

class VersionStringFilter(Filter):
    """ If a word looks like a version string, ignore it

        Version strings have the form X.Y.Z-GitRevision, or optionally
        the form X.Y.Z-CodeName-GitRevision, where CodeName can be anything.
    """

    # Same as a git commit
    allowedchars = string.hexdigits.lower()
    # A version string is X.Y.Z etc, where XYZ are digits
    versionchars = string.digits + "."

    def _skip(self, word):
        (version,sep,rest) = word.partition('-')
        if version == word:
            return False # probably not a version string then

        # The version string has to look right
        if not all_match(version, self.versionchars):
            return False

        (codename,sep,revparse) = rest.partition('-')
        if codename == rest:
            # Code name is optional, and we do not check it
            return all_match(rest, self.allowedchars)
        else:
            return all_match(revparse, self.allowedchars)
