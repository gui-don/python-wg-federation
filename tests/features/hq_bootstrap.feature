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

  @hq-bootstrap
  Scenario: hq bootstrap do not run when `hq bootstrap` are not the arguments
    When we run program with "hq -h"
    Then the system file “~/.local/share/wg-federation/state.digest” should not exist
    Then the system file “~/.local/share/wg-federation/state.json” should not exist
    Then the system file “~/.local/share/wg-federation/salt.txt” should not exist

  @hq-bootstrap
  Scenario: hq bootstrap creates puts the digest within the state file when specified
    When we run program with "hq bootstrap -P root-pass --state-digest-backend=DEFAULT --private-key-retrieval-method WG_FEDERATION_ENV_VAR_OR_FILE"
    Then the system file “~/.local/share/wg-federation/state.digest” should not exist
    Then the system file “~/.local/share/wg-federation/state.json” should exist
    Then the system file “~/.local/share/wg-federation/salt.txt” should exist
    Then the system file “~/.local/share/wg-federation/state.json” should contain “^{"data": {"federation":”
    Then the system file “~/.local/share/wg-federation/state.json” should contain “.+"digest": "[a-f0-9]+"}$”
    Then the system file “~/.local/share/wg-federation/state.json” should contain “.+"post_up": \["wg set %i private-key <\(wg-federation hq get-private-key.+”

  @hq-bootstrap
  Scenario: hq bootstrap shows a warning if the 'private-key-retrieval-method' is set to cleartext
    When we run program with "hq bootstrap -P root-pass --private-key-retrieval-method TEST_INSECURE_CLEARTEXT"
    Then the system file “~/.local/share/wg-federation/state.digest” should exist
    Then the system file “~/.local/share/wg-federation/state.json” should exist
    Then the system file “~/.local/share/wg-federation/salt.txt” should exist
    Then the system file “~/.local/share/wg-federation/state.json” should contain “^{"data": {"federation":”
    Then the system file “~/.local/share/wg-federation/state.json” should not contain “.+"post_up": .+”
    Then the stderr contains "The root passphrase retrieval method has been set to “TEST_INSECURE_CLEARTEXT”. This is insecure"

  @hq-bootstrap
  Scenario: hq bootstrap can fetch the root passphrase from a subcommand
    When we run program with "hq bootstrap --Pcmd "/usr/bin/echo dangerous do not do echo secrets like that" --private-key-retrieval-method WG_FEDERATION_COMMAND"
    Then the system file “~/.local/share/wg-federation/state.digest” should exist
    Then the system file “~/.local/share/wg-federation/state.json” should exist
    Then the system file “~/.local/share/wg-federation/salt.txt” should exist
    Then the system file “~/.local/share/wg-federation/state.json” should contain “^{"data": {"federation":”
    Then the system file “~/.local/share/wg-federation/state.json” should contain “.+"post_up": \["wg set %i private-key <\(wg-federation hq get-private-key.+”
    Then the stderr does not contain "The root passphrase retrieval method has been set to “TEST_INSECURE_CLEARTEXT”. This is insecure"
    Then the stderr does not contain "A root-passphrase-command was set but the root passphrase was retrieved through other means."

  @hq-bootstrap
  Scenario: hq bootstrap displays a warning if root passphrase and root subcommands are both used together
    When we run program with "hq bootstrap -P root-pass --Pcmd "/usr/bin/echo dangerous do not do echo secrets like that" --private-key-retrieval-method WG_FEDERATION_COMMAND"
    Then the stderr contains "A root-passphrase-command was set but the root passphrase was retrieved through other means."
