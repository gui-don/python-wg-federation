Feature: HQ bootstrap

  @hq-bootstrap
  Scenario: hq bootstrap runs when `hq bootstrap` are the arguments, make sure no secrets are in the state
    When we run program with "hq bootstrap -P root-pass --private-key-retrieval-method WG_FEDERATION_ENV_VAR_OR_FILE"

    Then the system file “~/.local/share/wg-federation/state.digest” should exist
    Then the system file “~/.local/share/wg-federation/state.json” should exist
    Then the system file “~/.local/share/wg-federation/salt.txt” should exist
    Then the system file “~/.local/share/wg-federation/state.json” should contain “^{"data": {"federation":”
    Then the system file “~/.local/share/wg-federation/state.json” should contain “.+"nonce": "[a-f0-9]+"}$”
    Then the system file “~/.local/share/wg-federation/state.json” should not contain “.+"private_key": "”
    Then the system file “~/.local/share/wg-federation/state.json” should not contain “.+"psk": "”
    Then the system file “~/.local/share/wg-federation/state.digest” should contain “^[a-f0-9]+$”

    Then the system file “${XDG_RUNTIME_DIR}/wg-federation/interfaces/wg-federation0.conf” should contain “^\[Interface\]\n”
    Then the system file “${XDG_RUNTIME_DIR}/wg-federation/forums/wgf-forum0.conf” should contain “^\[Interface\]\n”
    Then the system file “${XDG_RUNTIME_DIR}/wg-federation/phone_lines/wgf-phoneline0.conf” should contain “^\[Interface\]\n”
    Then the system file “${XDG_RUNTIME_DIR}/wg-federation/interfaces/wg-federation0.conf” should contain “^postup = wg set \%i private-key .*”
    Then the system file “${XDG_RUNTIME_DIR}/wg-federation/forums/wgf-forum0.conf” should contain “^postup \= wg set \%i private-key .*”
    Then the system file “${XDG_RUNTIME_DIR}/wg-federation/phone_lines/wgf-phoneline0.conf” should contain “^postup \= wg set \%i private-key .*”
    Then the system file “${XDG_RUNTIME_DIR}/wg-federation/interfaces/wg-federation0.conf” should not contain “^privatekey = .*”
    Then the system file “${XDG_RUNTIME_DIR}/wg-federation/forums/wgf-forum0.conf” should not contain “^privatekey = .*”
    Then the system file “${XDG_RUNTIME_DIR}/wg-federation/phone_lines/wgf-phoneline0.conf” should not contain “^privatekey = .*”

    Then the stderr does not contain "Traceback (most recent call last)"

  @hq-bootstrap
  Scenario: hq bootstrap do not run when `hq bootstrap` are not the arguments
    When we run program with "hq -h"
    Then the system file “~/.local/share/wg-federation/state.digest” should not exist
    Then the system file “~/.local/share/wg-federation/state.json” should not exist
    Then the system file “~/.local/share/wg-federation/salt.txt” should not exist

    Then the system file “${XDG_RUNTIME_DIR}/wg-federation/interfaces/wg-federation0.conf” should not exist
    Then the system file “${XDG_RUNTIME_DIR}/wg-federation/forums/wgf-forum0.conf” should not exist
    Then the system file “${XDG_RUNTIME_DIR}/wg-federation/phone_lines/wgf-phoneline0.conf” should not exist

    Then the stderr does not contain "Traceback (most recent call last)"

  @hq-bootstrap
  Scenario: hq bootstrap creates puts the digest within the state file when specified
    When we run program with "hq bootstrap -P root-pass --state-digest-backend=DEFAULT --private-key-retrieval-method WG_FEDERATION_ENV_VAR_OR_FILE"
    Then the system file “~/.local/share/wg-federation/state.digest” should not exist
    Then the system file “~/.local/share/wg-federation/state.json” should exist
    Then the system file “~/.local/share/wg-federation/salt.txt” should exist
    Then the system file “~/.local/share/wg-federation/state.json” should contain “^{"data": {"federation":”
    Then the system file “~/.local/share/wg-federation/state.json” should contain “.+"digest": "[a-f0-9]+"}$”
    Then the system file “~/.local/share/wg-federation/state.json” should contain “.+"post_up": \["wg set %i private-key <\(wg-federation hq get-private-key.+”

    Then the system file “${XDG_RUNTIME_DIR}/wg-federation/interfaces/wg-federation0.conf” should contain “^\[Interface\]\n”
    Then the system file “${XDG_RUNTIME_DIR}/wg-federation/forums/wgf-forum0.conf” should contain “^\[Interface\]\n”
    Then the system file “${XDG_RUNTIME_DIR}/wg-federation/phone_lines/wgf-phoneline0.conf” should contain “^\[Interface\]\n”
    Then the system file “${XDG_RUNTIME_DIR}/wg-federation/interfaces/wg-federation0.conf” should contain “^postup = ”
    Then the system file “${XDG_RUNTIME_DIR}/wg-federation/forums/wgf-forum0.conf” should contain “^postup = ”
    Then the system file “${XDG_RUNTIME_DIR}/wg-federation/phone_lines/wgf-phoneline0.conf” should contain “^postup = ”
    Then the system file “${XDG_RUNTIME_DIR}/wg-federation/interfaces/wg-federation0.conf” should not contain “^privatekey = .*”
    Then the system file “${XDG_RUNTIME_DIR}/wg-federation/forums/wgf-forum0.conf” should not contain “^privatekey = .*”
    Then the system file “${XDG_RUNTIME_DIR}/wg-federation/phone_lines/wgf-phoneline0.conf” should not contain “^privatekey = .*”

    Then the stderr does not contain "Traceback (most recent call last)"

  @hq-bootstrap
  Scenario: hq bootstrap shows a warning if the 'private-key-retrieval-method' is set to cleartext
    When we run program with "hq bootstrap -P root-pass --private-key-retrieval-method TEST_INSECURE_CLEARTEXT"
    Then the system file “~/.local/share/wg-federation/state.digest” should exist
    Then the system file “~/.local/share/wg-federation/state.json” should exist
    Then the system file “~/.local/share/wg-federation/salt.txt” should exist
    Then the system file “~/.local/share/wg-federation/state.json” should contain “^{"data": {"federation":”
    Then the system file “~/.local/share/wg-federation/state.json” should not contain “.+"post_up": .+”
    Then the stderr contains "The root passphrase retrieval method has been set to “TEST_INSECURE_CLEARTEXT”. This is insecure"

    Then the system file “${XDG_RUNTIME_DIR}/wg-federation/interfaces/wg-federation0.conf” should contain “^\[Interface\]\n”
    Then the system file “${XDG_RUNTIME_DIR}/wg-federation/forums/wgf-forum0.conf” should contain “^\[Interface\]\n”
    Then the system file “${XDG_RUNTIME_DIR}/wg-federation/phone_lines/wgf-phoneline0.conf” should contain “^\[Interface\]\n”
    Then the system file “${XDG_RUNTIME_DIR}/wg-federation/interfaces/wg-federation0.conf” should not contain “^postup = ”
    Then the system file “${XDG_RUNTIME_DIR}/wg-federation/forums/wgf-forum0.conf” should not contain “^postup = ”
    Then the system file “${XDG_RUNTIME_DIR}/wg-federation/phone_lines/wgf-phoneline0.conf” should not contain “^postup = ”
    Then the system file “${XDG_RUNTIME_DIR}/wg-federation/interfaces/wg-federation0.conf” should contain “^privatekey = [0-9A-Za-z+/]{43}[=]”
    Then the system file “${XDG_RUNTIME_DIR}/wg-federation/forums/wgf-forum0.conf” should contain “^privatekey = [0-9A-Za-z+/]{43}[=]”
    Then the system file “${XDG_RUNTIME_DIR}/wg-federation/phone_lines/wgf-phoneline0.conf” should contain “^privatekey = [0-9A-Za-z+/]{43}[=]”

    Then the stderr does not contain "Traceback (most recent call last)"

  @hq-bootstrap
  Scenario: hq bootstrap can fetch the root passphrase from a subcommand
    When we run program with "hq bootstrap --Pcmd "echo dangerous do not do echo secrets like that" --private-key-retrieval-method WG_FEDERATION_COMMAND"
    Then the system file “~/.local/share/wg-federation/state.digest” should exist
    Then the system file “~/.local/share/wg-federation/state.json” should exist
    Then the system file “~/.local/share/wg-federation/salt.txt” should exist
    Then the system file “~/.local/share/wg-federation/state.json” should contain “^{"data": {"federation":”
    Then the system file “~/.local/share/wg-federation/state.json” should contain “.+"post_up": \["wg set %i private-key <\(wg-federation hq get-private-key.+”

    Then the system file “${XDG_RUNTIME_DIR}/wg-federation/interfaces/wg-federation0.conf” should contain “^\[Interface\]\n”
    Then the system file “${XDG_RUNTIME_DIR}/wg-federation/forums/wgf-forum0.conf” should contain “^\[Interface\]\n”
    Then the system file “${XDG_RUNTIME_DIR}/wg-federation/phone_lines/wgf-phoneline0.conf” should contain “^\[Interface\]\n”
    Then the system file “${XDG_RUNTIME_DIR}/wg-federation/interfaces/wg-federation0.conf” should contain “^postup =.*echo dangerous do not do echo secrets like that”
    Then the system file “${XDG_RUNTIME_DIR}/wg-federation/forums/wgf-forum0.conf” should contain “^postup =.*echo dangerous do not do echo secrets like that”
    Then the system file “${XDG_RUNTIME_DIR}/wg-federation/phone_lines/wgf-phoneline0.conf” should contain “^postup =.*echo dangerous do not do echo secrets like that”
    Then the system file “${XDG_RUNTIME_DIR}/wg-federation/interfaces/wg-federation0.conf” should not contain “^privatekey = .*”
    Then the system file “${XDG_RUNTIME_DIR}/wg-federation/forums/wgf-forum0.conf” should not contain “^privatekey = .*”
    Then the system file “${XDG_RUNTIME_DIR}/wg-federation/phone_lines/wgf-phoneline0.conf” should not contain “^privatekey = .*”

    Then the stderr does not contain "The root passphrase retrieval method has been set to “TEST_INSECURE_CLEARTEXT”. This is insecure"
    Then the stderr does not contain "A root-passphrase-command was set but the root passphrase was retrieved through other means."

    Then the stderr does not contain "Traceback (most recent call last)"

  @hq-bootstrap
  Scenario: hq bootstrap displays a warning if root passphrase and root subcommands are both used together
    When we run program with "hq bootstrap -P root-pass --Pcmd "echo dangerous do not do echo secrets like that" --private-key-retrieval-method WG_FEDERATION_COMMAND"
    Then the stderr contains "A root-passphrase-command was set but the root passphrase was retrieved through other means."
    Then the stderr does not contain "Traceback (most recent call last)"

  @hq-bootstrap
  Scenario: hq bootstrap fails when the private key retrieval method is WG_FEDERATION_COMMAND but no command is provided
    When we run program with "hq bootstrap -P root-pass --private-key-retrieval-method WG_FEDERATION_COMMAND"
    Then the stderr contains "The method to retrieve WireGuard interface’s private keys was set to “WG_FEDERATION_COMMAND” \(the default value for this setting\), but you did not provide a command to get the root passphrase dynamically. Please set --root-passphrase-command or choose another method."
    Then the stderr does not contain "Traceback (most recent call last)"
