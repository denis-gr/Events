import asyncio
import logging

from main import start_bot

if __name__ == "__main__":
    logging.basicConfig(
            level=logging.INFO,
            format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger = logging.getLogger(__name__)
    logger.info("Starting")

    asyncio.run(start_bot())
