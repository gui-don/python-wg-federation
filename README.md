# wg-federation

A Wireguard federation server and client.

## Development

### Install, Develop & Run Package Locally

`virtualenv` must be installed on your system.

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
