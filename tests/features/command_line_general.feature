Feature: command line general features

  @command-line-general
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

  @command-line-general
  Scenario: wg-federation shows supported environment variables
    When we run program with "-h"
    Then the output contains "environment variables:"
    And the output contains "WG_FEDERATION_QUIET"
    And the output contains "WG_FEDERATION_LOG_LEVEL"
    And the output contains "WG_FEDERATION_VERBOSE"
    And the output contains "WG_FEDERATION_DEBUG"

  @command-line-general
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

  @command-line-general
  Scenario Outline: wg-federation shows its current version
    When we run program with "<version_option>"
    Then the output only contains current version

    Examples: options
      | version_option |
      | -V             |
      | --version      |

  @command-line-general
  Scenario Outline: wg-federation shows its debug outputs when debug option is set, because this option has the highest precedence
    When we run program with "<logging_options>"
    Then the stderr contains "ConfigureLoggingController♦ was run in response"
    Then the stderr contains "HQBootstrapController♦ was skipped."

    Examples: equivalent options for debug logging
      | logging_options        |
      | --vv                   |
      | --vv --log-level ERROR |
      | --vv -v                |
      | --log-level DEBUG      |

  @command-line-general
  Scenario Outline: wg-federation do not info debug outputs by default
    When we run program with "<logging_options>"
    Then the stderr does not contain "ConfigureLoggingController"
    And the output does not contain "ConfigureLoggingController"
    And the syslog does not contain "ConfigureLoggingController"

    Examples: options
      | logging_options      |
      | hq                   |
      | --log-level CRITICAL |
      | --log-level ERROR    |
      | --log-level WARNING  |
      | --log-level INFO     |

  @command-line-general @environment-variables
  Scenario: setting up the debug flag displays all early debug outputs
    Given the environment variable "WG_FEDERATION_DEBUG" contains "True"
    When we run program with "--log-level CRITICAL"
    Then the stderr contains "Trying to fetch “WG_FEDERATION_QUIET” environment variable"
    Then the stderr contains "InputManager♦: Command line argument processed"
    Then the stderr contains "InputManager♦: Environment variables processed"
    Then the stderr contains "InputManager♦: Final processed user inputs"

  @command-line-general @configuration-files
  Scenario Outline: wg-federation show its debug outputs when debug option is set from configuration files
    Given a system file “<configuration_path>” contains the following content “debug: True”
    When we run program with "--log-level CRITICAL"
    Then the stderr contains "ConfigureLoggingController♦ was run in response"
    Then the stderr contains "HQBootstrapController♦ was skipped."

    Examples: system files
      | configuration_path                     |
      | /etc/wg-federation/main.yaml           |
      | ~/.local/share/wg-federation/main.yaml |

  @command-line-general @configuration-files
  Scenario: wg-federation overrides configuration files by the most specific
    Given a system file “/etc/wg-federation/main.yaml” contains the following content “debug: True”
    Given a system file “~/.local/share/wg-federation/main.yaml” contains the following content “debug: False”
    When we run program with "--log-level CRITICAL"
    Then the stderr does not contain "ConfigureLoggingController♦"
    Then the stderr does not contain "HQBootstrapController♦"

  @command-line-general @configuration-files
  Scenario: wg-federation displays a warning if a root passphrase secret is found in the configuration
    Given a system file “~/.local/share/wg-federation/main.yaml” contains the following content “root_passphrase: 'not so secret'”
    When we run program with "--log-level INFO"
    Then the stderr contains "This secret might be readable by whomever access the disk or the configuration file"
