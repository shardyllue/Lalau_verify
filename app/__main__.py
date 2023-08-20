from asyncio import create_task

from aiogram import executor
from loguru import logger


from utils import schedular_main

from core import Dispatcher, dp
from core.middleware import TelegramMiddleware

from db import Session

from handler import dp


# from core import bot
# from aiogram.types import ChatPermissions
# from utils import config

async def on_startup(dp : Dispatcher):
    logger.info("Start up")

    dp.middleware.setup(TelegramMiddleware(
        Session
    ))

    create_task(schedular_main.scheduler_startup(
        Session
    ))

    # await bot.restrict_chat_member(
    #     chat_id=config.PUBLIC_GROUP, 
    #     user_id=5683272461,
    #     permissions=ChatPermissions(True),
    #     can_send_messages=True,
    # )

async def on_shutdown(dp : Dispatcher):
    logger.info("Shutdown down")

    


if __name__ == "__main__":
    
    executor.start_polling(
        dispatcher=dp,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
    )