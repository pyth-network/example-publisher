import asyncio
import os
from publisher.config import Config
from publisher.publisher import Publisher
import typed_settings as ts
import click
import logging

_DEFAULT_CONFIG_PATH = os.path.join('config', 'config.toml')

logging.basicConfig(
    level=logging.DEBUG,
)

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
        await publisher.start()

    loop = asyncio.get_event_loop()
    asyncio.ensure_future(run())
    loop.run_forever()

if __name__ == '__main__':  # pragma: no cover
    main()
