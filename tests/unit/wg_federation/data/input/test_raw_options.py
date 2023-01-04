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
        assert 0 == RawOptions.get_argument_depth([])
        assert 1 == RawOptions.get_argument_depth([
            CommandLineArgument()
        ])

    def test_get_all_argument_keys(self):
        """ it returns all possible arguments keys """
        assert 'arg0' in RawOptions.get_all_argument_keys()
        assert 'arg1' in RawOptions.get_all_argument_keys()

    def test_get_all_argument_options_names(self):
        """ it returns all arguments specific option names """
        assert [
            'private_key_retrieval_method',
            'interface_type',
            'interface_name'
        ] == RawOptions.get_all_argument_options_names(RawOptions.arguments)
