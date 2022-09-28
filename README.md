# wg-federation

A Wireguard federation server and client.

## Development

Python `virtualenv` must be installed on your system.

```bash
# Setup
python -m venv venv
source ./venv/bin/activate
pip install -e ".[dev]"
pip install -e ".[build]" # optional: if you want to build locally
wg-federation # To run wg-federation

# Deactivate
deactivate
```

### Run Unit Tests

```bash
pytest -v --spec
pytest -v --cov # To see coverage
```

### Run Functional Tests

```bash
behave tests/features
behave tests/features -w # To see all outputs of all features tagged @wip
```

### Setup IDE and Debugger
To avoid having to install the dependencies on your operating system, setup your IDE to use a python virtual environment “SDK”.
E.g. the `venv` directory you may have created above.
[Intellij/PyCharm provides this feature](https://www.jetbrains.com/help/idea/creating-virtual-environment.html).
This will allow the IDE to find the libraries in the virtual environment, run and debug the application.

To debug the application, run `src/wg_federation/__init__.py`

### Deploy Manually

#### Build
```bash
python -m build
```

#### Publish to Test PyPI
_Use `__token__` as a username to publish using a token_
```bash
twine upload --repository testpypi dist/*
```

#### Publish in Production (PyPI)
_Use `__token__` as a username to publish using a token_
```bash
twine upload dist/*
```

### Generate the documentation
```bash
make -C doc html
```
