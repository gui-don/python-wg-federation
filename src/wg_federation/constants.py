"""
    Defines all constants for wg-federation
"""
import os
import importlib.util

REGEXP_WIREGUARD_KEY = r'^[0-9A-Za-z+/]{43}[=]$'
CHANGELOG_FILENAME = 'CHANGELOG.md'
VERSION_FILENAME = '__version__.txt'
HAS_SYSTEMD = False
__version__ = 'UNDEFINED'

pwd = os.path.dirname(os.path.realpath(__file__))


def read_version(filename: str) -> str:
    """
    Read the version from a given filename
    :param filename: the full path and filename of the version file
    :return: the version
    """
    with open(filename, encoding='utf-8') as version_file:
        return version_file.readline().rstrip()


try:
    __version__ = read_version(os.path.join(pwd, '../../', CHANGELOG_FILENAME))
except FileNotFoundError:
    __version__ = read_version(os.path.join(pwd, VERSION_FILENAME))


HAS_SYSTEMD = importlib.util.find_spec('systemd') is not None
