# Example Pyth Publisher
An example publisher demonstrating how to use the [Pythd websocket API](https://github.com/pyth-network/pyth-client/blob/main/doc/websocket_api.md) to publish prices to Pyth.

The publisher:
- Looks up the price accounts corresponding to the configured symbols from the on-chain program.
- Continually polls CoinGecko for the latest prices for those symbols.
- Publishes price updates for those symbols in response to `notify_price_sched` messages from Pythd. A configurable amount of fuzzing is applied to each update, and the confidence interval is sampled from a configurable Laplace distribution.

## Configure
An example configuration file can be found in [`config/config.toml`](config/config.toml). The format of the configuration file is documented [here](publisher/config.py).

## Run
```bash
# Create and activate a virtualenv to run the publisher in
python -m venv .venv
. .venv/bin/activate
pip install --upgrade setuptools pip

# Install the publisher
pip install -e .

# Run the publisher
python -m publisher --config=config/config.toml
```
