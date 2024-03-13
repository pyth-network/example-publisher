import asyncio
import os
import sys
import threading
import uvicorn
from example_publisher.config import Config
from example_publisher.publisher import Publisher
import typed_settings as ts
import click
import logging
import structlog
from example_publisher.api.health_check import app, API

_DEFAULT_CONFIG_PATH = os.path.join("config", "config.toml")


log_level = logging._nameToLevel[os.environ.get("LOG_LEVEL", "DEBUG").upper()]
structlog.configure(wrapper_class=structlog.make_filtering_bound_logger(log_level))

log = structlog.get_logger()


@click.command()
@click.option(
    "--config",
    "config_path",
    default=_DEFAULT_CONFIG_PATH,
    help="Location of config file.",
)
def main(config_path):

    config: Config = ts.load(
        cls=Config,
        appname="publisher",
        config_files=[config_path],
    )

    publisher = Publisher(config=config)

    API.config = config
    API.publisher = publisher

    def run_server():
        uvicorn.run(app, host="0.0.0.0", port=config.health_check_port)

    server_thread = threading.Thread(target=run_server)
    server_thread.start()

    async def run():
        try:
            await publisher.start()
        except Exception:
            log.exception("Failed to start publisher")
            sys.exit(1)

    loop = asyncio.get_event_loop()
    asyncio.ensure_future(run())
    loop.run_forever()


if __name__ == "__main__":  # pragma: no cover
    main()
