import pytest
from pydantic import ValidationError

from wg_federation.data.input.command_line.secret_retreival_method import SecretRetrievalMethod
from wg_federation.data.input.user_input import UserInput


class TestUserInput:
    """ Test UserInput class """

    _subject: UserInput = None

    def setup_method(self):
        """ Constructor """
        self._subject = UserInput(
            verbose=True,
            debug=True,
            arg0='test',
            root_passphrase='very_secret',
        )

    def test_init(self):
        """ it can be instantiated """
        assert isinstance(self._subject, UserInput)

    def test_data(self):
        """ it returns its data """
        assert True is self._subject.verbose
        assert True is self._subject.debug
        assert 'test' == self._subject.arg0
        assert 'very_secret' == self._subject.root_passphrase.get_secret_value()

    def test_check_private_key_retrieval_method(self):
        """ it raises an error if the private key retrieval method is command but no command is passed """
        with pytest.raises(ValidationError) as error:
            UserInput(private_key_retrieval_method=SecretRetrievalMethod.WG_FEDERATION_COMMAND)

        assert 'did not provide a command to get the root passphrase dynamically' in str(error.value)
