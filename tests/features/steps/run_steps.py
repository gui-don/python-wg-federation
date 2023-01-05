import re
import sys

from behave import when
from behave.runner import Context

from wg_federation import Main
from wg_federation.di.container import Container


@when('we run program with "{argv}"')
# pylint: disable=unused-argument
def run_program(context: Context, argv: str = ''):
    """ step impl """

    # This algorithm poorly handles quotes in the given command line
    # Flawed, but sufficient for tests, until someone smart makes it better.
    list_argv = re.split(r'(?:"|\') ?', 'wg-federation ' + argv)
    for i, arg in enumerate(list_argv):
        if i % 2 == 0:
            list_argv[i] = arg.split()
        else:
            list_argv[i] = [arg]

    sys.argv = [item for sublist in list_argv for item in sublist]

    try:
        Main(Container()).main()
    except SystemExit:
        pass
