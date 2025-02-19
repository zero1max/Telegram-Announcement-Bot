import asyncio
import logging
import sys

from loader import bot, dp
import handlers.start

async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())