""" constants.py test suit """
import re

from wg_federation import constants


class TestConstants:
    """ Test constants.py """
    # pylint: disable=line-too-long
    SEMVER_REGEXP = r'^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$'

    def test_version(self):
        """ it fetches and returns the current application version """
        assert re.match(self.SEMVER_REGEXP, constants.__version__)
