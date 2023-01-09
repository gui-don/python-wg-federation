from contextlib import contextmanager
from pathlib import Path

from mockito import patch

from steps.context_steps import setup_default_mock, clean_mocks, get_modified_path
from wg_federation.data_transformation.locker.file_configuration_locker import FileConfigurationLocker
from wg_federation.utils.utils import Utils


# pylint: disable=unused-argument
def before_scenario(context, scenario):
    """ Runs before each scenario """
    setup_default_mock()

    patch(Utils.open, mock_open)
    # pylint: disable=protected-access
    patch(FileConfigurationLocker._do_lock, mock_lock)

    context.add_cleanup(clean_mocks)


def mock_open(file: str, mode: str, encoding: str):
    """
    Mock/Patch of the Utils.open method to use test modified path instead of real one.
    :param file:
    :param mode:
    :param encoding:
    :return:
    """
    modified_path = get_modified_path(file)

    return open(file=modified_path, mode=__prepare_open_mode(modified_path, mode), encoding=encoding)


@contextmanager
def mock_lock(location: str, mode: str, flags):
    """
    Mock/Patch of file locking using ConfigurationLocker to use modified test path instead of real ones.
    :param location:
    :param mode:
    :param flags:
    :return:
    """
    modified_path = get_modified_path(location)

    with open(file=modified_path, mode=__prepare_open_mode(modified_path, mode), encoding='UTF-8') as file:
        yield file


def __prepare_open_mode(location: str, mode: str) -> str:
    if mode in ['a++', 'w++']:
        Path(location).parents[0].mkdir(parents=True, exist_ok=True)
        return mode[:-1]

    return mode
