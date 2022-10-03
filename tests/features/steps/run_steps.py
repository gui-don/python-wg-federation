import sys

from behave import when
from behave.runner import Context

from wg_federation import Main
from wg_federation.di.container import Container


@when('we run program with "{argv}"')
# pylint: disable=unused-argument
def run_program(context: Context, argv: str = ''):
    """ step impl """
    sys.argv = ['wg-federation'] + argv.split()
    try:
        Main(Container()).main()
    except SystemExit:
        pass
