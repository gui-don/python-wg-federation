Feature: command line general features

  Scenario Outline: wg-federation shows help in all circumstances
    When we run program with "<help_option>"
    Then the output contains "usage\: wg\-federation"
    And the output contains "options\:"
    And the output does not contain "bleh\!"

    Examples: options
      | help_option  |
      | -h           |
      | hq -h        |
      | -h hq        |
      | hq run -h    |
      | hq -h run    |

  Scenario: wg-federation shows supported environment variables
    When we run program with "-h"
    Then the output contains "environment variables:"
    And the output contains "WG_FEDERATION_QUIET"
    And the output contains "WG_FEDERATION_LOG_LEVEL"
    And the output contains "WG_FEDERATION_VERBOSE"
    And the output contains "WG_FEDERATION_DEBUG"

  Scenario Outline: wg-federation shows it allows general options, even after arguments
    When we run program with "<help_command>"
    Then the output contains "-q, --quiet"
    And the output contains "-v, --verbose"
    And the output contains "-V, --version"

    Examples: options
      | help_command       |
      | hq -h              |
      | -h hq              |
      | hq run -h          |
      | hq -h bootstrap    |

  Scenario Outline: wg-federation shows its current version
    When we run program with "<version_option>"
    Then the output only contains current version

    Examples: options
      | version_option  |
      | -V              |
      | --version       |
