import asyncio
import os
import sys
import threading
import uvicorn

from pyth_publisher.config import config
from pyth_publisher.publisher import Publisher
import click
import logging
import structlog
from pyth_publisher.api.health_check import app, API


log_level = logging._nameToLevel[os.environ.get("LOG_LEVEL", "DEBUG").upper()]
structlog.configure(wrapper_class=structlog.make_filtering_bound_logger(log_level))

log = structlog.get_logger()


@click.command()
def main():
    publisher = Publisher(config=config)
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
