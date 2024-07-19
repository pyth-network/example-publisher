# Pyth Publisher
Propeller Heads publisher to [Pyth Agent websocket API](https://docs.pyth.network/price-feeds/publish-data/pyth-client-websocket-api).

The publisher: # TODO: update this
- Looks up the price accounts corresponding to the configured symbols from the on-chain program.
- Based on the configured provider, subscribes to the feeds on Pythnet, or polls the prices from Coingecko.
- Publishes price updates for those symbols in response to `notify_price_sched` messages from Pyth Agent.

## Prerequisites
This requires a running instance of the `pyth-agent` binary to be running. To set this up, follow the instructions in [Pyth Agent repository](https://github.com/pyth-network/pyth-agent). 
The`publisher.pythd.endpoint` configuration value should be set to the pyth-agent websocket endpoint (e.g. `ws://127.0.0.1:8910`).

## Configure
An example configuration file can be found in [`config/config.toml`](config/config.toml). The format of the configuration file is documented [here](pyth_publisher/config.py).

## Dev environment

- Create the dev environment `conda env create -f requirements/environment_dev.yaml`
- Activate it with `conda activate pyth-dev`
- Install dependencies with `pip install -r requirements/requirements.txt` 

## Run TODO - update run instructions

[Poetry](https://python-poetry.org/docs/) is used to manage the dependencies and run the tests. If you don't have it installed, you can install following the instructions [here](https://python-poetry.org/docs/#installation).

```bash
# Install the dependencies
poetry install

# Run the tests
poetry run pytest

# Run the publisher
poetry run example-publisher --config config/config.toml
```

