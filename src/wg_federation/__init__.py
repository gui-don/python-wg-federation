""" wg-federation """

from .hello import Hello
from .constants import __version__


def main():
    """ Main """
    _hello: Hello = Hello()
    _hello.hello(__version__)
