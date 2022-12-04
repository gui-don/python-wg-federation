import pytest
from mockito import unstub, when, mock, verify

from wg_federation.crypto.message_signer import MessageSigner
from wg_federation.data_transformation.configuration_location_finder import ConfigurationLocationFinder
from wg_federation.data_transformation.loader.can_load_configuration_interface import CanLoadConfigurationInterface
from wg_federation.data_transformation.loader.configuration_loader import ConfigurationLoader
from wg_federation.data_transformation.loader.proxy.verify_signature_configuration_loader_proxy import \
    VerifySignatureConfigurationLoaderProxy
from wg_federation.exception.developer.data_transformation.invalid_data_error import InvalidDataError


# pylint: disable=duplicate-code


class TestVerifySignatureConfigurationLoaderProxy:
    """ Test VerifySignatureConfigurationLoaderProxy class """

    _configuration_location_finder: ConfigurationLocationFinder = None
    _configuration_loader: CanLoadConfigurationInterface = None
    _message_signer: MessageSigner = None
    _digest_configuration_loader: CanLoadConfigurationInterface = None

    _subject: VerifySignatureConfigurationLoaderProxy = None

    @pytest.fixture(autouse=True)
    def run_around_tests(self):
        """ Resets mock between tests """
        unstub()
        self.setup_method()

    def setup_method(self):
        """ Constructor """

        self._message_signer = mock()

        self._digest_configuration_loader = mock()
        when(self._digest_configuration_loader).load('digest_location').thenReturn({'location': 'side_digest'})

        self._configuration_location_finder = mock()
        when(self._configuration_location_finder).state_digest_belongs_to_state().thenReturn(True)
        when(self._configuration_location_finder).state_digest().thenReturn('digest_location')

        data = {'data': {'real': 'data'}, 'nonce': 'nonce', 'digest': 'digest'}
        self._configuration_loader = mock(ConfigurationLoader)
        when(self._configuration_loader).load_if_exists(...).thenReturn(data.copy())
        when(self._configuration_loader).load(...).thenReturn(data.copy())
        when(self._configuration_loader).load_all_if_exists(...).thenReturn(data.copy())
        when(self._configuration_loader).load_all(...).thenReturn(data.copy())

        self._subject = VerifySignatureConfigurationLoaderProxy(
            configuration_location_finder=self._configuration_location_finder,
            configuration_loader=self._configuration_loader,
            message_signer=self._message_signer,
            digest_configuration_loader=self._digest_configuration_loader,
        )

    def test_init(self):
        """ it can be instantiated """
        assert isinstance(self._subject, VerifySignatureConfigurationLoaderProxy)

    def test_loadx(self):
        """ it verifies configuration content signature after loading configuration """
        assert {'real': 'data'} == self._subject.load('source')
        assert {'real': 'data'} == self._subject.load_if_exists('source')
        assert {'real': 'data'} == self._subject.load_all_if_exists(('source', 'source2',))
        assert {'real': 'data'} == self._subject.load_all(('source', 'source2',))

        verify(self._message_signer, times=4).verify_sign(str({'real': 'data'}), 'nonce', 'digest')

    def test_loadx2(self):
        """ it verifies configuration content signature after loading configuration, with a side digest """
        when(self._configuration_location_finder).state_digest_belongs_to_state().thenReturn(False)

        assert {'real': 'data'} == self._subject.load('source')
        assert {'real': 'data'} == self._subject.load_if_exists('source')
        assert {'real': 'data'} == self._subject.load_all_if_exists(('source', 'source2',))
        assert {'real': 'data'} == self._subject.load_all(('source', 'source2',))

        verify(self._message_signer, times=4).verify_sign(str({'real': 'data'}), 'nonce', 'side_digest')

    def test_load2(self):
        """ it raises an error when loaded data was not signed and does not contain a 'data' key """
        data = {'real': 'data'}
        when(self._configuration_loader).load(...).thenReturn(data.copy())

        with pytest.raises(InvalidDataError) as error:
            self._subject.load('source')
        assert 'Data was not found' in str(error)

        verify(self._message_signer, times=0).verify_sign(...)

    def test_load3(self):
        """ it raises an error when loaded data was not signed and 'data' key is not a dict """
        data = {'data': 'not_valid'}
        when(self._configuration_loader).load(...).thenReturn(data.copy())

        with pytest.raises(InvalidDataError) as error:
            self._subject.load('source')
        assert 'Data is expected to be in a dict' in str(error)

        verify(self._message_signer, times=0).verify_sign(...)

    def test_load4(self):
        """ it raises an error when loaded data was not signed and 'nonce' key was not found """
        data = {'data': {'real': 'no_nonce'}, 'digest': 'digest'}

        when(self._configuration_loader).load(...).thenReturn(data.copy())

        with pytest.raises(InvalidDataError) as error:
            self._subject.load('source')
        assert 'A “nonce” was expected next to the data' in str(error)

        verify(self._message_signer, times=0).verify_sign(...)

    def test_load5(self):
        """ it raises an error when loaded data was not signed and 'digest' key was not found """
        data = {'data': {'real': 'no_digest'}, 'nonce': 'nonce'}

        when(self._configuration_loader).load(...).thenReturn(data.copy())

        with pytest.raises(InvalidDataError) as error:
            self._subject.load('source')
        assert 'A “digest” was expected next to the data' in str(error)

        verify(self._message_signer, times=0).verify_sign(...)

    def test_load6(self):
        """ it raises an error when side digest cannot be loaded """
        when(self._configuration_location_finder).state_digest_belongs_to_state().thenReturn(False)
        when(self._digest_configuration_loader).load('digest_location').thenRaise(RuntimeError)

        with pytest.raises(InvalidDataError) as error:
            self._subject.load('source')
        assert 'Fail to load digest from “digest_location” to verify data signature.' in str(error)

        verify(self._message_signer, times=0).verify_sign(...)
