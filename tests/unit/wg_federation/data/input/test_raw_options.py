from wg_federation.data.input.command_line.command_line_argument import CommandLineArgument
from wg_federation.data.input.raw_options import RawOptions


class TestRawOptions:
    """ Test RawOptions class """

    def test_get_all_options_names(self):
        """ it returns its options names """
        assert 'verbose' in RawOptions.get_all_options_names()
        assert 'log_level' in RawOptions.get_all_options_names()
        assert 'debug' in RawOptions.get_all_options_names()

    def test_get_argument_depth(self):
        """ it returns the default arguments maximum depth """
        assert 2 == RawOptions.get_argument_depth()

    def test_get_argument_depth_2(self):
        """ it returns a specific arguments maximum depth """
        assert 3 == RawOptions.get_argument_depth(
            [
                CommandLineArgument(
                    subcommands=[
                        CommandLineArgument(
                            subcommands=[
                                CommandLineArgument()
                            ]
                        ),

                    ],
                )
            ]
        )

    def test_get_all_argument_keys(self):
        """ it returns all possible arguments keys """
        assert 'arg0' in RawOptions.get_all_argument_keys()
        assert 'arg1' in RawOptions.get_all_argument_keys()

    def test_option_has_default(self):
        """ it checks whether an option has a given default or not """
        assert RawOptions.option_has_default('quiet', False)
        assert not RawOptions.option_has_default('quiet', True)
