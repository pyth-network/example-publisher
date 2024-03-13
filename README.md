# Example Pyth Publisher
An example publisher demonstrating how to use the [Pyth Agent websocket API](https://docs.pyth.network/price-feeds/publish-data/pyth-client-websocket-api) to publish prices to Pyth. **Pyth publishers publish their own first party data to the Pyth network. This example is created solely for demonstration/testing purposes and is not used in production by any publisher.**

The publisher:
- Looks up the price accounts corresponding to the configured symbols from the on-chain program.
- Based on the configured provider, subscribes to the feeds on Pythnet, or polls the prices from Coingecko.
- Publishes price updates for those symbols in response to `notify_price_sched` messages from Pyth Agent.

## Prerequisites
This requires a running instance of the `pyth-agent` binary to be running. To set this up, follow the instructions in [Pyth Agent repository](https://github.com/pyth-network/pyth-agent). This example publisher's `publisher.pythd.endpoint` configuration value should be set to the pyth-agent websocket endpoint (e.g. `ws://127.0.0.1:8910`).

## Configure
An example configuration file can be found in [`config/config.toml`](config/config.toml). The format of the configuration file is documented [here](example_publisher/config.py).

## Run

[Poetry](https://python-poetry.org/docs/) is used to manage the dependencies and run the tests. If you don't have it installed, you can install following the instructions [here](https://python-poetry.org/docs/#installation).

```bash
# Install the dependencies
poetry install

# Run the tests
poetry run pytest

# Run the publisher
poetry run example-publisher --config config/config.toml
```
