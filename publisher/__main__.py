import asyncio
import os
import sys
from publisher.config import Config
from publisher.publisher import Publisher
import typed_settings as ts
import click
import logging
from structlog import get_logger

_DEFAULT_CONFIG_PATH = os.path.join('config', 'config.toml')

logging.basicConfig(
    level=logging.DEBUG,
)

log = get_logger()

@click.command()
@click.option('--config', 'config_path', default=_DEFAULT_CONFIG_PATH, help='Location of config file.')
def main(config_path):

    config = ts.load(
        cls=Config,
        appname="publisher",
        config_files=[config_path],
    )

    publisher = Publisher(config=config)

    async def run():
        try:
            await publisher.start()
        except:
            log.exception("Failed to start publisher")
            sys.exit(1)

    loop = asyncio.get_event_loop()
    asyncio.ensure_future(run())
    loop.run_forever()

if __name__ == '__main__':  # pragma: no cover
    main()
