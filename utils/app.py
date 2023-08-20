from db.base import AppTable

from core import bot
from aiogram import types

import template.app as tapp
import static


async def send_app(
    chat_id : int,
    app : AppTable
) -> types.Message:
    """
    
    Send app to user
    
    """


    photo_id = (
        app.photo_id 
        if app.photo_id is not None else static.anon
    ) 

    return await bot.send_photo(
        chat_id=chat_id,
        photo=photo_id,
        caption=tapp.app_text.format(app=app),
        reply_markup=tapp.app_kb(app)
    )