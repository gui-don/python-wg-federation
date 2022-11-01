Feature: command line general features

  Scenario Outline: wg-federation shows help in all circumstances
    When we run program with "<help_option>"
    Then the output contains "usage\: wg\-federation"
    And the output contains "options\:"
    And the output does not contain "bleh\!"

    Examples: options
      | help_option |
      | -h          |
      | hq -h       |
      | -h hq       |
      | hq run -h   |
      | hq -h run   |

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
      | help_command    |
      | hq -h           |
      | -h hq           |
      | hq run -h       |
      | hq -h bootstrap |

  Scenario Outline: wg-federation shows its current version
    When we run program with "<version_option>"
    Then the output only contains current version

    Examples: options
      | version_option |
      | -V             |
      | --version      |

  Scenario Outline: wg-federation shows its debug outputs when debug option is set, because this option has the highest precedence
    When we run program with "<logging_options>"
    Then the stderr contains "<class 'wg_federation.controller.baseline.configure_logging_controller.ConfigureLoggingController'> was run."

    Examples: equivalent options for debug logging
      | logging_options       |
      | -vv                   |
      | -vv --log-level ERROR |
      | -vv -v                |
      | --log-level DEBUG     |

  Scenario Outline: wg-federation do not info debug outputs by default
    When we run program with "<logging_options>"
    Then the stderr does not contain "wg_federation.controller.configure_logging_controller.ConfigureLoggingController"
    And the output does not contain "wg_federation.controller.configure_logging_controller.ConfigureLoggingController"
    And the syslog does not contain "wg_federation.controller.configure_logging_controller.ConfigureLoggingController"

    Examples: options
      | logging_options      |
      | hq                   |
      | --log-level CRITICAL |
      | --log-level ERROR    |
      | --log-level WARNING  |
      | --log-level INFO     |

  Scenario: setting up the debug flag displays all early debug outputs
    Given the environment variable "WG_FEDERATION_DEBUG" contains "True"
    When we run program with "--log-level CRITICAL"
    Then the stderr contains "Trying to fetch “WG_FEDERATION_QUIET” environment variable"
    Then the stderr contains "InputManager: Command line argument processed"
    Then the stderr contains "InputManager: Environment variables processed"
    Then the stderr contains "InputManager: Final processed user inputs"
