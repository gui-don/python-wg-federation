"""
    Defines all constants for wg-federation
"""
import os

CHANGELOG_FILENAME = 'CHANGELOG.md'
__version__ = 'UNDEFINED'

pwd = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(pwd, '../../', CHANGELOG_FILENAME), encoding='utf-8') as changelog_file:
    __version__ = changelog_file.readline().rstrip()
