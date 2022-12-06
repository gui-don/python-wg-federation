Feature: HQ bootstrap

  @hq-bootstrap
  Scenario: hq bootstrap runs when `hq bootstrap` are the arguments, make sure no secrets are in the state
    When we run program with "hq bootstrap -P root-pass"
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
    When we run program with "hq bootstrap -P root-pass --state-digest-backend=DEFAULT"
    Then the system file “~/.local/share/wg-federation/state.digest” should not exist
    Then the system file “~/.local/share/wg-federation/state.json” should exist
    Then the system file “~/.local/share/wg-federation/salt.txt” should exist
    Then the system file “~/.local/share/wg-federation/state.json” should contain “^{"data": {"federation":”
    Then the system file “~/.local/share/wg-federation/state.json” should contain “.+"digest": "[a-f0-9]+"}$”
