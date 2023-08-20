import asyncio
from loguru import logger

from aiogram import Dispatcher, types
from aiogram.dispatcher import DEFAULT_RATE_LIMIT
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.utils.exceptions import Throttled

from sqlalchemy.ext.asyncio import async_sessionmaker

import template.middleware as middleware



class TelegramMiddleware(BaseMiddleware):
    """
    Middleware

    """
    def __init__(
        self, sessionmaker : async_sessionmaker, 
        limit=DEFAULT_RATE_LIMIT, 
        key_prefix='antiflood_'
    ):
        self.rate_limit = limit
        self.prefix = key_prefix
        self.sessionmaker = sessionmaker

        super(TelegramMiddleware, self).__init__()


    async def on_pre_process_message(
        self, message: types.Message, 
        data: dict,
    ):
        """
        This handler is called when dispatcher receives a message
        :param message:
        """


        logger.info(middleware.message.format(
            message=message
        ))
        data.setdefault("db", self.sessionmaker())
        # Get current handler
        # handler = current_handler.get()
        # Get dispatcher from context
        # dispatcher = Dispatcher.get_current()

        # If handler was configured, get rate limit and key from handler

    async def on_pre_process_callback_query(
        self, callback : types.CallbackQuery, 
        data: dict
    ):
        data.setdefault("db", self.sessionmaker())

