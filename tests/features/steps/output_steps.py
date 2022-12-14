import re

from behave import then
from behave.runner import Context
from wg_federation.constants import __version__


@then('the syslog contains "{reg_pattern}"')
def syslog_contain(context: Context, reg_pattern: str):
    """ Step impl """
    assert re.search(reg_pattern, context.log_capture.getvalue()) is not None


@then('the output contains "{reg_pattern}"')
def output_contains(context: Context, reg_pattern: str):
    """ Step impl """
    assert re.search(reg_pattern, context.stdout_capture.getvalue()) is not None


@then('the stderr contains "{reg_pattern}"')
def stderr_contains(context: Context, reg_pattern: str):
    """ Step impl """
    assert re.search(reg_pattern, context.stderr_capture.getvalue()) is not None


@then('the syslog does not contain "{reg_pattern}"')
def syslog_not_contain(context: Context, reg_pattern: str):
    """ Step impl """
    assert re.search(reg_pattern, context.log_capture.getvalue()) is None


@then('the output does not contain "{reg_pattern}"')
def output_not_contain(context: Context, reg_pattern: str):
    """ Step impl """
    assert re.search(reg_pattern, context.stdout_capture.getvalue()) is None


@then('the stderr does not contain "{reg_pattern}"')
def stderr_not_contains(context: Context, reg_pattern: str):
    """ Step impl """
    assert re.search(reg_pattern, context.stderr_capture.getvalue()) is None


@then('the output only contains current version')
def ouptut_contains_version(context: Context):
    """ step impl """
    assert re.search(fr'^{__version__}$', context.stdout_capture.getvalue()) is not None
