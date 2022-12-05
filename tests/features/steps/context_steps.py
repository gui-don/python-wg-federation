import builtins
import os
from pathlib import Path

from behave import given
from behave.runner import Context
from mockito import when, unstub

TEST_PATH = '/tmp/wg-federation-test'


# pylint: disable=unused-argument


@given('a system file “{path}” contains the following content “{content}”')
def mock_system_file(context, path: str, content: str):
    """
    Step impl
    """

    # sadly because pathlib is horrendous, it is not mock-able.
    # If possible, always prefer os over pathlib.
    when(os.path).exists(path).thenReturn(True)
    when(os.path).isfile(path).thenReturn(True)

    with open(file=get_modified_path(path), mode='a+', encoding='UTF-8') as file:
        file.truncate(0)
        file.seek(0)
        file.write(content)

    context.add_cleanup(clean_mocks)


@given('the environment variable "{env_var_name}" contains "{env_var_value}"')
def environment_variable_contains(context: Context, env_var_name: str, env_var_value: str):
    """ Step impl """
    when(os).getenv(env_var_name).thenReturn(env_var_value)

    context.add_cleanup(clean_mocks)


def clean_mocks():
    """ Unstub all mockito mocks """
    unstub()


def setup_default_mock():
    """
    Setup default mocks for all steps.
    Prepares the methods below to be mocked for specific calls
    """

    when(os.path).exists(...).thenCallOriginalImplementation()
    when(os.path).isfile(...).thenCallOriginalImplementation()

    when(Path).is_file().thenCallOriginalImplementation()
    when(os).getenv(...).thenCallOriginalImplementation()
    when(builtins).open(...).thenCallOriginalImplementation()


def get_modified_path(path: str):
    """
    Get a modified form of a path for functional testing.
    :param path:
    :return:
    """
    original_path = Path(path.replace('~', os.path.expanduser('~')))
    return Path(TEST_PATH) / original_path.relative_to(original_path.anchor)
