from steps.context_steps import setup_default_mock


# pylint: disable=unused-argument
def before_scenario(context, scenario):
    """ Runs before each scenario """
    setup_default_mock()
