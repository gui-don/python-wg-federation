import os

from behave import given
from behave.runner import Context


@given('the environment variable "{env_var_name}" contains "{env_var_value}"')
def environment_variable_contains(context: Context, env_var_name: str, env_var_value: str):
    """ Step impl """
    if os.environ.get(env_var_name):
        raise (Exception(f'Cannot set {env_var_name} environment variable: already set in context.'
                         f'This is to avoid behave to override system environment variables.'))

    context.add_cleanup(clean_environment_variable, env_var_name)
    os.environ[env_var_name] = env_var_value


def clean_environment_variable(env_var_name: str):
    """ Unset previously set environment variables """
    os.unsetenv(env_var_name)
