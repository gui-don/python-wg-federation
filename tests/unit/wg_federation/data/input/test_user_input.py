from wg_federation.data.input.user_input import UserInput


class TestUserInput:
    """ Test UserInput class """

    _subject: UserInput = None

    def setup(self):
        """ Constructor """
        self._subject = UserInput(
            verbose=True,
            debug=True,
            arg0='test'
        )

    def test_init(self):
        """ it can be instantiated """
        assert isinstance(self._subject, UserInput)

    def test_data(self):
        """ it returns its data """
        assert True is self._subject.verbose
        assert True is self._subject.debug
        assert 'test' == self._subject.arg0
