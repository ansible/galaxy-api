from collections import namedtuple
import re


CollectionFilename = namedtuple("CollectionFilename", ["namespace", "name", "version"])

FILENAME_REGEXP = re.compile(
    r"^(?P<namespace>\w+)-(?P<name>\w+)-" r"(?P<version>[0-9a-zA-Z.+-]+)\.tar\.gz$"
)
VERSION_REGEXP = re.compile(r"""
^
(?P<major>0|[1-9][0-9]*)
\.
(?P<minor>0|[1-9][0-9]*)
\.
(?P<patch>0|[1-9][0-9]*)
(?:
    -(?P<pre>[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)
)?
(?:
    \+(?P<build>[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)
)?
$
""", re.VERBOSE | re.ASCII)


def parse_collection_filename(filename):
    """
    Parses collection filename.

    Parses and validates collection filename. Returns CollectionFilename named tuple.
    Raises ValueError if filename is not a valid collection filename.
    """
    match = FILENAME_REGEXP.match(filename)

    if not match:
        raise ValueError("Invalid filename. Expected: {namespace}-{name}-{version}.tar.gz")

    namespace, name, version = match.groups()

    match = VERSION_REGEXP.match(version)
    if not match:
        raise ValueError("Invalid version string. Expected semantic version format.")

    return CollectionFilename(namespace, name, version)
