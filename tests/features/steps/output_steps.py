import re

from behave import then
from behave.runner import Context
from wg_federation.constants import __version__


@then('the output contains "{reg_pattern}"')
def output_contains(context: Context, reg_pattern: str):
    """ Step impl """
    assert re.search(reg_pattern, context.stdout_capture.getvalue()) is not None


@then('the output does not contain "{reg_pattern}"')
def output_not_contain(context: Context, reg_pattern: str):
    """ Step impl """
    assert re.search(reg_pattern, context.stdout_capture.getvalue()) is None


@then('the output only contains current version')
def ouptut_contains_version(context: Context):
    """ step impl """
    assert re.search(fr'^{__version__}$', context.stdout_capture.getvalue()) is not None
