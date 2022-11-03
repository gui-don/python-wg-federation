import builtins
import os
from pathlib import Path

from behave import given
from behave.runner import Context
from mockito import when, unstub, ANY, mock, kwargs


@given('a system file “{path}” contains the following content “{content}”')
def mock_system_file(context, path: str, content: str):
    """
    Step impl
    """

    path = path.replace('~', os.path.expanduser('~'))

    file = mock(strict=True)
    when(file).fread(ANY).thenReturn(content)
    when(file).read(ANY).thenReturn(content)
    # Yes: necessary because it’s a stub
    # pylint: disable=unnecessary-dunder-call
    when(file).__enter__(...).thenReturn(content)
    when(file).__exit__(...).thenReturn(content)

    when(builtins).open(file=path, **kwargs).thenReturn(file)

    when(os.path).isfile(path).thenReturn(True)
    when(os.path).exists(path).thenReturn(True)

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
