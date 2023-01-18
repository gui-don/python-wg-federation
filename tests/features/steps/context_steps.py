import builtins
import os
import re
import shutil
from pathlib import Path

import xdg
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

    with open(file=get_modified_path(path), mode='a+', encoding='UTF-8') as file:
        file.truncate(0)
        file.seek(0)
        file.write(content)

    context.add_cleanup(clean_mocks)
    context.add_cleanup(clean_files)


@then('the system file “{path}” should exist')
def system_file_exists(context: Context, path: str):
    """ Step impl """
    assert os.path.exists(path)
    context.add_cleanup(clean_files)


@then('the system file “{path}” should not exist')
def system_file_not_exists(context: Context, path: str):
    """ Step impl """
    assert not os.path.exists(path)


@then('the system file “{path}” should contain “{reg_pattern}”')
def system_file_contains(context: Context, path: str, reg_pattern: str):
    """ Step impl """
    with open(file=get_modified_path(path), mode='r', encoding='UTF-8') as file:
        assert re.search(reg_pattern, file.read(), re.MULTILINE)


@then('the system file “{path}” should not contain “{reg_pattern}”')
def system_file_not_contains(context: Context, path: str, reg_pattern: str):
    """ Step impl """
    with open(file=get_modified_path(path), mode='r', encoding='UTF-8') as file:
        assert not re.search(reg_pattern, file.read(), re.MULTILINE)


@given('the environment variable "{env_var_name}" contains "{env_var_value}"')
def environment_variable_contains(context: Context, env_var_name: str, env_var_value: str):
    """ Step impl """
    when(os).getenv(env_var_name).thenReturn(env_var_value)

    context.add_cleanup(clean_mocks)


def clean_mocks():
    """ Unstub all mockito mocks """
    unstub()


def clean_files():
    """ Remove all tests files within the test scope """
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
    if path.startswith(TEST_PATH):
        return path

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
    path = path.replace('~', os.path.expanduser('~'))
    return path.replace('${XDG_RUNTIME_DIR}', str(xdg.XDG_RUNTIME_DIR))
