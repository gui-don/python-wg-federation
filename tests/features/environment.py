from mockito import patch

from steps.context_steps import setup_default_mock, clean_mocks, get_modified_path
from wg_federation.utils.utils import Utils


# pylint: disable=unused-argument
def before_scenario(context, scenario):
    """ Runs before each scenario """
    setup_default_mock()

    patch(Utils.open, mock_open)

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

    if 'a++' == mode:
        modified_path.parents[0].mkdir(parents=True, exist_ok=True)

    return open(file=modified_path, mode=mode, encoding=encoding)
