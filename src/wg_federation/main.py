""" Main class """

from wg_federation.controller.controller_events import ControllerEvents
from wg_federation.di.container import Container
from wg_federation.input.manager.input_manager import InputManager
from wg_federation.observer.event_dispatcher import EventDispatcher


class Main:
    """ Main """

    _container: Container = None

    def __init__(self, container: Container = None):
        """
        Constructor
        """
        if self._container is None:
            self._container = container or Container()

        self._container.wire(modules=[__name__])

    def main(self) -> int:
        """ main """
        input_manager: InputManager = self._container.input_manager()
        user_input = input_manager.parse_all()
        self._container.user_input.override(user_input)

        controller_dispatcher: EventDispatcher = self._container.controller_dispatcher()
        controller_dispatcher.dispatch([
            ControllerEvents.CONTROLLER_BASELINE,
            ControllerEvents.CONTROLLER_MAIN,
            ControllerEvents.CONTROLLER_LATE,
        ], user_input)

        # NEXT

        # wireguard_key_generator = self._container.wireguard_key_generator()
        # print(wireguard_key_generator.generate_key_pairs())
        # print(wireguard_key_generator.generate_psk())
        # crypto = self._container.cryptographic_key_deriver()
        #
        # configuration_loader = self._container.configuration_loader()
        #
        # state_data_manager = self._container.state_data_manager()
        #
        # # state_data = Dummy(**configuration_loader.load_if_exists(StateDataManager.STATE_FILE))
        #
        # print('NOW UPDATING')
        # state_data = state_data_manager.reload()
        #
        # print(state_data)
        #
        # print(self._container.cryptographic_key_deriver().get_cache_status())
        #
        # if user_input.arg0 == 'hq':
        # import random
        # from Crypto.Hash import Poly1305
        # from Crypto.Cipher import AES
        # from binascii import unhexlify
        # import json.
        #
        # secret = b'This is the user root passphrase'
        #
        # write_mac = Poly1305.new(key=secret, cipher=AES)
        # write_nonce_hex = write_mac.nonce.hex()
        #
        # write_state = {'data': {'test': self.randomword(16)}, 'nonce': write_nonce_hex}
        #
        # write_msg_data_byte = str(write_state.get('data')).encode('UTF-8')
        # write_mac.update(write_msg_data_byte)
        #
        # with open(file="state.txt", mode="w", encoding='utf-8') as state:
        #     json.dump(write_state, state)
        #
        # […] Below is checking the signature
        #
        # with open(file="state.txt", mode='r', encoding='utf-8') as state:
        #     loaded_json_msg = json.load(state)
        #
        # loaded_msg_data_byte = str(loaded_json_msg.get('data')).encode('UTF-8')
        # loaded_nonce = unhexlify(loaded_json_msg.get('nonce'))
        #
        # try:
        #     loaded_mac = Poly1305.new(key=secret, nonce=loaded_nonce, cipher=AES, data=loaded_msg_data_byte)
        #     loaded_mac.hexverify(loaded_mac.hexdigest())
        #     print("The message '%s' is authentic" % loaded_json_msg)
        # except ValueError:
        #     print("The message or the key is wrong")
        #
        # exit(0)
        #
        # from Crypto.Hash import BLAKE2b
        #
        # from Crypto.PublicKey import ECC
        #
        # message = b'I give my permission to order #4355'
        #
        # key = ECC.import_key(open('privkey.der').read())
        #
        # h = BLAKE2b.new(message)
        #
        # signer = DSS.new(key, 'fips-186-3')
        #
        # signature = signer.sign(h)

        # configuration_loader = self._container.configuration_loader()
        # print(configuration_loader.load(YamlFileConfigurationLoader.get_supported_source(), ('.pre-commit-config.yaml',)))

        # ok = WireguardInterfaceConfig(
        #     name='toto',
        #     server_private_key='L9kYW/Kej96/L4Ae2lK50X46gJMfrplRAY4WbK0w4iYRE=',
        #     server_public_key='L9kYW/Kej96/L4Ae2lK5X46gJMfrplRAY4WbK0w4YRE=',
        #     listen_port=35233,
        #     mtu=68,
        #     # dns=['1.1.1.1'],
        #     addresses=['10.10.100.1/24'],
        # )
        # ok2 = WireguardInterfaceConfig(
        #     name='tata',
        #     server_private_key='L9kYW/Kej96/L4Ae2lK5X46gJMfrplRAY4WbK0w4iYRE=',
        #     server_public_key='L9kYW/Kej96/L4Ae2lK5X46gJMfrplRAY4WbK0w4YRE=',
        #     listen_port=35243,
        #     mtu=68,
        #     # dns=['1.1.1.1'],
        #     addresses=['10.10.10.1'],
        # )
        # federation = FederationConfig(
        #     name="tartzepaezai",
        #     forum_min_port=64900,
        #     forum_max_port=65000,
        # )
        # wir = MainConfig(federation=federation, interfaces={'federation0': ok, 'federation1': ok2})
        # # wir.interfaces.update({})
        #
        #
        # print('-----------------------')
        #
        # with open('test.yaml', 'a+') as fp:
        #     fp.seek(0)
        #     data = yaml.safe_load(fp)
        #
        #     if None is data:
        #         data = {}
        #
        #     print(data)
        #     print('-----------------------')
        #
        #     print(wir.to_yaml_ready_dict())
        #
        #     data.update(wir.to_yaml_ready_dict())
        #
        # with open('test.yaml', 'w') as fp:
        #     yaml.dump(data, fp)
        #
        # print('-----------------------')
        # print(data)
        return 0
