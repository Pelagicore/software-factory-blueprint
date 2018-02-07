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

        Version strings have the form X.Y.Z-GitRevision
    """

    # Same as a git commit
    allowedchars = string.hexdigits.lower()
    # A version string is X.Y.Z etc, where XYZ are digits
    versionchars = string.digits + "."

    def _skip(self, word):
        (version,sep,revparse) = word.partition('-')
        if version == word:
            return False # probably not a version string then
        else:
            return all_match(version, self.versionchars) and all_match(revparse, self.allowedchars)
