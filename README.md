# wg-federation

A Wireguard federation server and client.

## Development

### Install, Develop & Run Package Locally

`virtualenv` and `pip` must be installed on your system.

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

### Run unit tests

```bash
pytest -v
```
