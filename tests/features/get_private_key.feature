Feature: HQ bootstrap

  @get-private-key
  Scenario Outline: get-private-key returns a key after `hq bootstrap`, with correct interface name and kind
    When we run program with "hq bootstrap -P root-pass --private-key-retrieval-method WG_FEDERATION_ENV_VAR_OR_FILE"
    When we run program with "hq get-private-key -P root-pass <kind> <name>"
    Then the output contains "^[0-9A-Za-z+/]{43}[=]$"

    Examples: options
      | kind                         | name                              |
      | -k phone_lines               | --interface-name 'wgf-phoneline0' |
      | --interface-kind phone_lines | -i wgf-phoneline0                 |
      | -k interfaces                | -i wg-federation0                 |
      | --interface-kind forums      | --interface-name "wgf-forum0"     |

  @get-private-key
  Scenario Outline: get-private-key returns nothing when the interface name does not exits
    When we run program with "hq bootstrap -P root-pass --private-key-retrieval-method WG_FEDERATION_ENV_VAR_OR_FILE"
    When we run program with "hq get-private-key -P root-pass <kind> <name>"
    Then the output does not contain "^[0-9A-Za-z+/]{43}[=]$"

    Examples: options
      | kind           | name              |
      | -k phone_lines | -i fail           |
      | -k phone_lines | -i wg-federation0 |
      | -k interfaces  | -i wg-federation1 |
      | -k interfaces  |                   |

  @get-private-key
  Scenario Outline: get-private-key fails gracefully if `hq bootstrap` was not run before
    When we run program with "hq get-private-key -P root-pass <kind> <name>"
    Then the output does not contain "^[0-9A-Za-z+/]{43}[=]$"
    Then the stderr contains "Unable to load the state: it was not bootstrapped. Run `hq boostrap`."

    Examples: options
      | kind           | name              |
      | -k phone_lines | -i wgf-phoneline0 |
      | -k interfaces  | -i wg-federation0 |
      | -k forums      | -i wgf-forum0     |

  @get-private-key
  Scenario Outline: get-private-key fails gracefully if the interface kind is not valid
    When we run program with "hq bootstrap -P root-pass --private-key-retrieval-method WG_FEDERATION_ENV_VAR_OR_FILE"
    When we run program with "hq get-private-key -P root-pass <kind> -i wg-federation0"
    Then the output does not contain "^[0-9A-Za-z+/]{43}[=]$"
    Then the stderr contains "permitted: 'interfaces', 'phone_lines', 'forums'"

    Examples: options
      | kind           |
      | -k invalid     |
      | -k phone_line  |

  @get-private-key
  Scenario: get-private-key fails gracefully if the root passphrase is incorrect
    When we run program with "hq bootstrap -P root-pass --private-key-retrieval-method WG_FEDERATION_ENV_VAR_OR_FILE"
    Then the stderr does not contain "State integrity failed. Are you sure you used the correct passphrase?"
    When we run program with "hq get-private-key -P wrong-pass -k interfaces -i wg-federation0"
    Then the output does not contain "^[0-9A-Za-z+/]{43}[=]$"
    Then the stderr contains "State integrity failed. Are you sure you used the correct passphrase?"
