0.3.0
=====

- feat: now able to load configuration from `/(etc|XDG_DATA_HOME)/wg-federation/main.yaml`
- feat: adds many new classes for data transformation
- refactor: changes code namespacing to prepare for next features
- test: introduces `mockito` as a mock framework
- chore: adds `pyyaml`, `deepmerge` and `xdg` as dependencies

0.2.1
=====

- refactor: changes `RawOptions` dict into an object

0.2.0
=====

- feat: adds a `option_has_default` method in  `RawOptions`
- feat: implements a simple controller module, with `ConfigureLoggingController` as a first concrete implementation
- feat: allows to set a `EARLY_DEBUG` flag manually or via env var to facilitate debug of early code, like input processing
- refactor: changes the service `Container` to a dynamic instead of declarative, to ease unit testing.
- chore: adjust pre-commit `pylint` rules and explains them
- fix: adds a `CRITICAL` log level, to align with the `logging` library
- fix: makes sur all options in `RawOptions` delivers a `name`
- test: adjusts unit test of existing code after the refactor
- test: adds unit tests for the controller module
- test: adds scenarios to test the new controller
- doc: regenerates documentation

0.1.1
=====

- doc: better explains in the `README.md` how to generate documentation
- doc: temporarily adds auto-generated module documentation, waiting for a pipeline.
- refactor: Initializes `InputManager` attributes with `None` to avoid implicit attributions

0.1.0
=====

- feat: adds argument parsing, environment variable reading and input validations
- doc: explains how to generate documentation in the README
- doc: explains how to setup debugger for this project in README
- doc: explains how to run functional tests in README
- chore: updates/add `.pyproject.toml` dependencies
- chore: updates pre-commit dependencies
- chore: makes python `3.9` the minimum version, because we use type hinting 3.9+
- test: disables `missing-module-docstring` for pylint as it makes no sense in a one file/one class setting
- test: adds first batch of unit tests, covering 99% of the code
- test: adds first feature functional tests with `behave`
- refactor: removes unneeded dummy code

0.0.3
=====

- feat: adds first documentation

0.0.2
=====

- fix: fix reading of version for packaged version again

0.0.1
=====

- fix: fix reading of version for packaged versions

0.0.0
=====

- tech: initial version
