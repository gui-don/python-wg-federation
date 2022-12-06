import builtins
import os
import shutil
from pathlib import Path

from behave import given, then
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
    when(os.path).exists(get_path(path)).thenReturn(True)
    when(os.path).isfile(get_path(path)).thenReturn(True)

    with open(file=get_modified_path(path), mode='a+', encoding='UTF-8') as file:
        file.truncate(0)
        file.seek(0)
        file.write(content)

    context.add_cleanup(clean_mocks)
    context.add_cleanup(clean_files)


@then('the system file “{path}” should exist')
def system_file_exists(context: Context, path: str):
    """ Step impl """
    assert os.path.exists(get_modified_path(path))


@given('the environment variable "{env_var_name}" contains "{env_var_value}"')
def environment_variable_contains(context: Context, env_var_name: str, env_var_value: str):
    """ Step impl """
    when(os).getenv(env_var_name).thenReturn(env_var_value)

    context.add_cleanup(clean_mocks)


def clean_mocks():
    """ Unstub all mockito mocks """
    unstub()


def clean_files():
    """ Unstub all mockito mocks """
    shutil.rmtree(TEST_PATH)


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


def get_modified_path(path: str) -> str:
    """
    Get a modified form of a path for functional testing.
    :param path:
    :return:
    """

    original_path = Path(get_path(path))
    modified_path = str(Path(TEST_PATH) / original_path.relative_to(original_path.anchor))
    Path(modified_path).parent.mkdir(parents=True, exist_ok=True)
    return modified_path


def get_path(path: str) -> str:
    """
    Returns path with expanded home (~)
    :param path:
    :return:
    """
    return path.replace('~', os.path.expanduser('~'))
